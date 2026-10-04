#!/usr/bin/env python3
"""List published digest posts with their url_key and discussion ids.

Usage:
    collide.py [posts_dir]        # default: src/_posts

merge.py calls this logic itself; the CLI exists for inspection. A missing or
empty posts directory is a normal state (fresh site), not an error.
"""

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def published(posts_dir=C.POSTS_DIR):
    if not os.path.isdir(posts_dir):
        return {"posts_dir": posts_dir, "exists": False, "posts_scanned": 0, "posts": []}
    posts = [C.post_record(p) for p in sorted(glob.glob(os.path.join(posts_dir, "*.md")))]
    tracked = [p for p in posts if p["url_key"] or p["hn_id"] or p["lobsters_id"]]
    return {"posts_dir": posts_dir, "exists": True, "posts_scanned": len(posts), "posts": tracked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posts_dir", nargs="?", default=C.POSTS_DIR)
    args = parser.parse_args()
    print(json.dumps(published(args.posts_dir), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
