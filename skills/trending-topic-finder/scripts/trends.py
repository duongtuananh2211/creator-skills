#!/usr/bin/env python3
"""Helper for the trending-topic-finder skill: pull what is trending in Vietnam now.

Subcommands (each prints compact JSON to stdout):
  google-trends [--geo VN]          Google Trends "Trending now" RSS, with linked news.
  news [--source NAME|all] [--limit N]
                                    News feeds: google-news, vnexpress-most-read,
                                    vnexpress-featured, kenh14, tuoitre, thanhnien.
  wiki-top [--date D] [--limit N]   Most-viewed vi.wikipedia articles for one day (UTC).
  suggest --q SEED [--yt] [--alphabet]
                                    Google / YouTube autocomplete (hl=vi, gl=VN).
  all [--seeds "a,b,c"] [--limit 20] [--no-yt]
                                    Everything above at once, keyed by source;
                                    seeds go to YouTube autocomplete unless --no-yt.

A source that fails returns {"source": ..., "error": ...} instead of stopping the run.
Only the Python standard library is used.
"""
import argparse
import email.utils
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

TIMEOUT = 15
# vnexpress.net took ~20 s just to open a connection on every try (2026-10-29), while
# other sites answered in under a second, so its sources get a longer budget.
SLOW_HOST_TIMEOUT = 35
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)
# Wikimedia asks API clients to identify themselves with a descriptive User-Agent.
WIKI_UA = "creator-skills-trending-topic-finder/1.0 (https://github.com/duongtuananh2211/creator-skills)"

HT_NS = "https://trends.google.com/trending/rss"
NEWS_FEEDS = {
    "google-news": ("rss", "https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi"),
    # The RSS at /rss/tin-xem-nhieu.rss is frozen on 2021 articles (checked 2026-10-29),
    # so the most-read list is scraped from the HTML page, which is current.
    "vnexpress-most-read": ("vnexpress-html", "https://vnexpress.net/tin-xem-nhieu"),
    "vnexpress-featured": ("rss", "https://vnexpress.net/rss/tin-noi-bat.rss"),
    "kenh14": ("rss", "https://kenh14.vn/rss/home.rss"),
    "tuoitre": ("rss", "https://tuoitre.vn/rss/tin-moi-nhat.rss"),
    "thanhnien": ("rss", "https://thanhnien.vn/rss/home.rss"),
}
WIKI_SKIP_PREFIXES = (
    "Trang_Chính", "Main_Page", "Đặc_biệt:", "Special:", "Tập_tin:", "File:",
    "Wikipedia:", "Thể_loại:", "Bản_mẫu:", "Trợ_giúp:", "Cổng_thông_tin:",
    "Chủ_đề:", "Thảo_luận", "Thành_viên:", "MediaWiki:", "Mô_đun:",
)
QUESTION_PREFIXES = ["tại sao", "vì sao", "cách", "có nên", "là gì"]


def fetch(url, ua=BROWSER_UA, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def clean(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def to_iso(value):
    """Normalise the date formats seen in Vietnamese feeds to ISO 8601; keep raw on failure."""
    if not value:
        return None
    value = value.strip()
    # "+07" offsets (Kenh14) are not RFC 2822; pad them.
    fixed = re.sub(r" ([+-]\d{2})$", r" \g<1>00", value)
    try:
        dt = email.utils.parsedate_to_datetime(fixed)
        if dt is not None:
            return dt.isoformat()
    except (TypeError, ValueError, IndexError):
        pass
    # Tuổi Trẻ uses "10/29/2026 12:21:00 PM" in Vietnam time.
    try:
        dt = datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
        return dt.replace(tzinfo=timezone(timedelta(hours=7))).isoformat()
    except ValueError:
        return value


def guarded(source, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except urllib.error.HTTPError as e:
        return {"source": source, "error": f"HTTP {e.code} {e.reason}"}
    except Exception as e:  # network, parse, timeout: report and keep going
        return {"source": source, "error": f"{type(e).__name__}: {e}"}


# ---------- Google Trends ----------

def google_trends(geo="VN"):
    url = f"https://trends.google.com/trending/rss?geo={urllib.parse.quote(geo)}"
    root = ET.fromstring(fetch(url).encode("utf-8"))
    ht = lambda tag: f"{{{HT_NS}}}{tag}"
    items = []
    for it in root.iter("item"):
        news = []
        for n in it.findall(ht("news_item")):
            news.append({
                "title": clean(n.findtext(ht("news_item_title"))),
                "url": (n.findtext(ht("news_item_url")) or "").strip(),
                "source": clean(n.findtext(ht("news_item_source"))),
            })
        items.append({
            "title": clean(it.findtext("title")),
            "approx_traffic": (it.findtext(ht("approx_traffic")) or "").strip() or None,
            "pubDate": to_iso(it.findtext("pubDate")),
            "news": news,
        })
    return {"source": "google-trends", "geo": geo, "url": url, "count": len(items), "items": items}


# ---------- News ----------

def timeout_for(url):
    return SLOW_HOST_TIMEOUT if "vnexpress.net" in url else TIMEOUT


def parse_rss(name, url):
    root = ET.fromstring(fetch(url, timeout=timeout_for(url)).encode("utf-8"))
    items = []
    for it in root.iter("item"):
        title = clean(it.findtext("title"))
        src_el = it.find("source")
        outlet = clean(src_el.text) if src_el is not None else None
        if name == "google-news" and outlet and title.endswith(" - " + outlet):
            title = title[: -len(" - " + outlet)]
        items.append({
            "title": title,
            "link": clean(it.findtext("link")),
            "pubDate": to_iso(it.findtext("pubDate")),
            "source": outlet or name,
        })
    return items


def parse_vnexpress_html(name, url):
    page = fetch(url, timeout=timeout_for(url))
    items, seen = [], set()
    pattern = r'class="title-news"[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*title="([^"]+)"'
    for link, title in re.findall(pattern, page):
        if link in seen:
            continue
        seen.add(link)
        items.append({"rank": len(items) + 1, "title": clean(title), "link": link,
                      "pubDate": None, "source": "vnexpress"})
    if not items:
        raise ValueError("no articles found; the page layout may have changed")
    return items


def news_one(name, limit=None):
    kind, url = NEWS_FEEDS[name]
    parser = parse_vnexpress_html if kind == "vnexpress-html" else parse_rss
    items = parser(name, url)[:limit]
    return {"source": name, "url": url, "count": len(items), "items": items}


def news(source="all", limit=None):
    names = list(NEWS_FEEDS) if source == "all" else [source]
    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        results = list(pool.map(lambda n: guarded(n, news_one, n, limit), names))
    if source != "all":
        return results[0]
    return {r["source"]: r for r in results}


# ---------- Wikipedia ----------

def wiki_top(date=None, limit=50):
    if date:
        days = [datetime.strptime(date, "%Y-%m-%d").date()]
    else:
        # Data for a day appears with roughly a one-day lag; try D-1 then D-2.
        today = datetime.now(timezone.utc).date()
        days = [today - timedelta(days=1), today - timedelta(days=2)]
    last_err = None
    for day in days:
        url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/vi.wikipedia/"
               f"all-access/{day:%Y/%m/%d}")
        try:
            data = json.loads(fetch(url, ua=WIKI_UA))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                last_err = e
                continue
            raise
        articles = []
        for a in data["items"][0]["articles"]:
            title = a["article"]
            if title.startswith(WIKI_SKIP_PREFIXES) or title == "-":
                continue
            articles.append({"article": title.replace("_", " "), "views": a["views"],
                             "rank": a["rank"]})
            if len(articles) >= limit:
                break
        return {"source": "wiki-top", "date": day.isoformat(), "url": url,
                "count": len(articles), "items": articles}
    raise last_err


# ---------- Autocomplete ----------

def suggest_once(q, yt=False):
    params = {"client": "firefox", "hl": "vi", "gl": "VN", "q": q}
    if yt:
        params["ds"] = "yt"
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(params)
    data = json.loads(fetch(url))
    return data[1] if len(data) > 1 else []


def suggest(q, yt=False, alphabet=False):
    queries = [q]
    if alphabet:
        # Skip question words when the seed already starts with one ("vì sao …").
        if not any(q.lower().startswith(w) for w in QUESTION_PREFIXES + ["tại sao", "sao"]):
            queries += [f"{w} {q}" for w in QUESTION_PREFIXES if w != "là gì"]
            queries.append(f"{q} là gì")
        queries += [f"{q} {c}" for c in "abcdeghiklmnopqrstuvxy"]  # Vietnamese alphabet letters
        queries = queries[:30]  # stay polite to an unofficial endpoint
    results, errors = {}, {}
    for i, query in enumerate(queries):
        if i:
            time.sleep(0.25)
        try:
            results[query] = suggest_once(query, yt)
        except Exception as e:
            errors[query] = f"{type(e).__name__}: {e}"
    if not results and errors:
        return {"source": "suggest", "q": q, "error": next(iter(errors.values()))}
    unique = list(dict.fromkeys(s for lst in results.values() for s in lst))
    out = {"source": "suggest-yt" if yt else "suggest", "q": q, "requests": len(queries),
           "count": len(unique), "suggestions": unique}
    if errors:
        out["errors"] = errors
    return out


# ---------- all ----------

def run_all(seeds, yt=True, limit=20):
    jobs = {
        "google-trends": lambda: guarded("google-trends", google_trends, "VN"),
        "news": lambda: news("all", limit),
        "wiki-top": lambda: guarded("wiki-top", wiki_top, None, limit),
    }
    seeds = [s.strip() for s in seeds if s.strip()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {k: pool.submit(f) for k, f in jobs.items()}
        # Autocomplete runs one seed at a time in a single worker to keep request rate low.
        sug = pool.submit(lambda: [guarded("suggest", suggest, s, yt) for s in seeds])
        out = {"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        for k, f in futures.items():
            out[k] = f.result()
        out["suggest"] = sug.result()
    failed = [k for k in ("google-trends", "wiki-top") if "error" in out[k]]
    failed += [k for k, v in out["news"].items() if "error" in v]
    failed += [f"suggest:{s['q']}" for s in out["suggest"] if "error" in s]
    out["failed_sources"] = failed
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("google-trends")
    g.add_argument("--geo", default="VN")
    n = sub.add_parser("news")
    n.add_argument("--source", default="all", choices=["all", *NEWS_FEEDS])
    n.add_argument("--limit", type=int, default=None, help="max items per feed")
    w = sub.add_parser("wiki-top")
    w.add_argument("--date", help="YYYY-MM-DD (UTC); default yesterday, then the day before")
    w.add_argument("--limit", type=int, default=50)
    s = sub.add_parser("suggest")
    s.add_argument("--q", required=True)
    s.add_argument("--yt", action="store_true", help="YouTube suggestions (ds=yt)")
    s.add_argument("--alphabet", action="store_true", help="also expand with question words and letters")
    a = sub.add_parser("all")
    a.add_argument("--seeds", default="", help="comma-separated seed keywords for autocomplete")
    a.add_argument("--no-yt", action="store_true", help="use web autocomplete instead of YouTube")
    a.add_argument("--limit", type=int, default=20,
                   help="max items per news feed and for wiki-top (default 20)")
    args = p.parse_args()

    if args.cmd == "google-trends":
        result = guarded("google-trends", google_trends, args.geo)
    elif args.cmd == "news":
        if args.source == "all":
            result = news("all", args.limit)
        else:
            result = guarded(args.source, news_one, args.source, args.limit)
    elif args.cmd == "wiki-top":
        result = guarded("wiki-top", wiki_top, args.date, args.limit)
    elif args.cmd == "suggest":
        result = guarded("suggest", suggest, args.q, args.yt, args.alphabet)
    else:
        result = run_all(args.seeds.split(","), yt=not args.no_yt, limit=args.limit)
    json.dump(result, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
