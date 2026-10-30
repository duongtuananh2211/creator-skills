#!/usr/bin/env python3
"""Helper for the long-video-to-shorts skill: transcribe a long video and cut vertical clips.

Subcommands (each prints compact JSON to stdout, progress goes to stderr):
  probe VIDEO                       Duration, size, fps, audio, and which tools/filters exist.
  transcribe VIDEO [--srt FILE] [--model PATH] [--lang vi] [--prompt TEXT] [--out DIR]
                                    Timed transcript as transcript.json + transcript.txt.
                                    --srt imports an existing .srt/.vtt (e.g. downloaded from
                                    YouTube Studio) instead of running whisper.cpp.
  cutpoints VIDEO [--out DIR] [--noise -35] [--min-silence 0.3] [--scene 0.3]
                                    Silences and scene changes, for placing clean cuts.
  render PLAN [--only 01,03] [--dry-run]
                                    Cut each clip in plan.json to 1080x1920 MP4 plus an .srt
                                    of its own captions.

Needs ffmpeg/ffprobe on PATH. Transcription needs whisper.cpp (`brew install whisper-cpp`)
and a ggml model; nothing else outside the Python standard library is used.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OUT_W, OUT_H = 1080, 1920
MODEL_DIRS = [Path.home() / ".cache" / "whisper.cpp", Path.home() / ".cache" / "whisper"]
# Preferred first: turbo is close to large-v3 on Vietnamese and several times faster.
MODEL_PREFERENCE = [
    "ggml-large-v3-turbo.bin", "ggml-large-v3-turbo-q5_0.bin", "ggml-large-v3-turbo-q8_0.bin",
    "ggml-large-v3.bin", "ggml-medium.bin", "ggml-small.bin",
]
WHISPER_BINS = ["whisper-cli", "whisper-cpp", "whisper.cpp"]
# Caption chunks: short lines read better on a phone than whole sentences.
CAPTION_MAX_WORDS = 7
CAPTION_MIN_DUR = 0.6


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def fail(msg, **extra):
    emit({"error": msg, **extra})
    sys.exit(1)


def run(cmd, capture=True):
    return subprocess.run(cmd, capture_output=capture, text=True)


def require_ffmpeg():
    missing = [b for b in ("ffmpeg", "ffprobe") if not shutil.which(b)]
    if missing:
        fail(f"missing {', '.join(missing)}", hint="brew install ffmpeg")


def ffmpeg_filters():
    out = run(["ffmpeg", "-hide_banner", "-filters"]).stdout
    return {line.split()[1] for line in out.splitlines() if len(line.split()) > 2 and line.startswith(" ")}


def find_whisper_bin():
    for name in WHISPER_BINS:
        path = shutil.which(name)
        if path:
            return path
    return None


def find_model(explicit=None):
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_file() else None
    env = os.environ.get("WHISPER_MODEL")
    if env and Path(env).expanduser().is_file():
        return Path(env).expanduser()
    for d in MODEL_DIRS:
        for name in MODEL_PREFERENCE:
            if (d / name).is_file():
                return d / name
    return None


def fmt_ts(sec):
    sec = max(0.0, sec)
    m, s = divmod(sec, 60)
    return f"{int(m):02d}:{s:04.1f}"


def srt_ts(sec):
    ms = int(round(max(0.0, sec) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_ts(value):
    """'00:01:02,500', '01:02.5' or '62.5' -> seconds."""
    value = value.strip().replace(",", ".")
    parts = value.split(":")
    sec = 0.0
    for part in parts:
        sec = sec * 60 + float(part)
    return sec


def stem_dir(video, out):
    return Path(out) if out else Path("shorts") / Path(video).stem


# ---------- probe ----------

def probe(video):
    require_ffmpeg()
    if not Path(video).is_file():
        fail(f"not a file: {video}")
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", video])
    if r.returncode:
        fail("ffprobe failed", stderr=r.stderr.strip()[-500:])
    info = json.loads(r.stdout)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    fps = None
    if v and v.get("avg_frame_rate", "0/0") != "0/0":
        num, den = v["avg_frame_rate"].split("/")
        fps = round(float(num) / float(den), 3)
    filters = ffmpeg_filters()
    model = find_model()
    return {
        "video": video,
        "duration": round(float(info["format"]["duration"]), 2),
        "width": v and v["width"], "height": v and v["height"], "fps": fps,
        "has_audio": a is not None,
        "can_burn_subs": "subtitles" in filters,
        "can_draw_text": "drawtext" in filters,
        "whisper_bin": find_whisper_bin(),
        "whisper_model": str(model) if model else None,
    }


# ---------- transcript ----------

def read_subtitle_file(path):
    text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    segs = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if idx is None:
            continue
        start, end = (parse_ts(x.split()[0]) for x in lines[idx].split("-->"))
        body = " ".join(lines[idx + 1:])
        body = re.sub(r"<[^>]+>", "", body).strip()
        if body:
            segs.append({"start": round(start, 2), "end": round(end, 2), "text": body})
    # YouTube auto-captions repeat rolling lines; drop exact consecutive repeats.
    deduped = []
    for s in segs:
        if deduped and s["text"] == deduped[-1]["text"]:
            deduped[-1]["end"] = s["end"]
        else:
            deduped.append(s)
    return deduped


def whisper_transcribe(video, model, lang, prompt, workdir):
    binary = find_whisper_bin()
    if not binary:
        fail("whisper.cpp not found", hint="brew install whisper-cpp, or pass --srt with a subtitle file")
    if not model:
        fail("no whisper model found", searched=[str(d) for d in MODEL_DIRS],
             hint="download ggml-large-v3-turbo.bin into ~/.cache/whisper.cpp/ or pass --model")
    wav = Path(workdir) / "audio16k.wav"
    log("extracting audio…")
    r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video,
             "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])
    if r.returncode:
        fail("audio extraction failed", stderr=r.stderr.strip()[-500:])
    base = Path(workdir) / "whisper"
    cmd = [binary, "-m", str(model), "-f", str(wav), "-l", lang, "-oj", "-of", str(base), "-np"]
    if prompt:
        cmd += ["--prompt", prompt]
    log(f"transcribing with {Path(model).name} (several minutes for a long video)…")
    r = run(cmd)
    if r.returncode:
        fail("whisper.cpp failed", stderr=r.stderr.strip()[-800:])
    data = json.loads(Path(f"{base}.json").read_text(encoding="utf-8", errors="replace"))
    segs = []
    for item in data.get("transcription", []):
        text = item.get("text", "").strip()
        if text:
            segs.append({"start": round(item["offsets"]["from"] / 1000, 2),
                         "end": round(item["offsets"]["to"] / 1000, 2), "text": text})
    return segs


def transcribe(video, srt, model, lang, prompt, out):
    require_ffmpeg()
    out_dir = stem_dir(video, out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if srt:
        segs, source = read_subtitle_file(srt), f"subtitle file {srt}"
    else:
        model_path = find_model(model)
        with tempfile.TemporaryDirectory() as tmp:
            segs = whisper_transcribe(video, model_path, lang, prompt, tmp)
        source = f"whisper.cpp {model_path.name}"
    if not segs:
        fail("transcript is empty", source=source)
    for i, s in enumerate(segs, 1):
        s["i"] = i
    (out_dir / "transcript.json").write_text(
        json.dumps({"video": video, "source": source, "segments": segs}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    lines = [f"#{s['i']} [{fmt_ts(s['start'])}–{fmt_ts(s['end'])}] {s['text']}" for s in segs]
    (out_dir / "transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"out_dir": str(out_dir), "source": source, "segments": len(segs),
            "duration_covered": segs[-1]["end"], "transcript_txt": str(out_dir / "transcript.txt")}


# ---------- cut points ----------

def cutpoints(video, out, noise, min_silence, scene):
    require_ffmpeg()
    out_dir = stem_dir(video, out)
    out_dir.mkdir(parents=True, exist_ok=True)
    log("detecting silences…")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", video, "-vn",
             "-af", f"silencedetect=n={noise}dB:d={min_silence}", "-f", "null", "-"])
    silences, start = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            start = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and start is not None:
            end = float(m.group(1))
            silences.append({"start": round(start, 2), "end": round(end, 2), "mid": round((start + end) / 2, 2)})
            start = None
    log("detecting scene changes…")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", video, "-an",
             "-vf", f"scale=320:-2,select='gt(scene,{scene})',showinfo", "-f", "null", "-"])
    scenes = [round(float(m.group(1)), 2) for m in re.finditer(r"pts_time:([\d.]+)", r.stderr)]
    result = {"video": video, "silences": silences, "scene_changes": scenes}
    (out_dir / "cutpoints.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"out_dir": str(out_dir), "silences": len(silences), "scene_changes": len(scenes),
            "file": str(out_dir / "cutpoints.json")}


# ---------- render ----------

def reframe_filter(mode, x, zoom):
    """Filter chain [vin] -> [vout] turning a landscape frame into 1080x1920."""
    if mode == "crop":
        # Keep a 9:16 window of the source; x picks where it sits (0 = left, 1 = right).
        # Quotes keep the comma inside min() from splitting the filter chain.
        return (f"[vin]crop=w='min(iw,ih*{OUT_W}/{OUT_H})':h=ih:x='(iw-ow)*{x}':y=0,"
                f"scale={OUT_W}:{OUT_H}:flags=lanczos,setsar=1[vout]")
    if mode == "blur":
        # Whole frame centred on a blurred, filled copy of itself; zoom > 1 enlarges the
        # foreground and trims its sides, which helps small subjects on wide frames.
        fg_w = int(OUT_W * zoom) // 2 * 2
        fg = f"scale={fg_w}:-2:flags=lanczos"
        if zoom > 1:
            fg += f",crop={OUT_W}:ih:(iw-{OUT_W})*{x}:0"
        return (f"[vin]split[bg0][fg0];"
                f"[bg0]scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=increase,"
                f"crop={OUT_W}:{OUT_H},gblur=sigma=30,eq=brightness=-0.08[bg];"
                f"[fg0]{fg}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[vout]")
    raise ValueError(f"unknown reframe mode: {mode}")


def caption_chunks(text, start, end):
    words = text.split()
    if not words:
        return []
    n = max(1, -(-len(words) // CAPTION_MAX_WORDS))
    per = -(-len(words) // n)
    groups = [words[i:i + per] for i in range(0, len(words), per)]
    total = sum(len(" ".join(g)) for g in groups)
    chunks, t = [], start
    for g in groups:
        dur = (end - start) * len(" ".join(g)) / total
        chunks.append((t, t + dur, " ".join(g)))
        t += dur
    return chunks


def clip_captions(segments, transcript):
    """Captions for a clip made of [(start, end), ...] source ranges, on the clip's own clock."""
    cues, offset = [], 0.0
    for s0, s1 in segments:
        for seg in transcript:
            a, b = max(seg["start"], s0), min(seg["end"], s1)
            # Keep a transcript segment only if most of it falls inside this range.
            if b - a < 0.5 * (seg["end"] - seg["start"]):
                continue
            for c0, c1, txt in caption_chunks(seg["text"], seg["start"], seg["end"]):
                c0, c1 = max(c0, s0), min(c1, s1)
                if c1 - c0 >= 0.15:
                    cues.append((offset + c0 - s0, offset + c1 - s0, txt))
        offset += s1 - s0
    # Avoid flicker: stretch very short cues into the gap that follows.
    out = []
    for i, (a, b, txt) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else offset
        out.append((a, max(b, min(a + CAPTION_MIN_DUR, nxt)), txt))
    return out


def write_srt(cues, path):
    lines = []
    for i, (a, b, txt) in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(a)} --> {srt_ts(b)}", txt, ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def srt_filter_path(path):
    # The subtitles filter parses its argument, so ':' '\' and quotes need escaping.
    return str(path).replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")


def render_clip(clip, plan, source, duration, out_dir, transcript, can_burn, dry_run):
    d = plan.get("defaults", {})
    rf = {**{"mode": "blur", "x": 0.5, "zoom": 1.0}, **d.get("reframe", {}), **clip.get("reframe", {})}
    pad_in = float(clip.get("pad_in", d.get("pad_in", 0.05)))
    pad_out = float(clip.get("pad_out", d.get("pad_out", 0.25)))
    burn = bool(clip.get("burn_subs", d.get("burn_subs", False)))
    loudnorm = bool(clip.get("loudnorm", d.get("loudnorm", True)))

    ranges = []
    for seg in clip["segments"]:
        s0 = max(0.0, parse_ts(str(seg["start"])) - pad_in)
        s1 = min(duration, parse_ts(str(seg["end"])) + pad_out)
        if s1 - s0 < 0.3:
            raise ValueError(f"segment {seg} is too short or outside the video")
        ranges.append((round(s0, 3), round(s1, 3)))
    total = sum(b - a for a, b in ranges)

    name = f"{clip['id']}-{clip.get('slug', 'clip')}"
    mp4, srt = out_dir / f"{name}.mp4", out_dir / f"{name}.srt"
    cues = clip_captions(ranges, transcript) if transcript else []
    if cues:
        write_srt(cues, srt)

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for a, b in ranges:
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(source)]
    parts, fade = [], 0.03
    for i, (a, b) in enumerate(ranges):
        # Tiny fades at every join so stitched segments do not click.
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30[v{i}];"
                     f"[{i}:a]asetpts=PTS-STARTPTS,afade=t=in:d={fade},"
                     f"afade=t=out:st={max(0, b - a - fade):.3f}:d={fade}[a{i}]")
    joined = "".join(f"[v{i}][a{i}]" for i in range(len(ranges)))
    graph = ";".join(parts) + f";{joined}concat=n={len(ranges)}:v=1:a=1[vin][ain];"
    graph += reframe_filter(rf["mode"], float(rf["x"]), float(rf["zoom"]))
    vout = "[vout]"
    if burn and can_burn and cues:
        style = ("FontName=Arial,FontSize=13,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                 "BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=70")
        graph += f";[vout]subtitles='{srt_filter_path(srt.resolve())}':force_style='{style}'[vsub]"
        vout = "[vsub]"
    end_fade = min(0.3, total / 4)
    afilter = f"[ain]afade=t=out:st={total - end_fade:.3f}:d={end_fade:.3f}"
    afilter += ",loudnorm=I=-14:TP=-1.5:LRA=11" if loudnorm else ""
    graph += f";{afilter},aresample=48000[aout]"
    cmd += ["-filter_complex", graph, "-map", vout, "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(mp4)]

    result = {"id": clip["id"], "file": str(mp4), "duration": round(total, 2),
              "segments": ranges, "reframe": rf, "srt": str(srt) if cues else None,
              "subs_burned": bool(burn and can_burn and cues)}
    if burn and not can_burn:
        result["note"] = "this ffmpeg has no subtitles filter; import the .srt in CapCut instead"
    if dry_run:
        result["cmd"] = cmd
        return result
    log(f"rendering {mp4.name} ({total:.1f}s)…")
    r = run(cmd)
    if r.returncode:
        result["error"] = r.stderr.strip()[-800:]
        return result
    result["preview"] = write_preview(mp4, total)
    return result


def write_preview(mp4, duration):
    """First, middle and last frame side by side, for a quick look at the framing."""
    png = mp4.with_suffix(".preview.png")
    times = [min(0.2, duration / 4), duration / 2, max(0.0, duration - 0.5)]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for t in times:
        cmd += ["-ss", f"{t:.3f}", "-i", str(mp4)]
    graph = "".join(f"[{i}:v]trim=end_frame=1,scale=270:-2[p{i}];" for i in range(3))
    graph += "[p0][p1][p2]hstack=3"
    r = run(cmd + ["-filter_complex", graph, "-frames:v", "1", str(png)])
    return None if r.returncode else str(png)


def render(plan_path, only, dry_run):
    require_ffmpeg()
    plan_path = Path(plan_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    # Relative paths in the plan are relative to the folder the script runs from (project root).
    source = Path(plan["source"]).expanduser()
    if not source.is_file():
        fail(f"source video not found: {source}")
    out_dir = Path(plan["out_dir"]).expanduser() if plan.get("out_dir") else plan_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript = []
    if plan.get("transcript"):
        transcript = json.loads(Path(plan["transcript"]).read_text(encoding="utf-8"))["segments"]
    duration = probe(str(source))["duration"]
    can_burn = "subtitles" in ffmpeg_filters()
    wanted = set(only.split(",")) if only else None
    results = []
    for clip in plan["clips"]:
        if wanted and clip["id"] not in wanted:
            continue
        try:
            results.append(render_clip(clip, plan, source, duration, out_dir, transcript, can_burn, dry_run))
        except (KeyError, ValueError) as e:
            results.append({"id": clip.get("id"), "error": f"{type(e).__name__}: {e}"})
    return {"out_dir": str(out_dir), "clips": results,
            "failed": [r["id"] for r in results if "error" in r]}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("probe")
    pr.add_argument("video")
    t = sub.add_parser("transcribe")
    t.add_argument("video")
    t.add_argument("--srt", help="import this .srt/.vtt instead of running whisper.cpp")
    t.add_argument("--model", help="path to a ggml whisper model")
    t.add_argument("--lang", default="vi")
    t.add_argument("--prompt", help="names and terms the speech uses, to steer spelling")
    t.add_argument("--out", help="output folder (default shorts/<video name>)")
    c = sub.add_parser("cutpoints")
    c.add_argument("video")
    c.add_argument("--out")
    c.add_argument("--noise", type=float, default=-35)
    c.add_argument("--min-silence", type=float, default=0.3)
    c.add_argument("--scene", type=float, default=0.3)
    r = sub.add_parser("render")
    r.add_argument("plan")
    r.add_argument("--only", help="comma-separated clip ids")
    r.add_argument("--dry-run", action="store_true", help="print ffmpeg commands without running")
    args = p.parse_args()

    if args.cmd == "probe":
        emit(probe(args.video))
    elif args.cmd == "transcribe":
        emit(transcribe(args.video, args.srt, args.model, args.lang, args.prompt, args.out))
    elif args.cmd == "cutpoints":
        emit(cutpoints(args.video, args.out, args.noise, args.min_silence, args.scene))
    elif args.cmd == "render":
        result = render(args.plan, args.only, args.dry_run)
        emit(result)
        sys.exit(1 if result["failed"] else 0)


if __name__ == "__main__":
    main()
