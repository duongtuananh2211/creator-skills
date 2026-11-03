#!/usr/bin/env python3
"""Helper for the keyword-research skill.

Subcommands:
  expand --seed S [--seed S2 ...] [--platform yt,google,tiktok] [--alphabet] [--no-accent]
                                    Autocomplete from YouTube, Google and TikTok (Vietnam).
                                    --alphabet also tries question words and "seed + letter".
                                    Merges duplicates and records, for every suggestion,
                                    which platform returned it and at what best rank. JSON out.
  serp --q Q [--q Q2 ...] [--limit 20]
                                    First page of YouTube search (gl=VN, hl=vi): title,
                                    channel, views, age, length per video, plus a summary
                                    (how many titles match the phrase, how many are under a
                                    year old, median views, distinct channels). JSON out.
  links --q Q [--q Q2 ...]          Links the user opens by hand: Google Trends with the
                                    YouTube Search filter, YouTube and TikTok search pages.

Only the Python standard library is used. All endpoints are public but unofficial; they can
change or block without notice, and none of them returns search volume.
"""
import argparse
import json
import re
import statistics
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

TIMEOUT = 15
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
PAUSE = 0.3                # between calls to the same endpoint
MAX_QUERIES = 30           # per seed per platform, stay polite
PREFIXES = ["cách", "vì sao", "có nên"]
SUFFIXES = ["là gì", "cho người mới", "nào tốt", "bao nhiêu"]
LETTERS = "abcdeghiklmnopqrstuvxy"
QUESTION_START = tuple(PREFIXES + ["tại sao", "sao", "làm sao", "làm thế nào"])
QUESTION_WORDS = ["cach", "vi sao", "tai sao", "lam sao", "the nao", "co nen", "la gi", "bao nhieu",
                  "o dau", "khi nao", "co tot khong", "co nen khong", "nhu nao"]
PLATFORMS = ("yt", "google", "tiktok")


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


def norm(text):
    """Lowercase, no diacritics, single spaces: for matching only."""
    return re.sub(r"\s+", " ", strip_accents(nfc(text)).lower()).strip()


def get(url, accept_json=True):
    headers = {"User-Agent": UA, "Accept-Language": "vi-VN,vi;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        body = resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
    return json.loads(body) if accept_json else body


# ---------- expand ----------

def suggest_google(q, yt=False):
    params = {"client": "firefox", "hl": "vi", "gl": "VN", "q": q}
    if yt:
        params["ds"] = "yt"
    data = get("https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(params))
    return data[1] if len(data) > 1 else []


def suggest_tiktok(q):
    params = {"keyword": q, "aid": "1988", "region": "VN", "lang": "vi"}
    data = get("https://www.tiktok.com/api/search/general/sug/?" + urllib.parse.urlencode(params))
    return [s["content"] for s in data.get("sug_list") or [] if s.get("content")]


FETCHERS = {
    "yt": lambda q: suggest_google(q, yt=True),
    "google": lambda q: suggest_google(q),
    "tiktok": suggest_tiktok,
}


def queries_for(seed, alphabet, no_accent):
    qs = [seed]
    if no_accent and strip_accents(seed) != seed:
        qs.append(strip_accents(seed))
    if alphabet:
        if not seed.lower().startswith(QUESTION_START):
            qs += [f"{w} {seed}" for w in PREFIXES]
        qs += [f"{seed} {w}" for w in SUFFIXES]
        qs += [f"{seed} {c}" for c in LETTERS]
    return qs[:MAX_QUERIES]


def expand(args):
    platforms = [p.strip() for p in args.platform.split(",") if p.strip()]
    bad = [p for p in platforms if p not in PLATFORMS]
    if bad:
        fail(f"unknown platform: {', '.join(bad)}", allowed=list(PLATFORMS))
    seeds = [nfc(s.strip()) for s in args.seed if s.strip()]
    found = {}          # norm -> {"text", "sources": {platform: best rank}, "from": set(queries)}
    calls, errors, empty = 0, {}, {}
    for platform in platforms:
        dead = 0
        for seed in seeds:
            for q in queries_for(seed, args.alphabet, args.no_accent):
                if dead >= 3:   # endpoint is blocking or down, stop hammering it
                    break
                if calls:
                    time.sleep(PAUSE)
                calls += 1
                try:
                    items = FETCHERS[platform](q)
                    dead = 0
                except Exception as e:
                    errors.setdefault(platform, {})[q] = f"{type(e).__name__}: {e}"
                    dead += 1
                    continue
                if not items and q == seed:
                    empty.setdefault(platform, []).append(seed)
                for rank, text in enumerate(items, 1):
                    text = nfc(text.strip())
                    key = norm(text)
                    if not key:
                        continue
                    entry = found.setdefault(key, {"text": text, "sources": {}, "from": set()})
                    # prefer the accented spelling when both exist
                    if strip_accents(entry["text"]) == entry["text"] and strip_accents(text) != text:
                        entry["text"] = text
                    best = entry["sources"].get(platform)
                    entry["sources"][platform] = rank if best is None else min(best, rank)
                    entry["from"].add(q)
    rows = []
    for e in found.values():
        key = norm(e["text"])
        rows.append({
            "kw": e["text"],
            "platforms": len(e["sources"]),
            "best_rank": min(e["sources"].values()),
            "sources": e["sources"],
            "hits": len(e["from"]),
            "question": any(re.search(rf"\b{w}\b", key) for w in QUESTION_WORDS),
        })
    rows.sort(key=lambda r: (-r["platforms"], -r["hits"], r["best_rank"], r["kw"]))
    out = {
        "seeds": seeds,
        "platforms": platforms,
        "requests": calls,
        "count": len(rows),
        "on_all_platforms": sum(r["platforms"] == len(platforms) for r in rows) if len(platforms) > 1 else None,
        "keywords": rows[: args.limit] if args.limit else rows,
    }
    if empty:
        # A platform answering with nothing for the bare seed: often the topic is suppressed
        # there (TikTok does this for gambling), sometimes just too rare.
        out["empty_seed"] = empty
    if errors:
        out["errors"] = {p: dict(list(v.items())[:3]) for p, v in errors.items()}
        out["failed_platforms"] = [p for p in platforms if p in errors and
                                   not any(p in r["sources"] for r in rows)]
    emit(out)
    if not rows:
        sys.exit(1)


# ---------- serp ----------

AGE_UNITS = [("giây", 1 / 86400), ("phút", 1 / 1440), ("giờ", 1 / 24), ("ngày", 1), ("tuần", 7),
             ("tháng", 30), ("năm", 365),
             ("second", 1 / 86400), ("minute", 1 / 1440), ("hour", 1 / 24), ("day", 1), ("week", 7),
             ("month", 30), ("year", 365)]


def text_of(node):
    if not node:
        return ""
    if "simpleText" in node:
        return node["simpleText"]
    return "".join(r.get("text", "") for r in node.get("runs", []))


def age_days(published):
    """'3 tháng trước', 'Đã phát trực tiếp 2 năm trước', '5 days ago' -> days (approximate)."""
    m = re.search(r"(\d+)\s*([^\d\s]+)", published or "")
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2).lower()
    for name, days in AGE_UNITS:
        if unit.startswith(name):
            return round(n * days, 2)
    return None


def to_int(views):
    digits = re.sub(r"[^\d]", "", views or "")
    return int(digits) if digits else None


def walk(node, key):
    if isinstance(node, dict):
        if key in node:
            yield node[key]
        for v in node.values():
            yield from walk(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)


def serp_one(q, limit):
    params = {"search_query": q, "gl": "VN", "hl": "vi"}
    html = get("https://www.youtube.com/results?" + urllib.parse.urlencode(params), accept_json=False)
    m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});\s*</script>", html, re.S)
    if not m:
        raise ValueError("ytInitialData not found (YouTube changed the page or showed a consent wall)")
    data = json.loads(m.group(1))
    videos = []
    for v in walk(data, "videoRenderer"):
        if not v.get("videoId") or any(x["id"] == v["videoId"] for x in videos):
            continue
        published = text_of(v.get("publishedTimeText"))
        videos.append({
            "id": v["videoId"],
            "title": text_of(v.get("title")),
            "channel": text_of(v.get("ownerText")),
            "views": to_int(text_of(v.get("viewCountText"))),
            "published": published,
            "age_days": age_days(published),
            "length": text_of(v.get("lengthText")),
        })
        if len(videos) >= limit:
            break
    shorts = sum(1 for _ in walk(data, "shortsLockupViewModel"))
    words = norm(q).split()
    for v in videos:
        t = norm(v["title"])
        tokens = set(re.findall(r"\w+", t))
        share = sum(w in tokens for w in words) / len(words) if words else 0
        v["match"] = ("exact" if norm(q) in t else "all_words" if share == 1
                      else "most_words" if share >= 0.6 else "partial")
    views = [v["views"] for v in videos if v["views"] is not None]
    ages = [v["age_days"] for v in videos if v["age_days"] is not None]
    # "1 năm trước" means 12-23 months, so the cut-offs are strict
    recent = [v for v in videos if v["age_days"] is not None and v["age_days"] < 365]
    summary = {
        "results": len(videos),
        "title_exact": sum(v["match"] == "exact" for v in videos),
        "title_all_words": sum(v["match"] in ("exact", "all_words") for v in videos),
        "title_most_words": sum(v["match"] != "partial" for v in videos),
        "under_1y": len(recent),
        "under_90d": sum(v["age_days"] is not None and v["age_days"] < 90 for v in videos),
        "median_age_days": round(statistics.median(ages)) if ages else None,
        "median_views": round(statistics.median(views)) if views else None,
        "max_views": max(views) if views else None,
        "median_views_under_1y": round(statistics.median([v["views"] for v in recent if v["views"] is not None]))
                                 if any(v["views"] is not None for v in recent) else None,
        "distinct_channels": len({v["channel"] for v in videos if v["channel"]}),
        "top_channel_share": max((sum(v["channel"] == c for v in videos) for c in {v["channel"] for v in videos}),
                                 default=0),
        "shorts_on_page": shorts,
    }
    return {"q": q, "summary": summary, "videos": videos}


def serp(args):
    out, errors = [], {}
    for i, q in enumerate(args.q):
        if i:
            time.sleep(1.0)
        try:
            res = serp_one(nfc(q.strip()), args.limit)
            if args.brief:
                res["videos"] = [{k: v[k] for k in ("title", "channel", "views", "published", "match")}
                                 for v in res["videos"][:5]]
            out.append(res)
        except Exception as e:
            errors[q] = f"{type(e).__name__}: {e}"
    if not out:
        fail("youtube search failed", errors=errors)
    result = {"serps": out}
    if errors:
        result["errors"] = errors
    emit(result)


# ---------- links ----------

def links(args):
    rows = []
    for q in args.q:
        q = nfc(q.strip())
        enc = urllib.parse.quote(q)
        rows.append({
            "q": q,
            "google_trends_youtube": f"https://trends.google.com/trends/explore?geo=VN&gprop=youtube&date=today%2012-m&q={enc}",
            "google_trends_youtube_5y": f"https://trends.google.com/trends/explore?geo=VN&gprop=youtube&date=today%205-y&q={enc}",
            "youtube_search": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}",
            "tiktok_search": f"https://www.tiktok.com/search?q={enc}",
        })
    if len(args.q) > 1:
        joined = urllib.parse.quote(",".join(nfc(q.strip()) for q in args.q[:5]), safe=",")
        rows.append({"compare_up_to_5": f"https://trends.google.com/trends/explore?geo=VN&gprop=youtube&date=today%2012-m&q={joined}"})
    rows.append({"tiktok_creative_center_hashtags": "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?region=VN"})
    emit(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("expand")
    e.add_argument("--seed", action="append", required=True, help="seed keyword; repeat for more")
    e.add_argument("--platform", default="yt,google,tiktok", help="comma list of yt, google, tiktok")
    e.add_argument("--alphabet", action="store_true", help="also try question words and seed + letter")
    e.add_argument("--no-accent", action="store_true", help="also query each seed without diacritics")
    e.add_argument("--limit", type=int, default=0, help="keep only the first N keywords (0 = all)")
    s = sub.add_parser("serp")
    s.add_argument("--q", action="append", required=True, help="search phrase; repeat for more")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--brief", action="store_true", help="only the top 5 videos per phrase, fewer fields")
    l = sub.add_parser("links")
    l.add_argument("--q", action="append", required=True)
    args = p.parse_args()
    {"expand": expand, "serp": serp, "links": links}[args.cmd](args)


if __name__ == "__main__":
    main()
