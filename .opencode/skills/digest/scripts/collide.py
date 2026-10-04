#!/usr/bin/env python3
"""Find digest posts that already exist, so the digest can enrich instead of duplicate.

A story can reappear on a front page across days, and running /digest twice on
one day is normal. Without this check each run writes a second post for the same
article, and the index fills with duplicates. For a story already published the
right move is to refresh only its comments summary, not to add a post.

Usage:
    collide.py [posts_dir]        # default: src/_posts

Output is JSON on stdout: one entry per post that carries a source_url, keyed
by the same url_key the fetch scripts produce so the parent can compare exactly.

The url_key() below MUST stay identical to the one in the worker scripts
(hn-digest/scripts/fetch.py, lb-digest/scripts/fetch.py). They are duplicated
rather than imported because each skill has to stand alone, which means a fix
to one is not automatically a fix to the others — drift here silently turns
into missed collisions. If you change one, change all three and re-check parity.
"""

import argparse
import glob
import html
import json
import os
import re
import sys
import urllib.parse

# Query params that identify the referrer rather than the page.
TRACKING = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "dclid", "igshid", "mc_cid", "mc_eid", "ref", "ref_src",
    "ref_url", "source", "spm", "at_medium", "at_campaign", "gift", "amp",
    "si", "s_cid", "sr_share", "guccounter", "yclid", "__twitter_impression",
    "mcg", "pk_campaign", "pk_kwd", "hsa_acc", "hsa_cam",
}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)
HN_ID = re.compile(r"news\.ycombinator\.com/item\?id=(\d+)")
LOBSTERS_ID = re.compile(r"lobste\.rs/s/([A-Za-z0-9]+)")


def url_key(url):
    """Byte-identical to the workers' url_key. Keep in sync — see module docstring."""
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


def front_matter(path):
    """Read top-level scalar keys from a post's front matter.

    Deliberately a flat line scan rather than a YAML parse: it only needs the
    handful of URL keys, and a real parser would also pull in PyYAML, which the
    repo does not depend on. Indented continuation lines (a `summary: >-` block)
    are skipped, so they can never be mistaken for top-level keys.
    """
    with open(path, encoding="utf-8", errors="replace") as fh:
        head = fh.read(8192)
    match = FRONT_MATTER.match(head)
    if not match:
        return {}
    keys = {}
    for line in match.group(1).split("\n"):
        if not line or line[0] in " \t-":
            continue
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        value = value.strip().strip("\"'")
        if value:
            keys[name.strip()] = html.unescape(value)
    return keys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "posts_dir",
        nargs="?",
        default="src/_posts",
        help="directory of Bridgetown posts (default: src/_posts)",
    )
    args = parser.parse_args()

    # A missing or empty posts directory means there is nothing to collide with,
    # which is the normal state right after a wipe — not a failure. Erroring here
    # would block the very first run of a fresh site.
    if not os.path.isdir(args.posts_dir):
        print(
            json.dumps(
                {
                    "posts_dir": args.posts_dir,
                    "exists": False,
                    "posts_scanned": 0,
                    "with_source_url": 0,
                    "posts": [],
                },
                indent=2,
            )
        )
        return

    posts = []
    for path in sorted(glob.glob(os.path.join(args.posts_dir, "*.md"))):
        data = front_matter(path)
        source = data.get("source_url", "")
        posts.append(
            {
                "path": path,
                "slug": os.path.splitext(os.path.basename(path))[0],
                "title": data.get("title"),
                "source_url": source,
                "url_key": url_key(source),
                "hn_id": (HN_ID.search(data.get("hn_url", "")) or [None, None])[1]
                if HN_ID.search(data.get("hn_url", ""))
                else None,
                "lobsters_id": (
                    LOBSTERS_ID.search(data.get("lobsters_url", "")) or [None, None]
                )[1]
                if LOBSTERS_ID.search(data.get("lobsters_url", ""))
                else None,
            }
        )

    tracked = [p for p in posts if p["url_key"]]
    print(
        json.dumps(
            {
                "posts_dir": args.posts_dir,
                "exists": True,
                "posts_scanned": len(posts),
                "with_source_url": len(tracked),
                "posts": tracked,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()