#!/usr/bin/env python3
"""Scrape one or more tweets/X posts plus their visible replies.
No API, no browser.

Usage:
    fetch_tweet.py <tweet URL | numeric status ID> [...]

The first input is the original post; any further inputs are tweets
related to it (same thread, quote-tweets, notable replies). Each input
is scraped independently (see scrape_one) and written to its own
.opencode/tmp/digest/tweet-<id>.json. Duplicate IDs are scraped once.

Why static scraping and not a headless browser: X returns HTTP 403 to
automated Chromium (even with stealth tweaks and warmed cookies) while
the same page served to plain HTTP carries the tweet and its top replies
server-rendered. A browser adds ~170MB of downloads for strictly less
data, so the script scrapes the HTML directly with the standard library.

Only the replies X renders for logged-out readers are returned (usually
a handful of the top ones). The record flags when the thread is longer
than what was captured; the skill enriches with webfetch/websearch.

Errors go to stderr with exit code 1.
"""

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

RUN_DIR = ".opencode/tmp/digest"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

ID_RE = re.compile(r"(?:status(?:es)?/)(\d{2,25})")
META_RE = re.compile(
    r'<meta\s+(?:property|name)="([^"]+)"\s+content="([^"]*)"', re.S)
FULL_TEXT_RE = re.compile(r'full_text:"((?:[^"\\]|\\.)*)"')
SCREEN_RE = re.compile(r'screen_name:"([A-Za-z0-9_]{1,15})"')
CREATED_RE = re.compile(r'created_at_ms:(\d+)')
COUNT_RE = re.compile(
    r'(favorite_count|reply_count|retweet_count|quote_count):(\d+)')


def fail(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def parse_id(raw):
    raw = (raw or "").strip().strip("<>").strip()
    if not raw:
        fail("give a tweet URL or status ID, e.g. "
             "https://x.com/someone/status/1234567890")
    if re.fullmatch(r"\d{2,25}", raw):
        return raw
    m = ID_RE.search(raw)
    if m:
        return m.group(1)
    fail("could not find a numeric status ID in {0!r}; expected "
         ".../status/<digits>".format(raw))


def download(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            final = resp.geturl()
            return resp.read().decode("utf-8", "replace"), final
    except urllib.error.HTTPError as exc:
        raise RuntimeError("HTTP {0} from {1}".format(exc.code, url))
    except urllib.error.URLError as exc:
        raise RuntimeError("could not reach {0}: {1}".format(url, exc.reason))


def clean(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def js_unescape(raw):
    try:
        return json.loads('"' + raw + '"')
    except json.JSONDecodeError:
        return raw.replace('\\"', '"').replace("\\\\", "\\")


def meta_tags(page):
    tags = {}
    for name, value in META_RE.findall(page):
        tags.setdefault(name, html.unescape(value))
    return tags


def scrape_entries(page):
    """Every server-rendered tweet on the page, in document order."""
    entries = []
    for m in FULL_TEXT_RE.finditer(page):
        start = max(0, m.start() - 3000)
        before = page[start:m.start()]
        screens = SCREEN_RE.findall(before)
        created = CREATED_RE.findall(before)
        counts = dict(COUNT_RE.findall(before))
        entries.append({
            "author": screens[-1] if screens else "",
            "text": clean(js_unescape(m.group(1))),
            "created_ms": int(created[-1]) if created else None,
            "likes": int(counts["favorite_count"])
            if "favorite_count" in counts else None,
            "replies": int(counts["reply_count"])
            if "reply_count" in counts else None,
            "reposts": int(counts["retweet_count"])
            if "retweet_count" in counts else None,
            "quotes": int(counts["quote_count"])
            if "quote_count" in counts else None,
        })
    return entries


def stamp(ms):
    if not ms:
        return ""
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime(
        "%a %b %d %H:%M:%S %z %Y")


def scrape_one(status_id):
    """Scrape one status ID. Returns (record, path); fails on error."""
    url = "https://x.com/i/status/{0}".format(status_id)
    try:
        page, final_url = download(url)
    except RuntimeError as exc:
        fail(str(exc))

    tags = meta_tags(page)
    meta_text = clean(tags.get("og:description", ""))
    meta_author = (tags.get("twitter:creator", "") or "").lstrip("@")
    meta_date = tags.get("article:published_time", "")

    entries = [e for e in scrape_entries(page) if e["text"]]
    if not entries and not meta_text:
        fail("X returned a page with no tweet data for status {0} "
             "(deleted, protected, or login-walled). Try webfetch on "
             "https://x.com/i/status/{0} instead.".format(status_id))

    main = None
    if meta_text:
        for e in entries:
            if e["text"] == meta_text and \
                    (not meta_author or e["author"] == meta_author):
                main = e
                break
    if main is None and entries:
        main = entries[0]
    if main is None:
        main = {"author": meta_author or "unknown", "text": meta_text,
                "created_ms": None, "likes": None, "replies": None,
                "reposts": None, "quotes": None}

    seen = {(main["author"], main["text"])}
    comments = []
    for e in entries:
        key = (e["author"], e["text"])
        if key in seen or not e["author"]:
            continue
        seen.add(key)
        comments.append({"author": e["author"], "depth": 0, "text": e["text"]})

    created = stamp(main["created_ms"]) or meta_date
    author = main["author"] or meta_author or "unknown"
    m = ID_RE.search(final_url)
    if m:
        status_id = m.group(1)
    canonical = "https://x.com/{0}/status/{1}".format(author, status_id)

    record = {
        "source": "tweet",
        "id": status_id,
        "author": author,
        "author_name": "",
        "text": main["text"] or meta_text,
        "created_at": created,
        "likes": main["likes"],
        "retweets": main["reposts"],
        "replies": main["replies"],
        "quotes": main["quotes"],
        "views": None,
        "canonical_url": canonical,
        "comment_count": main["replies"],
        "returned": len(comments),
        "truncated": main["replies"] is not None and
        main["replies"] > len(comments),
        "article_url": None,
        "comments": comments,
    }

    os.makedirs(RUN_DIR, exist_ok=True)
    path = os.path.join(RUN_DIR, "tweet-{0}.json".format(status_id))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return record, path


def report(record, path):
    def num(value):
        return str(value) if value is not None else "?"

    print("Tweet file: {0}".format(path))
    print("Author:     @{0}".format(record["author"]))
    print("Date:       {0}".format(record["created_at"] or "?"))
    print("Text:       {0}".format(record["text"]))
    print("Stats:      {0} likes · {1} reposts · {2} replies · "
          "{3} quotes".format(
              num(record["likes"]), num(record["retweets"]),
              num(record["replies"]), num(record["quotes"])))
    print("Link:       {0}".format(record["canonical_url"]))
    print("Replies:    {0} captured{1}".format(
        record["returned"],
        " (thread is longer — enrich with webfetch/websearch)"
        if record["truncated"] else ""))
    for c in record["comments"][:8]:
        print("  @{0}: {1}".format(c["author"], c["text"][:160]))


def main():
    if len(sys.argv) < 2:
        fail("usage: fetch_tweet.py <tweet URL | numeric status ID> [...] "
             "(first input is the original post, the rest are related tweets)")
    ids = []
    for raw in sys.argv[1:]:
        sid = parse_id(raw)
        if sid not in ids:
            ids.append(sid)

    records = []
    for n, status_id in enumerate(ids, 1):
        if len(ids) > 1:
            print("--- tweet {0}/{1} ---".format(n, len(ids)))
        record, path = scrape_one(status_id)
        report(record, path)
        records.append(record)

    if len(ids) > 1:
        print("Scraped {0} tweets: {1}".format(
            len(ids), ", ".join(ids)))
        print("Original: {0}".format(records[0]["canonical_url"]))
    print("Next: read the tweet file(s), optionally webfetch the links and "
          "websearch the tweet IDs for more replies, then write the brief "
          "and run write_tweet_post.py. Do not write post files by hand.")


if __name__ == "__main__":
    main()
