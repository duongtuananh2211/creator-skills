#!/usr/bin/env python3
"""Helper for the youtube-description-writer skill.

Subcommands:
  check FILE [--title T] [--keyword K ...] [--duration D] [--shorts]
                                    Lint a description (plain text or .md): length, the
                                    part shown before "more", keywords, chapters, hashtags,
                                    links, repeated lines, keyword-list lines. JSON out.
  suggest --q SEED [--alphabet] [--no-accent]
                                    YouTube autocomplete (hl=vi, gl=VN). --no-accent also
                                    asks for the seed without diacritics. JSON out.
  transcript FILE [--every 30]      Condense an .srt/.vtt into "[MM:SS] text" blocks of
                                    about N seconds, for writing chapters. Plain text out.
  fetch VIDEO [--subs DIR]          Title, description, duration, chapters, tags of a
                                    published video via yt-dlp (on PATH or through uvx).
                                    --subs DIR also saves its Vietnamese/English captions
                                    as .vtt. JSON out.

D is a duration like 12:34 or 1:02:03. Only the Python standard library is used, plus
yt-dlp for fetch.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

TIMEOUT = 15
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
DESC_MAX = 5000            # official: "a maximum of 5000 characters"
TITLE_MAX = 100
FOLD_MOBILE = 100          # practitioner estimates of what shows before "more"
FOLD_DESKTOP = 157
HASHTAG_IGNORE_OVER = 60   # official: more than 60 and every hashtag is ignored
CHAPTER_MIN_SEC = 10
QUESTION_PREFIXES = ["vì sao", "cách", "có nên"]
SHORTENERS = ("bit.ly", "tinyurl.com", "t.co", "goo.gl", "rb.gy", "cutt.ly", "shorturl.at", "s.id")

TS_LINE = re.compile(r"^\s*[\(\[]?((?:\d{1,2}:)?\d{1,2}:\d{2})[\)\]]?\s*(?:[-–—:|.]\s*)?(.*)$")
HASHTAG = re.compile(r"(?<![\w&/])#(\w+)", re.UNICODE)
URL = re.compile(r"https?://[^\s<>()]+|\bwww\.[^\s<>()]+", re.IGNORECASE)


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def fail(msg, **extra):
    emit({"error": msg, **extra})
    sys.exit(1)


def nfc(text):
    return unicodedata.normalize("NFC", text)


def strip_accents(text):
    text = unicodedata.normalize("NFD", text).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def to_sec(ts):
    parts = [int(p) for p in ts.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def fmt(sec):
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


# ---------- check ----------

def read_description(path):
    text = nfc(Path(path).read_text(encoding="utf-8"))
    # Allow a draft saved as Markdown with the paste-ready text inside one fenced block.
    fence = re.search(r"```[^\n]*\n(.*?)\n```", text, re.S)
    return fence.group(1) if fence else text


def keyword_hits(text, kw):
    low, kw_low = text.lower(), nfc(kw).lower()
    exact = low.count(kw_low)
    loose = strip_accents(low).count(strip_accents(kw_low))
    return exact, loose


def parse_chapters(lines):
    chapters = []
    for i, line in enumerate(lines):
        m = TS_LINE.match(line)
        if m:
            chapters.append({"line": i + 1, "ts": m.group(1), "sec": to_sec(m.group(1)),
                             "label": m.group(2).strip()})
    return chapters


def check_chapters(chapters, duration, issues):
    if not chapters:
        return
    if len(chapters) < 3:
        issues.append(("error", "chapters_too_few",
                       f"Có {len(chapters)} mốc thời gian; cần ít nhất 3 mốc thì YouTube mới tạo chương."))
    if chapters[0]["sec"] != 0:
        issues.append(("error", "chapters_no_zero",
                       f"Mốc đầu tiên là {chapters[0]['ts']}; mốc đầu phải là 00:00."))
    for a, b in zip(chapters, chapters[1:]):
        if b["sec"] <= a["sec"]:
            issues.append(("error", "chapters_order",
                           f"Mốc {b['ts']} (dòng {b['line']}) không lớn hơn mốc trước {a['ts']}."))
        elif b["sec"] - a["sec"] < CHAPTER_MIN_SEC:
            issues.append(("error", "chapter_short",
                           f"Chương '{a['label'] or a['ts']}' chỉ dài {b['sec'] - a['sec']} giây; tối thiểu 10 giây."))
    for c in chapters:
        if not c["label"]:
            issues.append(("warn", "chapter_no_label", f"Mốc {c['ts']} (dòng {c['line']}) chưa có tên chương."))
    if duration is not None:
        last = chapters[-1]
        if last["sec"] >= duration:
            issues.append(("error", "chapter_past_end",
                           f"Mốc {last['ts']} nằm sau độ dài video {fmt(duration)}."))
        elif duration - last["sec"] < CHAPTER_MIN_SEC:
            issues.append(("error", "chapter_short",
                           f"Chương cuối chỉ dài {duration - last['sec']} giây; tối thiểu 10 giây."))
    gaps = [b["sec"] - a["sec"] for a, b in zip(chapters, chapters[1:])]
    if duration is not None and chapters:
        gaps.append(duration - chapters[-1]["sec"])
    if gaps and max(gaps) > 8 * 60:
        issues.append(("info", "chapter_long",
                       f"Có chương dài {fmt(max(gaps))}; cân nhắc tách nếu nội dung đổi ý ở giữa."))


def looks_like_keyword_list(line):
    if re.match(r"^\s*(tags?|từ khoá|từ khóa|keywords?)\s*:", line, re.I):
        return True
    items = [x.strip() for x in re.split(r"[,;|]", line) if x.strip()]
    if len(items) < 6:
        return False
    short = [x for x in items if len(x.split()) <= 4 and not re.search(r"[.!?]", x)]
    return len(short) >= 0.8 * len(items)


def check(args):
    text = read_description(args.file).strip("\n")
    lines = text.splitlines()
    issues = []
    n = len(text)

    if n > DESC_MAX:
        issues.append(("error", "too_long", f"{n} ký tự, vượt giới hạn {DESC_MAX}."))
    if "<" in text or ">" in text:
        issues.append(("error", "angle_brackets",
                       "Có ký tự < hoặc >; YouTube Studio thường không cho lưu mô tả chứa hai ký tự này. Đổi thành → hoặc bỏ."))

    first_line = next((l for l in lines if l.strip()), "")
    flat = re.sub(r"\s+", " ", text).strip()
    fold = flat[:FOLD_DESKTOP]
    if URL.search(first_line) or first_line.lstrip().startswith("#"):
        issues.append(("warn", "fold_wasted", "Dòng đầu là link hoặc hashtag; dòng đầu nên nói video về gì."))
    if TS_LINE.match(first_line):
        issues.append(("warn", "fold_wasted", "Mô tả mở bằng mốc thời gian; nên có 1–2 câu giới thiệu trước danh sách chương."))

    title = nfc(args.title) if args.title else None
    if title:
        if len(title) > TITLE_MAX:
            issues.append(("error", "title_too_long", f"Tiêu đề {len(title)} ký tự, vượt {TITLE_MAX}."))
        if first_line.strip().lower() == title.strip().lower():
            issues.append(("warn", "fold_repeats_title",
                           "Dòng đầu chép nguyên tiêu đề; nên nói thêm điều tiêu đề chưa nói."))

    kw_stats = []
    for kw in args.keyword or []:
        exact, loose = keyword_hits(flat, kw)
        in_fold = keyword_hits(flat[:FOLD_DESKTOP], kw)
        in_title = keyword_hits(title, kw)[1] > 0 if title else None
        kw_stats.append({"keyword": kw, "count": exact, "count_ignoring_accents": loose,
                         "in_fold": in_fold[0] > 0, "in_title": in_title})
        if loose == 0:
            issues.append(("warn", "keyword_missing", f"Không thấy từ khoá '{kw}' trong mô tả."))
        elif exact == 0:
            issues.append(("warn", "keyword_accent", f"'{kw}' chỉ xuất hiện ở dạng khác dấu; kiểm tra chính tả."))
        elif not in_fold[1]:
            issues.append(("info", "keyword_late", f"'{kw}' không nằm trong khoảng {FOLD_DESKTOP} ký tự đầu."))
        if in_title is False:
            issues.append(("info", "keyword_not_in_title", f"'{kw}' không có trong tiêu đề."))
        if exact > 6:
            issues.append(("warn", "keyword_repeated",
                           f"'{kw}' lặp {exact} lần; đọc lại xem có gượng không, lặp nhiều không giúp gì thêm."))

    seen, repeated = {}, []
    for i, line in enumerate(lines):
        key = re.sub(r"\s+", " ", line).strip().lower()
        if len(key) < 12 or TS_LINE.match(line) or not re.search(r"\w", key):
            continue
        if key in seen:
            repeated.append({"line": i + 1, "same_as_line": seen[key], "text": line.strip()[:80]})
        else:
            seen[key] = i + 1
    if repeated:
        issues.append(("warn", "repeated_lines",
                       f"{len(repeated)} dòng lặp lại nguyên văn; chính sách hashtag của YouTube cấm câu lặp lại trong mô tả."))

    kw_lines = [{"line": i + 1, "text": l.strip()[:80]} for i, l in enumerate(lines) if looks_like_keyword_list(l)]
    if kw_lines:
        issues.append(("error", "keyword_list",
                       "Có dòng trông như danh sách từ khoá; nhồi tag/từ khoá vào mô tả vi phạm chính sách spam của YouTube."))

    tags = [nfc(t) for t in HASHTAG.findall(text)]
    if len(tags) > HASHTAG_IGNORE_OVER:
        issues.append(("error", "hashtags_ignored", f"{len(tags)} hashtag (> {HASHTAG_IGNORE_OVER}): YouTube bỏ qua toàn bộ."))
    elif len(tags) > 15:
        issues.append(("warn", "hashtags_many", f"{len(tags)} hashtag; càng nhiều càng kém liên quan, thường 3–5 là đủ."))
    dupes = sorted({t for t in tags if tags.count(t) > 1})
    if dupes:
        issues.append(("info", "hashtags_duplicate", "Hashtag trùng: " + ", ".join("#" + t for t in dupes)))
    if re.search(r"(^|\s)#\s+\w", text):
        issues.append(("warn", "hashtag_space", "Có dấu # đứng tách khỏi chữ; hashtag không được có khoảng trắng."))

    urls = URL.findall(text)
    short = [u for u in urls if any(s in u.lower() for s in SHORTENERS)]
    if short:
        issues.append(("info", "short_links", "Link rút gọn che đích đến; dùng link đầy đủ nếu được: " + ", ".join(short)))
    if args.shorts and urls:
        issues.append(("info", "shorts_links",
                       "Link trong mô tả Shorts không bấm được; dùng 'Video liên quan' hoặc link trên trang kênh."))

    duration = to_sec(args.duration) if args.duration else None
    chapters = parse_chapters(lines)
    check_chapters(chapters, duration, issues)
    if not chapters and not args.shorts and duration and duration >= 5 * 60:
        issues.append(("info", "no_chapters", "Video dài từ 5 phút mà chưa có chương."))

    order = {"error": 0, "warn": 1, "info": 2}
    issues.sort(key=lambda x: order[x[0]])
    emit({
        "chars": n,
        "limit": DESC_MAX,
        "words": len(flat.split()),
        "lines": len(lines),
        "fold_preview": {"mobile_~100": flat[:FOLD_MOBILE], "desktop_~157": fold},
        "keywords": kw_stats,
        "hashtags": {"count": len(tags), "first_three": ["#" + t for t in tags[:3]], "all": ["#" + t for t in tags]},
        "chapters": [{"ts": c["ts"], "label": c["label"]} for c in chapters],
        "links": urls,
        "repeated_lines": repeated,
        "keyword_list_lines": kw_lines,
        "issues": [{"level": lv, "code": code, "msg": msg} for lv, code, msg in issues],
    })


# ---------- suggest ----------

def suggest_once(q):
    params = {"client": "firefox", "ds": "yt", "hl": "vi", "gl": "VN", "q": q}
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "vi-VN,vi;q=0.9"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace"))
    return data[1] if len(data) > 1 else []


def suggest(args):
    q = nfc(args.q.strip())
    queries = [q]
    if args.no_accent and strip_accents(q) != q:
        queries.append(strip_accents(q))
    if args.alphabet:
        if not any(q.lower().startswith(w) for w in QUESTION_PREFIXES + ["tại sao", "sao"]):
            queries += [f"{w} {q}" for w in QUESTION_PREFIXES]
            queries.append(f"{q} là gì")
        queries += [f"{q} {c}" for c in "abcdeghiklmnopqrstuvxy"]
        queries = queries[:30]  # stay polite to an unofficial endpoint
    results, errors = {}, {}
    for i, query in enumerate(queries):
        if i:
            time.sleep(0.25)
        try:
            results[query] = suggest_once(query)
        except Exception as e:
            errors[query] = f"{type(e).__name__}: {e}"
    if not results:
        fail(next(iter(errors.values()), "no results"), q=q)
    unique = list(dict.fromkeys(nfc(s) for lst in results.values() for s in lst))
    out = {"q": q, "requests": len(queries), "count": len(unique), "suggestions": unique}
    if errors:
        out["errors"] = errors
    emit(out)


# ---------- transcript ----------

CUE_TIME = re.compile(r"((?:\d+:)?\d{1,2}:\d{2})[.,](\d{1,3})\s*-->\s*")


def parse_cues(path):
    raw = nfc(Path(path).read_text(encoding="utf-8", errors="replace"))
    cues = []
    for block in re.split(r"\n\s*\n", raw.replace("\r\n", "\n")):
        lines = block.strip().splitlines()
        idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if idx is None:
            continue
        m = CUE_TIME.search(lines[idx])
        if not m:
            continue
        text_lines = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", l)).strip() for l in lines[idx + 1:]]
        text_lines = [l for l in text_lines if l]
        if text_lines:
            cues.append((to_sec(m.group(1)), text_lines))
    return cues


def transcript(args):
    cues = parse_cues(args.file)
    if not cues:
        fail("no cues found", file=args.file)
    out, start, buf, recent = [], None, [], []
    for sec, text_lines in cues:
        # YouTube auto captions scroll: each cue repeats the line before it, so keep
        # only lines not seen in the last few cues.
        new = [l for l in text_lines if l not in recent]
        recent = (recent + new)[-4:]
        if start is None:
            start = sec
        if sec - start >= args.every and buf:
            out.append(f"[{fmt(start)}] " + " ".join(buf))
            start, buf = sec, []
        buf.extend(new)
    if buf:
        out.append(f"[{fmt(start)}] " + " ".join(buf))
    print(f"# {Path(args.file).name}: {len(cues)} cues, ends ~{fmt(cues[-1][0])}")
    print("\n".join(out))


# ---------- fetch ----------

def ytdlp_cmd():
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uvx"):
        return ["uvx", "yt-dlp"]
    fail("missing yt-dlp", hint="brew install yt-dlp (hoặc pipx install yt-dlp, hoặc cài uv để chạy qua uvx)")


def fetch(args):
    video = args.video if args.video.startswith("http") else f"https://www.youtube.com/watch?v={args.video}"
    res = subprocess.run(ytdlp_cmd() + ["-J", "--no-warnings", "--skip-download", video],
                         capture_output=True, text=True)
    if res.returncode != 0:
        fail("yt-dlp failed", detail=(res.stderr.strip().splitlines()[-1:] or [""])[0])
    info = json.loads(res.stdout)
    out = {
        "id": info.get("id"),
        "title": info.get("title"),
        "channel": info.get("channel"),
        "upload_date": info.get("upload_date"),
        "duration": fmt(info["duration"]) if info.get("duration") else None,
        "views": info.get("view_count"),
        "tags": info.get("tags") or [],
        "chapters": [{"ts": fmt(c["start_time"]), "label": c.get("title")} for c in info.get("chapters") or []],
        "description": info.get("description") or "",
        "caption_langs": sorted(set((info.get("subtitles") or {}).keys())),
        "auto_caption_has_vi": "vi" in (info.get("automatic_captions") or {}),
    }
    if args.subs:
        Path(args.subs).mkdir(parents=True, exist_ok=True)
        cmd = ytdlp_cmd() + ["--skip-download", "--no-warnings", "--write-subs", "--write-auto-subs",
                             "--sub-langs", "vi,vi-orig,en", "--sub-format", "vtt",
                             "-o", str(Path(args.subs) / "%(id)s.%(ext)s"), video]
        subprocess.run(cmd, capture_output=True, text=True)
        out["subs_files"] = sorted(str(p) for p in Path(args.subs).glob(f"{info.get('id')}*.vtt"))
    emit(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--title")
    c.add_argument("--keyword", action="append", help="main keyword; repeat for more")
    c.add_argument("--duration", help="video length, e.g. 12:34")
    c.add_argument("--shorts", action="store_true")
    s = sub.add_parser("suggest")
    s.add_argument("--q", required=True)
    s.add_argument("--alphabet", action="store_true", help="also expand with question words and letters")
    s.add_argument("--no-accent", action="store_true", help="also query the seed without diacritics")
    t = sub.add_parser("transcript")
    t.add_argument("file")
    t.add_argument("--every", type=int, default=30, help="seconds per block (default 30)")
    f = sub.add_parser("fetch")
    f.add_argument("video", help="URL or video id")
    f.add_argument("--subs", help="directory to save captions (.vtt)")
    args = p.parse_args()
    {"check": check, "suggest": suggest, "transcript": transcript, "fetch": fetch}[args.cmd](args)


if __name__ == "__main__":
    main()
