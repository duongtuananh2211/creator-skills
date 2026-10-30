#!/usr/bin/env python3
"""Helper for the thumbnail-designer skill: gather reference thumbnails and preview candidates.

Subcommands (each prints compact JSON to stdout, progress goes to stderr):
  channel CHANNEL [--limit 60] [--top 8] [--skip-newest 2] [--source internal|model|…]
          [--download DIR]
                                    A channel's long videos ranked by outlier score
                                    (views / median views of the channel). CHANNEL is a
                                    @handle or a channel URL.
  search QUERY [--limit 20] [--outlier] [--max-channels 8] [--top 8] [--download DIR]
                                    YouTube search results; --outlier also fetches each
                                    channel's recent videos to score results against the
                                    channel's own median.
  fetch VIDEO... --download DIR     Thumbnails of specific videos (URLs or ids), e.g. the
                                    user's bookmarks.
  sheet DIR [--cols 4] [--highlight IMAGE] [--out FILE]
                                    One contact sheet of every image in DIR, row-major in
                                    filename order, written next to DIR (not inside it). --highlight inserts IMAGE second with a
                                    red frame, to see a candidate among competitors.
  check IMAGE [--out FILE]          Preview sheet for one candidate: full size, TV view (only
                                    the top half visible), phone sizes, grayscale, and the
                                    duration badge corner.

Downloads go to DIR/<source>-<views>-<id>.jpg plus DIR/refs.json with titles, channels,
views and scores. Needs ffmpeg on PATH; YouTube data needs yt-dlp (on PATH, or run through
uvx). Nothing else outside the Python standard library is used.
"""
import argparse
import json
import shutil
import statistics
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

THUMB_NAMES = ["maxresdefault.jpg", "hq720.jpg", "hqdefault.jpg"]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
SHORTS_MAX_SEC = 70
GENERATED = {"contact-sheet", "feed-check"}
TILE_W, TILE_H = 480, 270
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def fail(msg, **extra):
    emit({"error": msg, **extra})
    sys.exit(1)


def require_ffmpeg():
    if not shutil.which("ffmpeg"):
        fail("missing ffmpeg", hint="brew install ffmpeg")


def ytdlp_cmd():
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uvx"):
        return ["uvx", "yt-dlp"]
    fail("missing yt-dlp", hint="brew install yt-dlp (hoặc pipx install yt-dlp, hoặc cài uv để chạy qua uvx)")


def ytdlp_flat(url, limit, fatal=True):
    cmd = ytdlp_cmd() + ["--flat-playlist", "-J", "--no-warnings", "--playlist-end", str(limit), url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        err = (res.stderr.strip().splitlines()[-1:] or ["unknown error"])[0]
        if not fatal:
            log(f"skipped {url}: {err}")
            return None
        hint = "YouTube đang giới hạn (429), đợi vài phút rồi chạy lại" if "429" in res.stderr else None
        fail(f"yt-dlp failed for {url}: {err}", hint=hint)
    return json.loads(res.stdout)


def channel_videos_url(channel):
    channel = channel.strip().rstrip("/")
    if channel.startswith("@"):
        return f"https://www.youtube.com/{channel}/videos"
    if not channel.startswith("http"):
        channel = "https://www.youtube.com/" + channel
    if channel.endswith(("/videos", "/featured", "/shorts", "/streams")):
        channel = channel.rsplit("/", 1)[0]
    return channel + "/videos"


def age_days(entry, now):
    ts = entry.get("timestamp") or entry.get("release_timestamp")
    return round((now - ts) / 86400, 1) if ts else None


def video_row(entry, source, now):
    return {
        "id": entry["id"],
        "title": entry.get("title"),
        "channel": entry.get("channel") or entry.get("uploader"),
        "channel_id": entry.get("channel_id"),
        "views": entry.get("view_count"),
        "duration": entry.get("duration"),
        "age_days": age_days(entry, now),
        "url": f"https://www.youtube.com/watch?v={entry['id']}",
        "source": source,
    }


def is_mature(row, index, min_age, skip_newest):
    # Channel tabs list newest first; flat listings often lack upload dates, so the newest
    # few uploads stand in for "too young to have their views yet".
    if row["age_days"] is not None:
        return row["age_days"] >= min_age
    return index >= skip_newest


def score_against_median(rows, min_age, skip_newest=0):
    """Attach outlier = views / median of mature videos; young videos are not scored."""
    flags = [bool(r["views"]) and is_mature(r, i, min_age, skip_newest) for i, r in enumerate(rows)]
    mature = [r for r, ok in zip(rows, flags) if ok]
    if len(mature) < 3:
        return None
    median = statistics.median(r["views"] for r in mature)
    for r, ok in zip(rows, flags):
        r["outlier"] = round(r["views"] / median, 2) if ok and median else None
    return median


def fetch_thumb(video_id, dest):
    for name in THUMB_NAMES:
        req = urllib.request.Request(f"https://i.ytimg.com/vi/{video_id}/{name}", headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
        except Exception:
            continue
        # maxresdefault 404s for old/small uploads; tiny placeholder images also mean "missing".
        if len(data) > 2000:
            dest.write_bytes(data)
            return True
    return False


def download(rows, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    meta_path = out / "refs.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
    known = {m["id"] for m in meta}
    for r in rows:
        name = f"{r['source']}-{r['views'] or 0:010d}-{r['id']}.jpg"
        dest = out / name
        if r["id"] not in known and fetch_thumb(r["id"], dest):
            r["file"] = str(dest)
            meta.append(r)
            known.add(r["id"])
        elif r["id"] in known:
            r["file"] = next((m.get("file") for m in meta if m["id"] == r["id"]), None)
        else:
            r["file"] = None
            log(f"no thumbnail for {r['id']}")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    return str(meta_path)


def cmd_channel(a):
    now = time.time()
    data = ytdlp_flat(channel_videos_url(a.channel), a.limit)
    rows = [video_row(e, a.source, now) for e in data.get("entries") or [] if e.get("id")]
    for r in rows:
        r["channel"] = r["channel"] or data.get("channel")
        r["channel_id"] = r["channel_id"] or data.get("channel_id")
    median = score_against_median(rows, a.min_age_days, a.skip_newest)
    if median is None:
        fail("not enough mature videos to compute a median", videos=len(rows))
    ranked = sorted((r for r in rows if r["outlier"] is not None), key=lambda r: r["outlier"], reverse=True)
    top = ranked[: a.top]
    result = {
        "channel": data.get("channel"),
        "subscribers": data.get("channel_follower_count"),
        "videos_scanned": len(rows),
        "median_views": int(median),
        "too_new_to_score": [r["title"] for r in rows if r["outlier"] is None],
        "top": top,
    }
    if a.download:
        result["refs"] = download(top, a.download)
    emit(result)


def cmd_search(a):
    now = time.time()
    data = ytdlp_flat(f"ytsearch{a.limit}:{a.query}", a.limit)
    rows = [video_row(e, "search", now) for e in data.get("entries") or [] if e.get("id")]
    if not a.include_shorts:
        rows = [r for r in rows if not (r["duration"] and r["duration"] <= SHORTS_MAX_SEC)]
    if a.outlier:
        channels = []
        for r in rows:
            if r["channel_id"] and r["channel_id"] not in channels:
                channels.append(r["channel_id"])
        medians = {}
        for cid in channels[: a.max_channels]:
            log(f"scanning channel {cid}")
            ch = ytdlp_flat(f"https://www.youtube.com/channel/{cid}/videos", 30, fatal=False) or {}
            ch_rows = [video_row(e, "channel", now) for e in ch.get("entries") or [] if e.get("id")]
            medians[cid] = score_against_median(ch_rows, a.min_age_days, 2)
            time.sleep(1)
        for r in rows:
            med = medians.get(r["channel_id"])
            r["channel_median"] = int(med) if med else None
            r["outlier"] = round(r["views"] / med, 2) if med and r["views"] else None
        rows.sort(key=lambda r: r["outlier"] or 0, reverse=True)
    else:
        rows.sort(key=lambda r: r["views"] or 0, reverse=True)
    top = rows[: a.top]
    result = {"query": a.query, "results": len(rows), "top": top}
    if a.download:
        result["refs"] = download(top, a.download)
    emit(result)


def video_id(value):
    """Id from a bare id, watch?v=, youtu.be/, /shorts/ or /live/ link."""
    u = urllib.parse.urlparse(value.strip())
    if not u.netloc:
        return value.strip()
    query = urllib.parse.parse_qs(u.query)
    if "v" in query:
        return query["v"][0]
    return u.path.rstrip("/").split("/")[-1]


def cmd_fetch(a):
    rows = []
    for v in a.videos:
        vid = video_id(v)
        rows.append({"id": vid, "title": None, "channel": None, "views": None,
                     "url": f"https://www.youtube.com/watch?v={vid}", "source": a.source})
    emit({"refs": download(rows, a.download), "fetched": [r for r in rows if r.get("file")]})


def ffmpeg(args):
    res = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + args,
                         capture_output=True, text=True)
    if res.returncode != 0:
        fail("ffmpeg failed", detail=res.stderr.strip()[-600:])


def fit(label, w=TILE_W, h=TILE_H):
    return (f"[{label}]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")


def cmd_sheet(a):
    require_ffmpeg()
    folder = Path(a.dir)
    images = sorted(p for p in folder.iterdir()
                    if p.suffix.lower() in IMAGE_EXTS and p.stem not in GENERATED and not p.stem.endswith("-check"))
    if a.highlight:
        hl = Path(a.highlight).resolve()
        images = [p for p in images if p.resolve() != hl]
        images.insert(min(1, len(images)), hl)
    if not images:
        fail(f"no images in {folder}")
    cols = max(1, min(a.cols, len(images)))
    rows = -(-len(images) // cols)
    inputs, chains = [], []
    for i, p in enumerate(images):
        inputs += ["-i", str(p)]
        chain = fit(f"{i}:v")
        if a.highlight and p.resolve() == Path(a.highlight).resolve():
            chain += ",drawbox=x=0:y=0:w=iw:h=ih:color=red:t=10"
        chains.append(f"{chain},pad=iw+8:ih+8:4:4:color=white[t{i}]")
    # Blank tiles fill the last row so xstack gets a full grid.
    for i in range(len(images), rows * cols):
        chains.append(f"color=c=white:s={TILE_W + 8}x{TILE_H + 8}:d=1[t{i}]")
    layout = "|".join(f"{(i % cols) * (TILE_W + 8)}_{(i // cols) * (TILE_H + 8)}" for i in range(rows * cols))
    stack = "".join(f"[t{i}]" for i in range(rows * cols))
    graph = ";".join(chains) + f";{stack}xstack=inputs={rows * cols}:layout={layout}[out]"
    # Written next to refs/, not inside it, so a later sheet does not pick it up as a reference.
    out = a.out or str(folder.resolve().parent / ("feed-check.jpg" if a.highlight else "contact-sheet.jpg"))
    if rows * cols == 1:
        graph = chains[0].replace("[t0]", "[out]")
    ffmpeg(inputs + ["-filter_complex", graph, "-map", "[out]", "-frames:v", "1", "-q:v", "3", out])
    emit({"sheet": out, "order": [p.name for p in images], "cols": cols})


def cmd_check(a):
    require_ffmpeg()
    img = Path(a.image)
    if not img.exists():
        fail(f"not found: {img}")
    out = a.out or str(img.with_name(img.stem + "-check.jpg"))
    W, H = 960, 540
    graph = ";".join([
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,split=4[a][b][c][d]",
        # TV home/suggested rows show roughly the top half until the viewer presses down.
        f"[b]drawbox=x=0:y=ih/2:w=iw:h=ih/2:color=0x202020@0.92:t=fill[tv]",
        # Duration badge and progress bar sit in the bottom-right / along the bottom.
        f"[c]drawbox=x=iw-150:y=ih-62:w=128:h=44:color=black@0.85:t=fill,"
        f"drawbox=x=0:y=ih-10:w=iw*0.6:h=10:color=red@0.9:t=fill[badge]",
        f"[d]format=gray,format=yuv420p[gray]",
        f"[a]split=3[full][m1][m2]",
        # Phone home feed is roughly full width; sidebar and search lists are tiny.
        f"[m1]scale=246:138[s1]",
        f"[m2]scale=168:94[s2]",
        f"color=c=white:s={W}x240:d=1[bg]",
        f"[bg][s1]overlay=60:50[bg1]",
        f"[bg1][s2]overlay=380:72[small]",
        f"[full][tv]hstack[r1]",
        f"[badge][gray]hstack[r2]",
        f"[small]pad={W * 2}:240:0:0:color=white[r3]",
        f"[r1][r2][r3]vstack=inputs=3[out]",
    ])
    ffmpeg(["-i", str(img), "-filter_complex", graph, "-map", "[out]", "-frames:v", "1", "-q:v", "3", out])
    emit({
        "sheet": out,
        "panels": {
            "row1_left": "full size",
            "row1_right": "TV view: only the top half visible",
            "row2_left": "duration badge + progress bar overlay",
            "row2_right": "grayscale (contrast without colour)",
            "row3": "phone sizes 246x138 and 168x94 at real pixel size",
        },
    })


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("channel")
    c.add_argument("channel")
    c.add_argument("--limit", type=int, default=60)
    c.add_argument("--top", type=int, default=8)
    c.add_argument("--min-age-days", type=float, default=7)
    c.add_argument("--skip-newest", type=int, default=2, help="unscored newest uploads when dates are missing")
    c.add_argument("--source", default="channel", help="file label: internal (own channel), model, external…")
    c.add_argument("--download")
    c.set_defaults(func=cmd_channel)

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--top", type=int, default=8)
    s.add_argument("--outlier", action="store_true")
    s.add_argument("--max-channels", type=int, default=8)
    s.add_argument("--min-age-days", type=float, default=7)
    s.add_argument("--include-shorts", action="store_true")
    s.add_argument("--download")
    s.set_defaults(func=cmd_search)

    f = sub.add_parser("fetch")
    f.add_argument("videos", nargs="+")
    f.add_argument("--download", required=True)
    f.add_argument("--source", default="bookmark")
    f.set_defaults(func=cmd_fetch)

    sh = sub.add_parser("sheet")
    sh.add_argument("dir")
    sh.add_argument("--cols", type=int, default=4)
    sh.add_argument("--highlight")
    sh.add_argument("--out")
    sh.set_defaults(func=cmd_sheet)

    ck = sub.add_parser("check")
    ck.add_argument("image")
    ck.add_argument("--out")
    ck.set_defaults(func=cmd_check)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
