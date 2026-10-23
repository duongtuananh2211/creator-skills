#!/usr/bin/env python3
"""Helper for the google-flow-image-generation skill.

Subcommands:
  config                    Print the resolved config as JSON.
  set-project <id|url>      Save the Flow project id (accepts a full project URL).
  set-output-dir <path>     Save the folder generated images are moved into.
  mark                      Print the current timestamp; pass it to `move --since`.
  move --since TS [...]     Wait for images downloaded after TS, move them into
                            the output folder, print the new paths as JSON.

Only the Python standard library is used.
"""
import argparse
import json
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# The config lives in the user's project (the agent's working directory), so each
# project keeps its own Flow project id and output folder.
DEFAULT_CONFIG_PATH = Path.cwd() / "skill-config.json"
DEFAULT_CONFIG = {
    "flow_project_id": "",
    "output_dir": "./flow-images",
    "downloads_dir": "~/Downloads",
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}
PARTIAL_EXTS = {".crdownload", ".part", ".download", ".tmp"}


def load_config(path):
    if not path.exists():
        save_config(path, DEFAULT_CONFIG)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {**DEFAULT_CONFIG, **data}


def save_config(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_dir(value, config_path):
    # Relative paths resolve against the folder holding skill-config.json.
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = config_path.resolve().parent / path
    return path.resolve()


def parse_project_id(value):
    match = re.search(r"/project/([^/?#]+)", value)
    return match.group(1) if match else value.strip().strip("/")


def slugify(text, max_len=50):
    text = text.lower()
    text = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", text)
    text = re.sub(r"[èéẹẻẽêềếệểễ]", "e", text)
    text = re.sub(r"[ìíịỉĩ]", "i", text)
    text = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", text)
    text = re.sub(r"[ùúụủũưừứựửữ]", "u", text)
    text = re.sub(r"[ỳýỵỷỹ]", "y", text)
    text = text.replace("đ", "d")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len].rstrip("-") or "flow-image"


def find_new_images(downloads, since):
    found = []
    for p in downloads.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS and p.stat().st_mtime >= since:
            found.append(p)
    return sorted(found, key=lambda p: p.stat().st_mtime)


def has_partial_downloads(downloads, since):
    return any(
        p.suffix.lower() in PARTIAL_EXTS and p.stat().st_mtime >= since
        for p in downloads.iterdir()
        if p.is_file()
    )


def unique_path(path):
    if not path.exists():
        return path
    i = 2
    while True:
        candidate = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def cmd_config(args, config):
    print(json.dumps({
        "config_path": str(args.config),
        "flow_project_id": config["flow_project_id"],
        "project_url": f"https://flow.google.com/project/{config['flow_project_id']}"
        if config["flow_project_id"] else None,
        "output_dir": str(resolve_dir(config["output_dir"], args.config)),
        "downloads_dir": str(resolve_dir(config["downloads_dir"], args.config)),
    }, indent=2, ensure_ascii=False))


def cmd_set_project(args, config):
    config["flow_project_id"] = parse_project_id(args.value)
    save_config(args.config, config)
    print(json.dumps({"flow_project_id": config["flow_project_id"]}))


def cmd_set_output_dir(args, config):
    config["output_dir"] = args.path
    save_config(args.config, config)
    print(json.dumps({"output_dir": str(resolve_dir(args.path, args.config))}, ensure_ascii=False))


def cmd_mark(args, config):
    # Back off one second so a download that starts in the same second still counts.
    print(int(time.time()) - 1)


def cmd_move(args, config):
    downloads = resolve_dir(config["downloads_dir"], args.config)
    # A one-off --output-dir is relative to where the command runs, like any CLI path.
    output = Path(args.output_dir).expanduser().resolve() if args.output_dir \
        else resolve_dir(config["output_dir"], args.config)
    deadline = time.time() + args.timeout

    images = []
    while time.time() < deadline:
        images = find_new_images(downloads, args.since)
        if len(images) >= args.expect and not has_partial_downloads(downloads, args.since):
            # Let the last file settle before moving it.
            sizes = [p.stat().st_size for p in images]
            time.sleep(1)
            if sizes == [p.stat().st_size for p in images]:
                break
        time.sleep(1)

    if not images:
        print(json.dumps({"moved": [], "error": f"No new image found in {downloads} within {args.timeout}s"}))
        sys.exit(1)

    output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = slugify(args.name) if args.name else None
    moved = []
    for i, src in enumerate(images, start=1):
        if base:
            suffix = f"-{i}" if len(images) > 1 else ""
            dest_name = f"{stamp}-{base}{suffix}{src.suffix.lower()}"
        else:
            dest_name = src.name
        dest = unique_path(output / dest_name)
        shutil.move(str(src), str(dest))
        moved.append(str(dest))

    result = {"moved": moved, "output_dir": str(output)}
    if len(images) < args.expect:
        result["warning"] = f"Expected {args.expect} image(s), found {len(images)}"
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH,
                        help="Path to skill-config.json (default: ./skill-config.json in the project)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("config")
    p = sub.add_parser("set-project")
    p.add_argument("value", help="Project id or full https://flow.google.com/project/<id> URL")
    p = sub.add_parser("set-output-dir")
    p.add_argument("path")
    sub.add_parser("mark")
    p = sub.add_parser("move")
    p.add_argument("--since", type=float, required=True, help="Timestamp printed by `mark`")
    p.add_argument("--expect", type=int, default=1, help="Number of images to wait for")
    p.add_argument("--timeout", type=int, default=60, help="Seconds to wait for downloads")
    p.add_argument("--name", help="Text used to name the files (usually the prompt)")
    p.add_argument("--output-dir", help="Override the configured output folder for this run")

    args = parser.parse_args()
    config = load_config(args.config)
    {
        "config": cmd_config,
        "set-project": cmd_set_project,
        "set-output-dir": cmd_set_output_dir,
        "mark": cmd_mark,
        "move": cmd_move,
    }[args.command](args, config)


if __name__ == "__main__":
    main()
