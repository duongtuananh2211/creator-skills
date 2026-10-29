#!/usr/bin/env python3
"""Local review server for the script-review skill.

Subcommands:
  serve <script.md> [--port 0] [--no-open] [--round N] [--timeout-min 120]
                    [--previous <review-json>]
      Serve assets/review.html on 127.0.0.1, wait for the human to submit
      feedback, write <stem>.review-r<N>.json and .md next to the script, then
      exit. Prints REVIEW_URL, then FEEDBACK_SAVED <path> (or REVIEW_TIMEOUT).
  respond <review-json> <responses-json>
      Merge the agent's per-comment responses into a review json.

Only the Python standard library is used.
"""
import argparse
import json
import re
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ASSET = Path(__file__).resolve().parent.parent / "assets" / "review.html"
COMMENT_TYPES = {"sửa", "cắt", "hỏi", "giữ", "khác"}
VERDICTS = {"duyệt", "sửa tiếp"}
RESPONSE_STATUSES = {"đã sửa", "giữ nguyên", "cần bạn quyết"}
MAX_BODY = 5 * 1024 * 1024

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
HR_RE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- parsing

def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells = re.split(r"(?<!\\)\|", s)
    out = []
    for c in cells:
        c = c.strip().replace("\\|", "|")
        c = re.sub(r"<br\s*/?>", "\n", c, flags=re.I)
        out.append(c)
    return out


def unique_names(names):
    seen, out = {}, []
    for i, n in enumerate(names):
        n = n or f"Cột {i + 1}"
        if n in seen:
            seen[n] += 1
            n = f"{n} ({seen[n]})"
        else:
            seen[n] = 1
        out.append(n)
    return out


def is_table_start(lines, i):
    if i + 1 >= len(lines):
        return False
    return "|" in lines[i] and "|" in lines[i + 1] and "-" in lines[i + 1] and bool(SEP_RE.match(lines[i + 1]))


def parse_blocks(md):
    """Split markdown into reviewable blocks (heading, p, li, quote, code, row)."""
    lines = md.splitlines()
    blocks = []
    section = ""
    table_no = 0

    def add(btype, text, raw, line_no, **extra):
        b = {"id": f"b{len(blocks) + 1}", "type": btype, "text": text, "raw": raw, "line": line_no, "section": section}
        b.update(extra)
        blocks.append(b)

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if FENCE_RE.match(line):
            start = i
            i += 1
            while i < n and not FENCE_RE.match(lines[i]):
                i += 1
            body = lines[start + 1:i]
            i += 1  # closing fence
            if any(x.strip() for x in body):
                add("code", "\n".join(body), "\n".join(lines[start:i]), start + 1)
            continue
        m = HEAD_RE.match(line)
        if m:
            section = m.group(2)
            add("heading", m.group(2), line, i + 1, level=len(m.group(1)))
            i += 1
            continue
        if is_table_start(lines, i):
            table_no += 1
            headers = unique_names(split_row(line))
            i += 2
            while i < n and lines[i].strip() and "|" in lines[i]:
                cells = split_row(lines[i])
                names = headers + unique_names([""] * max(0, len(cells) - len(headers)))
                fields = [{"name": names[k], "text": cells[k]} for k in range(len(cells))]
                add("row", " | ".join(c["text"] for c in fields), lines[i], i + 1, cells=fields, table=table_no)
                i += 1
            continue
        if HR_RE.match(line):
            i += 1
            continue
        m = LIST_RE.match(line)
        if m:
            start = i
            text = [m.group(3)]
            i += 1
            while i < n and lines[i].strip() and lines[i][:1] in (" ", "\t") and not LIST_RE.match(lines[i]):
                text.append(lines[i].strip())
                i += 1
            add("li", "\n".join(text), "\n".join(lines[start:i]), start + 1, indent=len(m.group(1).expandtabs(2)), marker=m.group(2))
            continue
        # paragraph or quote: gather until blank or another structure starts
        start = i
        quote = line.lstrip().startswith(">")
        buf = []
        while i < n and lines[i].strip():
            ln = lines[i]
            if i > start and (HEAD_RE.match(ln) or LIST_RE.match(ln) or is_table_start(lines, i) or FENCE_RE.match(ln) or HR_RE.match(ln)):
                break
            buf.append(re.sub(r"^\s*>\s?", "", ln) if quote else ln.strip())
            i += 1
        add("quote" if quote else "p", "\n".join(buf), "\n".join(lines[start:i]), start + 1)
    return blocks


# ---------------------------------------------------------------- files

def review_path(script, rnd, ext="json"):
    return script.with_name(f"{script.stem}.review-r{rnd}.{ext}")


def next_round(script):
    pat = re.compile(re.escape(script.stem) + r"\.review-r(\d+)\.json$")
    nums = [int(m.group(1)) for p in script.parent.glob(f"{script.stem}.review-r*.json") if (m := pat.match(p.name))]
    return max(nums, default=0) + 1


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_previous(script, rnd, prev_path):
    path = Path(prev_path) if prev_path else review_path(script, rnd - 1)
    data = load_json(path)
    if not isinstance(data, dict) or "responses" not in data or not isinstance(data["responses"], dict):
        return None
    responses = data["responses"]
    comments = []
    for c in data.get("comments", []):
        if isinstance(c, dict):
            comments.append(dict(c, response=responses.get(c.get("id"))))
    return {
        "file": data.get("file"),
        "round": data.get("round"),
        "verdict": data.get("verdict"),
        "overall": data.get("overall", ""),
        "submitted_at": data.get("submitted_at"),
        "approved_count": len(data.get("approved_blocks", [])),
        "comments": comments,
    }


def md_quote(text):
    return "\n".join("> " + ln for ln in text.splitlines()) or "> "


def render_md(data, blocks):
    by_id = {b["id"]: b for b in blocks}
    order = {b["id"]: k for k, b in enumerate(blocks)}
    out = [f"# Phản hồi review: {data['file']} (vòng {data['round']})", ""]
    out.append(f"- Gửi lúc: {data['submitted_at']}")
    out.append(f"- Kết luận: **{data['verdict']}**")
    out.append(f"- Số nhận xét: {len(data['comments'])} | đoạn đã đánh dấu ổn: {len(data['approved_blocks'])}")
    out += ["", "## Nhận xét chung", "", data.get("overall") or "(không có)", "", "## Nhận xét theo đoạn", ""]
    responses = data.get("responses") or {}
    comments = sorted(data["comments"], key=lambda c: (order.get(c["block_id"], 10**9), c.get("start") or 0))
    if not comments:
        out.append("(không có)")
    for c in comments:
        b = by_id.get(c["block_id"], {})
        where = f"{c['block_id']}" + (f" / {c['field']}" if c.get("field") else "")
        if b.get("section"):
            where += f" (mục: {b['section']})"
        out.append(f"### {c['id']} [{c['type']}] {where}")
        out.append("")
        out.append(md_quote(c.get("quote", "")))
        if c.get("note"):
            out += ["", f"Nhận xét: {c['note']}"]
        if c.get("suggestion"):
            out += ["", f"Đề xuất: {c['suggestion']}"]
        r = responses.get(c["id"])
        if r:
            out += ["", f"Agent trả lời: **{r.get('status')}** - {r.get('note', '')}"]
        out.append("")
    out += ["## Đoạn đã đánh dấu ổn", ""]
    if data["approved_blocks"]:
        for bid in data["approved_blocks"]:
            b = by_id.get(bid, {})
            out.append(f"- {bid}: {(b.get('text') or '')[:80].replace(chr(10), ' ')}")
    else:
        out.append("(không có)")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- validation

def validate_feedback(body, block_ids):
    if not isinstance(body, dict):
        return "Body phải là JSON object"
    if body.get("verdict") not in VERDICTS:
        return "verdict phải là 'duyệt' hoặc 'sửa tiếp'"
    if not isinstance(body.get("overall", ""), str):
        return "overall phải là chuỗi"
    approved = body.get("approved_blocks", [])
    if not isinstance(approved, list) or any(not isinstance(x, str) or x not in block_ids for x in approved):
        return "approved_blocks chứa id không hợp lệ"
    comments = body.get("comments", [])
    if not isinstance(comments, list):
        return "comments phải là danh sách"
    seen = set()
    for c in comments:
        if not isinstance(c, dict):
            return "Mỗi comment phải là object"
        cid = c.get("id")
        if not isinstance(cid, str) or not cid or cid in seen:
            return "comment thiếu id hoặc trùng id"
        seen.add(cid)
        if c.get("block_id") not in block_ids:
            return f"{cid}: block_id không tồn tại"
        if c.get("type") not in COMMENT_TYPES:
            return f"{cid}: type không hợp lệ"
        if c.get("field") is not None and not isinstance(c.get("field"), str):
            return f"{cid}: field phải là chuỗi hoặc null"
        for key in ("quote", "note", "suggestion", "context_before", "context_after"):
            if not isinstance(c.get(key, ""), str):
                return f"{cid}: {key} phải là chuỗi"
        for key in ("start", "end"):
            if c.get(key) is not None and (not isinstance(c.get(key), int) or isinstance(c.get(key), bool)):
                return f"{cid}: {key} phải là số nguyên"
    return None


def clean_feedback(body, script, rnd):
    keep = ("id", "block_id", "field", "quote", "start", "end", "context_before", "context_after", "type", "note", "suggestion", "created_at")
    comments = []
    for c in body.get("comments", []):
        d = {k: c.get(k) for k in keep}
        d["field"] = c.get("field") or None
        for k in ("quote", "note", "suggestion", "context_before", "context_after"):
            d[k] = c.get(k) or ""
        d["created_at"] = c.get("created_at") or now_iso()
        comments.append(d)
    return {
        "file": script.name,
        "round": rnd,
        "submitted_at": now_iso(),
        "overall": body.get("overall", ""),
        "verdict": body["verdict"],
        "approved_blocks": body.get("approved_blocks", []),
        "comments": comments,
    }


# ---------------------------------------------------------------- server

class Ctx:
    pass


class Handler(BaseHTTPRequestHandler):
    server_version = "ScriptReview/1.0"

    def log_message(self, fmt, *args):  # keep stdout clean for the agent
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

    def _host_ok(self):
        port = self.server.server_address[1]
        allowed = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if self.headers.get("Host") not in allowed:
            return False
        origin = self.headers.get("Origin")
        return origin is None or origin in {f"http://{h}" for h in allowed}

    def do_GET(self):
        ctx = self.server.ctx
        if not self._host_ok():
            return self._send(403, {"error": "forbidden host"})
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            try:
                return self._send(200, ASSET.read_bytes(), "text/html; charset=utf-8")
            except OSError:
                return self._send(500, {"error": f"không đọc được {ASSET}"})
        if path == "/api/doc":
            return self._send(200, ctx.doc)
        self._send(404, {"error": "not found"})

    def do_POST(self):
        ctx = self.server.ctx
        if not self._host_ok():
            return self._send(403, {"error": "forbidden host"})
        if self.path.split("?", 1)[0] != "/api/feedback":
            return self._send(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            return self._send(400, {"error": "body rỗng hoặc quá lớn"})
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self._send(400, {"error": "JSON không hợp lệ"})
        err = validate_feedback(body, ctx.block_ids)
        if err:
            return self._send(400, {"error": err})
        with ctx.lock:
            if ctx.done.is_set():
                return self._send(409, {"error": "phản hồi đã được gửi"})
            data = clean_feedback(body, ctx.script, ctx.round)
            jpath, mpath = review_path(ctx.script, ctx.round, "json"), review_path(ctx.script, ctx.round, "md")
            try:
                jpath.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                mpath.write_text(render_md(data, ctx.blocks), encoding="utf-8")
            except OSError as e:
                return self._send(500, {"error": f"không ghi được file: {e}"})
            ctx.saved = jpath
            self._send(200, {"ok": True, "json": str(jpath), "md": str(mpath)})
            ctx.done.set()


def cmd_serve(args):
    script = Path(args.script).expanduser().resolve()
    if not script.is_file():
        sys.exit(f"Không tìm thấy file: {script}")
    md = script.read_text(encoding="utf-8")
    blocks = parse_blocks(md)
    if not blocks:
        sys.exit("File không có nội dung để review")

    prev_data = load_json(args.previous) if args.previous else None
    if args.round:
        rnd = args.round
    elif args.previous and isinstance(prev_data, dict) and isinstance(prev_data.get("round"), int):
        rnd = prev_data["round"] + 1
    else:
        rnd = next_round(script)
    if rnd < 1:
        sys.exit("--round phải >= 1")

    ctx = Ctx()
    ctx.script, ctx.round, ctx.blocks = script, rnd, blocks
    ctx.block_ids = {b["id"] for b in blocks}
    ctx.done, ctx.lock, ctx.saved = threading.Event(), threading.Lock(), None
    ctx.doc = {
        "file": script.name,
        "round": rnd,
        "generated_at": now_iso(),
        "blocks": blocks,
        "markdown": md,
        "previous": load_previous(script, rnd, args.previous),
    }

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    server.ctx = ctx
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"REVIEW_URL {url}", flush=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    if not args.no_open:
        try:
            if not webbrowser.open(url):
                print("Không mở được trình duyệt tự động, hãy mở URL ở trên bằng tay.", file=sys.stderr, flush=True)
        except Exception:
            pass
    try:
        got = ctx.done.wait(args.timeout_min * 60)
    except KeyboardInterrupt:
        print("REVIEW_CANCELLED", flush=True)
        threading.Thread(target=server.shutdown).start()
        return 130
    if got:
        print(f"FEEDBACK_SAVED {ctx.saved}", flush=True)
        time.sleep(0.5)  # let the 200 response drain before closing
        shutter = threading.Thread(target=server.shutdown)
        shutter.start()
        shutter.join(5)
        server.server_close()
        return 0
    print("REVIEW_TIMEOUT", flush=True)
    shutter = threading.Thread(target=server.shutdown)
    shutter.start()
    shutter.join(5)
    server.server_close()
    return 2


def cmd_respond(args):
    rpath = Path(args.review_json)
    review = load_json(rpath)
    if not isinstance(review, dict) or "comments" not in review:
        sys.exit(f"Không đọc được review json: {rpath}")
    new = load_json(args.responses_json)
    if isinstance(new, dict) and isinstance(new.get("responses"), dict):
        new = new["responses"]
    if not isinstance(new, dict):
        sys.exit(f"Không đọc được responses json: {args.responses_json}")
    ids = {c["id"] for c in review["comments"]}
    errors = []
    for cid, r in new.items():
        if cid not in ids:
            errors.append(f"{cid}: không có comment này trong review")
        elif not isinstance(r, dict) or r.get("status") not in RESPONSE_STATUSES:
            errors.append(f"{cid}: status phải là một trong {sorted(RESPONSE_STATUSES)}")
    if errors:
        sys.exit("\n".join(errors))
    responses = review.get("responses") or {}
    for cid, r in new.items():
        responses[cid] = {"status": r["status"], "note": r.get("note", "")}
    review["responses"] = responses
    rpath.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    missing = sorted(ids - set(responses))
    print(f"RESPONSES_SAVED {rpath.resolve()} ({len(responses)}/{len(ids)} nhận xét đã có phản hồi)")
    if missing:
        print("Chưa trả lời: " + ", ".join(missing))
    # refresh the human-readable summary if it exists
    mpath = rpath.with_suffix(".md")
    if mpath.exists():
        script = rpath.parent / (re.sub(r"\.review-r\d+\.json$", "", rpath.name) + ".md")
        blocks = parse_blocks(script.read_text(encoding="utf-8")) if script.is_file() else []
        mpath.write_text(render_md(review, blocks), encoding="utf-8")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve", help="mở trang review và chờ phản hồi")
    s.add_argument("script")
    s.add_argument("--port", type=int, default=0)
    s.add_argument("--no-open", action="store_true")
    s.add_argument("--round", type=int, default=0)
    s.add_argument("--timeout-min", type=float, default=120)
    s.add_argument("--previous", help="review json của vòng trước (dùng khi file kịch bản đã đổi tên, ví dụ .v2.md)")
    r = sub.add_parser("respond", help="gộp phản hồi của agent vào review json")
    r.add_argument("review_json")
    r.add_argument("responses_json")
    args = ap.parse_args()
    sys.exit(cmd_serve(args) if args.cmd == "serve" else cmd_respond(args))


if __name__ == "__main__":
    main()
