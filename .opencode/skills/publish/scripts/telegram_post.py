#!/usr/bin/env python3
"""Post new digest posts to a Telegram public channel. Opt-in only.

Usage:
    telegram_post.py [--dry-run] [--chat @handle] [--include-updated] [file ...]

With no file args, posts are taken from the HEAD commit
(`git diff HEAD~1 HEAD --name-status -- src/_posts/`): files Added in that
commit are sent, Modified ones are skipped unless --include-updated is given.
With file args, exactly those files are sent.

Each post becomes one message: title, share_text hook, summary, and links
(site, original, HN/Lobsters when present), sent via the Bot API as HTML.

Config comes from the environment and is never committed:
    TELEGRAM_BOT_TOKEN   Bot token from @BotFather (required).
    TELEGRAM_CHANNEL     e.g. @digestvo (required, --chat overrides it).
    BRIDGETOWN_URL       Site root, defaults to https://digest.ezcurdia.dev.

The bot must be an administrator of the channel. The token is never printed.
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

POSTS_PREFIX = "src/_posts/"
FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")
SITE_URL_DEFAULT = "https://digest.ezcurdia.dev"
API_TIMEOUT = 30
MESSAGE_LIMIT = 4096


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def commit_post_files(include_updated):
    """(added, updated) post paths from the HEAD commit's name-status."""
    res = git("diff", "HEAD~1", "HEAD", "--name-status",
              "--diff-filter=ACM", "--", POSTS_PREFIX)
    if res.returncode != 0:
        fail("`git diff HEAD~1 HEAD` failed:\n" + (res.stderr or res.stdout).strip())
    added, updated = [], []
    for line in res.stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        status, path = parts
        if not path.endswith(".md"):
            continue
        if status == "A":
            added.append(path)
        elif status in ("C", "M"):
            updated.append(path)
    if include_updated:
        return added + updated
    return added


def parse_front_matter(text):
    """Flat front-matter scan with folded-block support (`summary: >-`).

    The digest writes `summary` as a folded block of indented lines; a naive
    line scan would read its value as the literal `>-`. Continuation lines
    (indented) are folded with spaces; other keys are single-line scalars
    with surrounding quotes stripped.
    """
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return None, ""
    fm_text, body = m.group(1), text[m.end():]
    keys = {}
    current = None
    folded = None
    for line in fm_text.split("\n"):
        if folded is not None and (line.startswith(" ") or line.startswith("\t")):
            folded.append(line.strip())
            continue
        if folded is not None:
            keys[current] = html.unescape(" ".join(folded))
            folded = None
            current = None
        if not line or line[0] in " \t-#":
            continue
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        name, value = name.strip(), value.strip()
        if value in (">-", ">", "|-", "|"):
            current, folded = name, []
        elif value:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                try:
                    value = json.loads(value) if value[0] == '"' else value[1:-1]
                except json.JSONDecodeError:
                    value = value[1:-1]
            keys[name] = html.unescape(value)
    if folded is not None:
        keys[current] = html.unescape(" ".join(folded))
    return keys, body


def site_url_for(path, site_root):
    """Canonical post URL from the filename: YYYY-MM-DD-slug.md."""
    m = FILENAME_RE.match(os.path.basename(path))
    if not m:
        return None
    year, month, day, slug = m.groups()
    return "{0}/digest/{1}/{2}/{3}/{4}/".format(
        site_root.rstrip("/"), year, month, day, slug)


def build_message(keys, url):
    """HTML message for one post, truncated to Telegram's 4096-char limit."""
    title = keys.get("title", "(untitled)").strip()
    share = keys.get("share_text", "").strip()
    summary = re.sub(r"\s+", " ", keys.get("summary", "")).strip()

    links = []
    if url:
        links.append(('<a href="{0}">Read on digesTvo</a>').format(html.escape(url, quote=True)))
    if keys.get("source_url"):
        links.append(('<a href="{0}">Original</a>').format(
            html.escape(keys["source_url"], quote=True)))
    if keys.get("hn_url"):
        links.append(('<a href="{0}">Hacker News</a>').format(
            html.escape(keys["hn_url"], quote=True)))
    if keys.get("lobsters_url"):
        links.append(('<a href="{0}">Lobsters</a>').format(
            html.escape(keys["lobsters_url"], quote=True)))

    head = "<b>{0}</b>".format(html.escape(title, quote=False))
    parts = [head]
    if share:
        parts.append("<i>{0}</i>".format(html.escape(share, quote=False)))
    parts.append("{SUMMARY}")
    if links:
        parts.append("  ·  ".join(links))
    template = "\n\n".join(parts)

    budget = MESSAGE_LIMIT - len(template.replace("{SUMMARY}", "")) - 1
    if len(summary) > budget:
        summary = summary[:max(0, budget - 1)].rstrip() + "…"
    return template.replace("{SUMMARY}", html.escape(summary, quote=False))


def send_message(api_base, chat, message):
    payload = json.dumps({
        "chat_id": chat,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        api_base + "/sendMessage", data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")
        except Exception:
            detail = str(exc)
        raise RuntimeError("HTTP {0}: {1}".format(exc.code, detail))
    except urllib.error.URLError as exc:
        raise RuntimeError("could not reach Telegram API: {0}".format(exc.reason))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="post files to send")
    parser.add_argument("--dry-run", action="store_true",
                        help="print messages, send nothing")
    parser.add_argument("--chat", default=None,
                        help="override TELEGRAM_CHANNEL for this run")
    parser.add_argument("--include-updated", action="store_true",
                        help="also send Modified (not just Added) posts from HEAD")
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        fail("TELEGRAM_BOT_TOKEN is not set; export it before posting")
    chat = (args.chat or os.environ.get("TELEGRAM_CHANNEL", "")).strip()
    if not chat:
        fail("no channel: set TELEGRAM_CHANNEL or pass --chat @handle")
    if not (chat.startswith("@") or chat.startswith("-")
            or chat.startswith("+") or chat.lstrip("0123456789") == ""):
        chat = "@" + chat
    site_root = os.environ.get("BRIDGETOWN_URL", SITE_URL_DEFAULT).strip() \
        or SITE_URL_DEFAULT

    if args.files:
        paths = args.files
    else:
        if git("rev-parse", "--is-inside-work-tree").returncode != 0:
            fail("not inside a git work tree; run from the repo root")
        paths = commit_post_files(args.include_updated)

    posts = []
    for path in paths:
        if not path.startswith(POSTS_PREFIX) or not path.endswith(".md"):
            fail("{0} is not a digest post under {1}".format(path, POSTS_PREFIX))
        if not os.path.isfile(path):
            fail("{0} not found".format(path))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        keys, _ = parse_front_matter(text)
        if not keys or not keys.get("title"):
            fail("{0} has no readable front matter; refusing to post".format(path))
        url = site_url_for(path, site_root)
        if not url:
            fail("{0} is not named YYYY-MM-DD-slug.md; cannot build its URL".format(path))
        posts.append({"path": path, "title": keys["title"],
                      "message": build_message(keys, url)})

    if not posts:
        print("REPORT")
        print("NOTHING TO SEND — the HEAD commit added no posts under {0}; "
              "nothing was sent to {1}.".format(POSTS_PREFIX, chat))
        return

    if args.dry_run:
        print("REPORT")
        print("DRY RUN — nothing was sent to {0}.".format(chat))
        for p in posts:
            print("- {0}  ({1} chars)".format(p["path"], len(p["message"])))
            print(p["message"])
            print("---")
        return

    api_base = "https://api.telegram.org/bot{0}".format(token)
    sent = []
    try:
        for i, p in enumerate(posts):
            if i:
                time.sleep(1)
            resp = send_message(api_base, chat, p["message"])
            if not resp.get("ok"):
                raise RuntimeError("API returned: {0}".format(
                    json.dumps(resp)[:300]))
            msg = resp.get("result", {})
            sent.append({"path": p["path"],
                         "message_id": msg.get("message_id")})
    except RuntimeError as exc:
        print("error: send failed after {0} of {1} message(s): {2}".format(
            len(sent), len(posts), exc), file=sys.stderr)
        for s in sent:
            print("error: already sent {0} (message_id {1})".format(
                s["path"], s["message_id"]), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("error: interrupted after {0} of {1} message(s)".format(
            len(sent), len(posts)), file=sys.stderr)
        sys.exit(1)

    print("REPORT")
    print("Sent {0} message(s) to {1}.".format(len(sent), chat))
    for s in sent:
        print("- sent {0}  (message_id {1})".format(s["path"], s["message_id"]))


if __name__ == "__main__":
    main()
