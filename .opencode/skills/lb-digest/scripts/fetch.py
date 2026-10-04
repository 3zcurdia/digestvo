#!/usr/bin/env python3
"""Fetch Lobsters hottest stories and their comment threads.

Bundled with the lb-digest skill so each research subagent does not reinvent
HTML-stripping, entity-decoding, or the URL normalisation that lets the parent
digest skill notice a story appearing on both Lobsters and Hacker News.

Usage:
    fetch.py front [--limit 6]
    fetch.py comments <short_id> [--max 40] [--chars 600] [--budget 30000]

Output is always JSON on stdout. Errors go to stderr with a non-zero exit code.
"""

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HOTTEST = "https://lobste.rs/hottest.json"
ITEM = "https://lobste.rs/s/{0}.json"
UA = "digestvo-lb-digest-skill/1.0 (newsletter aggregator)"

# Query params that identify the referrer rather than the page. Everything else
# is kept: a YouTube watch URL is entirely in its query string, so blanket
# query-stripping would merge every video into one entry. The list cannot be
# exhaustive — newsletters invent new referral params constantly — which is why
# the parent skill also compares host+path before assuming two cards are
# different stories.
TRACKING = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "dclid", "igshid", "mc_cid", "mc_eid", "ref", "ref_src",
    "ref_url", "source", "spm", "at_medium", "at_campaign", "gift", "amp",
    "si", "s_cid", "sr_share", "guccounter", "yclid", "__twitter_impression",
    "mcg", "pk_campaign", "pk_kwd", "hsa_acc", "hsa_cam",
}

TAG_RE = re.compile(r"<[^>]+>")


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        fail("HTTP {0} from {1}".format(exc.code, url))
    except urllib.error.URLError as exc:
        fail("could not reach {0}: {1}".format(url, exc.reason))
    except json.JSONDecodeError:
        fail(
            "non-JSON response from {0} (lobste.rs serves HTML to some clients; "
            "check the User-Agent)".format(url)
        )


def fail(msg):
    print("fetch.py: " + msg, file=sys.stderr)
    sys.exit(1)


def clean(text):
    """Collapse whitespace and decode entities.

    Lobsters ships `comment_plain`, so this rarely has markup to strip — the
    real work is unescaping entities like &amp; in a hand-typed comment.
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub(" ", text))).strip()


def url_key(url):
    """Reduce a URL to a comparable identity.

    The parent skill groups both sources by this exact string to find stories
    that appeared twice, so it must be stable and must NOT be fuzzy-matched by
    the model later. Scheme, www, tracking params and trailing slash are
    normalised away; the path keeps its case because paths are case-sensitive.
    """
    if not url:
        return ""
    parts = urllib.parse.urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = urllib.parse.unquote(parts.path or "").rstrip("/")
    kept = [
        (k, v)
        for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in TRACKING
    ]
    kept.sort()
    query = urllib.parse.urlencode(kept)
    return host + path + ("?" + query if query else "")


def short_id(discussion_url):
    """Pull the short id out of https://lobste.rs/s/<short_id>/<slug>."""
    match = re.search(r"/s/([^/?#]+)", discussion_url or "")
    return match.group(1) if match else ""


def cmd_front(args):
    """Hottest stories, ranked toward substantive discussion."""
    raw = fetch(HOTTEST)
    if not isinstance(raw, list):
        fail("expected a JSON list of stories from {0}".format(HOTTEST))

    stories = []
    for s in raw:
        score, comments = s.get("score") or 0, s.get("comment_count") or 0
        discussion = s.get("comments_url") or ""
        stories.append(
            {
                "source": "lobsters",
                "id": short_id(discussion),
                "headline": s.get("title") or "",
                "url": s.get("url"),
                "url_key": url_key(s.get("url")),
                "ask_hn": False,
                "score": score,
                "comment_count": comments,
                "discussion_url": discussion,
                "tags_hint": s.get("tags") or [],
                # Lobsters runs on a much smaller scale than HN, but that does
                # not matter here: this skill only ever ranks Lobsters against
                # Lobsters. The cross-source scale clash is the parent skill's
                # problem, and it resolves it with per-source quotas instead.
                "weight": score + 3 * comments,
            }
        )
    stories.sort(key=lambda s: s["weight"], reverse=True)
    print(
        json.dumps(
            {
                "source": "lobsters",
                "count": len(stories),
                "stories": stories[: args.limit],
            },
            indent=2,
        )
    )


def cmd_comments(args):
    """Lobsters threads are flat-ish, short, and come with real nesting depth."""
    if not re.fullmatch(r"[A-Za-z0-9]+", args.item_id or ""):
        fail("Lobsters short id looks wrong: {0!r}".format(args.item_id))

    item = fetch(ITEM.format(args.item_id))
    comments = []
    for c in item.get("comments") or []:
        if c.get("is_deleted") or c.get("is_moderated"):
            continue
        text = clean(c.get("comment_plain") or c.get("comment"))
        if not text:
            continue
        comments.append(
            {
                "author": c.get("commenting_user"),
                "depth": c.get("depth") or 0,
                "score": c.get("score") or 0,
                "in_reply_to": c.get("parent_comment"),
                "text": text,
            }
        )

    kept, spent, trimmed = comments[: args.max], 0, []
    for c in kept:
        room = args.budget - spent
        if room <= 0:
            break
        text = c["text"]
        if len(text) > args.chars:
            text = text[: args.chars].rsplit(" ", 1)[0] + " …"
        spent += len(text)
        trimmed.append({**c, "text": text})

    print(
        json.dumps(
            {
                "source": "lobsters",
                "id": item.get("short_id") or args.item_id,
                "headline": item.get("title"),
                "url": item.get("url"),
                "total_comments": len(comments),
                "returned": len(trimmed),
                "truncated": len(comments) > len(trimmed),
                "comments": trimmed,
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    front = sub.add_parser("front", help="list hottest stories")
    front.add_argument("--limit", type=int, default=6)
    front.set_defaults(func=cmd_front)

    comments = sub.add_parser("comments", help="fetch a comment thread")
    comments.add_argument("item_id", help="the short id from the front listing")
    comments.add_argument("--max", type=int, default=40, help="max comments to return")
    comments.add_argument("--chars", type=int, default=600, help="max chars per comment")
    comments.add_argument("--budget", type=int, default=30000, help="max total chars")
    comments.set_defaults(func=cmd_comments)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()