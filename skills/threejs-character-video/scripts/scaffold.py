#!/usr/bin/env python3
"""Scaffold a Three.js project that renders 3D-character videos (threejs-character-video skill).

Subcommands (compact JSON to stdout, progress to stderr):
  check                         Node/npm/ffmpeg/Chrome versions and what is missing.
  init DIR [--name N] [--format 9:16|16:9|1:1|4:5] [--fps 30] [--no-demo] [--into-existing]
                                Copy the project template into DIR. Unless --no-demo, also
                                download the CC0 RobotExpressive model and synthesise a short
                                Vietnamese demo voice (macOS `say`, voice Linh) with an .srt.
  demo-voice DIR [--lines "câu 1|câu 2"] [--voice Linh]
                                (Re)generate public/audio/demo.wav + demo.srt in a project.

Standard library only. Never overwrites existing files.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import wave
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template"
FORMATS = {"9:16", "16:9", "1:1", "4:5"}
ROBOT_URL = "https://raw.githubusercontent.com/mrdoob/three.js/r170/examples/models/gltf/RobotExpressive/RobotExpressive.glb"
DEMO_LINES = [
    "Xin chào, mình là Rô bốt, nhân vật ba chiều đầu tiên của dự án này.",
    "Mỗi cảnh được viết bằng một file TypeScript ngắn, bám theo từng câu thoại.",
    "Bạn sửa file, trình duyệt tự tải lại, rồi xuất ra video MP4.",
]
CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def fail(msg, **extra):
    emit({"error": msg, **extra})
    sys.exit(1)


def version_of(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return (out.stdout or out.stderr).strip().splitlines()[0] if out.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, IndexError):
        return None


def cmd_check(_args):
    node = version_of(["node", "--version"])
    npm = version_of(["npm", "--version"])
    ffmpeg = version_of(["ffmpeg", "-version"])
    chrome = os.environ.get("CHROME_PATH") or next((p for p in CHROME_PATHS if Path(p).exists()), None)
    say = shutil.which("say")
    linh = False
    if say:
        voices = subprocess.run([say, "-v", "?"], capture_output=True, text=True).stdout
        linh = bool(re.search(r"^Linh\s", voices, re.M))
    missing, hints = [], []
    node_ok = False
    if node:
        m = re.match(r"v(\d+)\.(\d+)", node)
        major, minor = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        node_ok = (major == 20 and minor >= 19) or (major == 22 and minor >= 12) or major >= 23
    if not node_ok:
        missing.append("node")
        hints.append("Cần Node.js 20.19+ hoặc 22.12+ (Vite 8). macOS: brew install node")
    if not ffmpeg:
        missing.append("ffmpeg")
        hints.append("Cần ffmpeg để ghép khung hình thành MP4. macOS: brew install ffmpeg")
    if not chrome:
        missing.append("chrome")
        hints.append("Cần Chrome/Chromium/Edge để render, hoặc đặt CHROME_PATH")
    emit({
        "node": node, "npm": npm, "ffmpeg": ffmpeg, "chrome": chrome,
        "say": say, "say_vietnamese_voice": linh,
        "missing": missing, "hints": hints, "ok": not missing,
    })


def copy_template(dest: Path, name: str, fmt: str, fps: int, into_existing: bool):
    if dest.exists() and any(dest.iterdir()) and not into_existing:
        fail(f"Thư mục {dest} đã có file", hint="Chọn thư mục mới, hoặc thêm --into-existing để chỉ thêm file còn thiếu (không ghi đè).")
    dest.mkdir(parents=True, exist_ok=True)
    written, skipped = [], []
    replacements = {"__PROJECT_NAME__": name, "__FORMAT__": fmt, "__FPS__": str(fps)}
    for src in sorted(TEMPLATE.rglob("*")):
        if src.is_dir() or src.name == ".DS_Store":
            continue
        rel = src.relative_to(TEMPLATE)
        if rel.name == "gitignore":
            rel = rel.with_name(".gitignore")
        out = dest / rel
        if out.exists():
            skipped.append(str(rel))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in {".json", ".ts", ".html", ".md", ".mjs", ".css"} or rel.name == ".gitignore":
            text = src.read_text(encoding="utf-8")
            for k, v in replacements.items():
                text = text.replace(k, v)
            out.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src, out)
        written.append(str(rel))
    for d in ("public/models", "public/audio", "public/images", "public/anims"):
        (dest / d).mkdir(parents=True, exist_ok=True)
    return written, skipped


def download_robot(dest: Path):
    out = dest / "public" / "models" / "RobotExpressive.glb"
    if out.exists():
        return str(out), None
    log(f"Tải model mẫu: {ROBOT_URL}")
    try:
        with urllib.request.urlopen(ROBOT_URL, timeout=60) as r, open(out, "wb") as f:
            shutil.copyfileobj(r, f)
    except Exception as e:  # noqa: BLE001 - report any network failure as a hint
        if out.exists():
            out.unlink()
        return None, f"Không tải được model mẫu ({e}). Tự tải {ROBOT_URL} về public/models/."
    (dest / "public" / "models" / "CREDITS.md").write_text(
        "# Nguồn model\n\n"
        "- `RobotExpressive.glb`: Tomás Laulhé (Quaternius), chỉnh sửa bởi Don McCurdy. CC0 1.0.\n"
        f"  Lấy từ {ROBOT_URL}\n",
        encoding="utf-8",
    )
    return str(out), None


def srt_stamp(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def make_voice(dest: Path, lines, voice="Linh", lead=0.6, gap=0.45, tail=1.2, rate=22050):
    """One wav per line via `say`, concatenated with gaps; exact timings go into the .srt."""
    audio_dir = dest / "public" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    wav_out, srt_out = audio_dir / "demo.wav", audio_dir / "demo.srt"
    say = shutil.which("say")
    synth = bool(say)
    if say:
        voices = subprocess.run([say, "-v", "?"], capture_output=True, text=True).stdout
        synth = bool(re.search(rf"^{re.escape(voice)}\s", voices, re.M))
    chunks = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, line in enumerate(lines):
            if synth:
                p = Path(tmp) / f"{i}.wav"
                r = subprocess.run([say, "-v", voice, "-o", str(p), "--file-format=WAVE", f"--data-format=LEI16@{rate}", line],
                                   capture_output=True, text=True)
                if r.returncode != 0 or not p.exists():
                    synth = False
                else:
                    with wave.open(str(p)) as w:
                        chunks.append(w.readframes(w.getnframes()))
                    continue
            # No TTS available: silence of a plausible reading length (~4.5 syllables/s).
            chunks.append(b"\x00\x00" * int(rate * max(1.5, len(line.split()) / 4.5)))
    if not synth:
        chunks = [b"\x00\x00" * (len(c) // 2) for c in chunks]
    silence = lambda sec: b"\x00\x00" * int(rate * sec)  # noqa: E731
    pcm, cues, t = bytearray(silence(lead)), [], lead
    for i, (line, c) in enumerate(zip(lines, chunks)):
        dur = len(c) / 2 / rate
        cues.append((i + 1, t, t + dur, line))
        pcm += c
        t += dur
        if i < len(lines) - 1:
            pcm += silence(gap)
            t += gap
    pcm += silence(tail)
    with wave.open(str(wav_out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(pcm))
    srt_out.write_text(
        "\n".join(f"{n}\n{srt_stamp(a)} --> {srt_stamp(b)}\n{txt}\n" for n, a, b, txt in cues),
        encoding="utf-8",
    )
    return {"audio": str(wav_out), "subtitles": str(srt_out), "voiced": synth,
            "duration": round(len(pcm) / 2 / rate, 2)}


def cmd_init(args):
    if args.format not in FORMATS:
        fail(f"format phải là một trong {sorted(FORMATS)}")
    dest = Path(args.dir).expanduser().resolve()
    name = args.name or re.sub(r"[^a-z0-9-]+", "-", dest.name.lower()).strip("-") or "character-video"
    written, skipped = copy_template(dest, name, args.format, args.fps, args.into_existing)
    result = {"project": str(dest), "name": name, "format": args.format, "fps": args.fps,
              "written": len(written), "skipped_existing": skipped, "warnings": []}
    if not args.no_demo:
        model, err = download_robot(dest)
        if err:
            result["warnings"].append(err)
        result["demo_model"] = model
        voice = make_voice(dest, DEMO_LINES)
        if not voice["voiced"]:
            result["warnings"].append("Không có giọng tiếng Việt của macOS `say`; demo dùng audio im lặng (miệng không động).")
        result["demo_voice"] = voice
    else:
        demo = dest / "src" / "episodes" / "demo.ts"
        if demo.exists() and "demo.ts" in " ".join(written):
            demo.unlink()
    result["next"] = [f"cd {dest}", "npm install", "npm run still -- demo --at 1,4,8 --scale 0.5", "npm run dev"]
    emit(result)


def cmd_demo_voice(args):
    dest = Path(args.dir).expanduser().resolve()
    lines = [s.strip() for s in args.lines.split("|")] if args.lines else DEMO_LINES
    emit(make_voice(dest, [s for s in lines if s], voice=args.voice))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    p = sub.add_parser("init")
    p.add_argument("dir")
    p.add_argument("--name")
    p.add_argument("--format", default="9:16")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--no-demo", action="store_true")
    p.add_argument("--into-existing", action="store_true")
    p.set_defaults(fn=cmd_init)
    p = sub.add_parser("demo-voice")
    p.add_argument("dir")
    p.add_argument("--lines")
    p.add_argument("--voice", default="Linh")
    p.set_defaults(fn=cmd_demo_voice)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
