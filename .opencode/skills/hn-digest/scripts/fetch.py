#!/usr/bin/env python3
"""Fetch Hacker News front-page stories and comment threads.

Bundled with the hn-digest skill so each research subagent does not reinvent
HTML-stripping, entity-decoding, or the URL normalisation that lets the parent
digest skill notice a story appearing on both HN and Lobsters.

Usage:
    fetch.py front [--limit 8]
    fetch.py comments <item_id> [--max 60] [--chars 600] [--budget 40000]

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

SEARCH = "https://hn.algolia.com/api/v1/search"
ITEM = "https://hn.algolia.com/api/v1/items/{0}"
UA = "digestvo-hn-digest-skill/1.0 (newsletter aggregator)"

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
        fail("non-JSON response from {0}".format(url))


def fail(msg):
    print("fetch.py: " + msg, file=sys.stderr)
    sys.exit(1)


def clean(text):
    """Strip HN's HTML markup and decode entities, then collapse whitespace."""
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


def cmd_front(args):
    """Front-page stories, ranked toward substantive discussion."""
    url = "{0}?{1}".format(
        SEARCH, urllib.parse.urlencode({"tags": "front_page", "hitsPerPage": args.pool})
    )
    hits = fetch(url).get("hits") or []
    stories = []
    for h in hits:
        title = h.get("title") or ""
        points, comments = h.get("points") or 0, h.get("num_comments") or 0
        stories.append(
            {
                "source": "hn",
                "id": h.get("objectID"),
                "headline": title,
                "url": h.get("url"),
                "url_key": url_key(h.get("url")),
                "ask_hn": title.startswith(("Ask HN", "Show HN")),
                "points": points,
                "comment_count": comments,
                "discussion_url": "https://news.ycombinator.com/item?id={0}".format(
                    h.get("objectID")
                ),
                # Comments are weighted over points because the digest reports
                # the argument, not the applause.
                "weight": points + 3 * comments,
            }
        )
    stories.sort(key=lambda s: s["weight"], reverse=True)
    print(
        json.dumps(
            {"source": "hn", "count": len(stories), "stories": stories[: args.limit]},
            indent=2,
        )
    )


def cmd_comments(args):
    """Flatten a comment tree into capped, de-marked-up lines."""
    try:
        args.item_id = int(args.item_id)
    except ValueError:
        fail("HN item id must be an integer, got {0!r}".format(args.item_id))

    item = fetch(ITEM.format(args.item_id))
    comments = []

    def walk(node, depth):
        for child in node.get("children") or []:
            text = clean(child.get("text"))
            if text:
                comments.append(
                    {"author": child.get("author"), "depth": depth, "text": text}
                )
            walk(child, depth + 1)

    walk(item, 0)

    kept, spent, trimmed = comments[: args.max], 0, []
    for c in kept:
        room = args.budget - spent
        if room <= 0:
            break
        text = c["text"]
        if len(text) > args.chars:
            text = text[: args.chars].rsplit(" ", 1)[0] + " …"
        spent += len(text)
        trimmed.append({"author": c["author"], "depth": c["depth"], "text": text})

    print(
        json.dumps(
            {
                "source": "hn",
                "id": item.get("id"),
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

    front = sub.add_parser("front", help="list front-page stories")
    front.add_argument("--limit", type=int, default=8)
    front.add_argument("--pool", type=int, default=30)
    front.set_defaults(func=cmd_front)

    comments = sub.add_parser("comments", help="fetch a comment thread")
    comments.add_argument("item_id")
    comments.add_argument("--max", type=int, default=60, help="max comments to return")
    comments.add_argument("--chars", type=int, default=600, help="max chars per comment")
    comments.add_argument("--budget", type=int, default=40000, help="max total chars")
    comments.set_defaults(func=cmd_comments)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()