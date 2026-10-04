#!/usr/bin/env python3
"""Turn your YouTube watch history into a numbered shortlist.

Reads your history through yt-dlp using your own browser session, falling back
to a Google Takeout export when there is no session. Writes front.json and
prints the table the skill curates from.

This script never writes to YouTube. It asks yt-dlp to list, and that is all.

Usage:
    python3 .opencode/skills/videos/scripts/candidates.py [options]

Options:
    --source history|watch-later|both   What to read. Default: history
    --days N                  Only videos watched in the last N days.
                              Default: 30. Needs timestamps; ignored when the
                              session path supplies no watch dates.
    --limit N                 Cap the shortlist. Default: 20
    --history PATH            Takeout watch-history.json, overriding
                              ~/.config/digestvo/takeout.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

SOURCES = {
    "history": {"label": "watch history", "url": C.HISTORY_FEED},
    "watch-later": {"label": "Watch Later", "url": C.WATCH_LATER_FEED},
}
# How many entries to pull per feed before filtering. YouTube serves a long
# first page, so this is generous rather than tight.
FEED_PAGES = 120


def from_session(source, limit):
    """Entries from a YouTube feed or playlist, via cookies. [] on any failure."""
    if not C.cookies_available():
        return []
    args = C.ytdlp_base_args() + C.cookies_args() + [
        "--flat-playlist",
        "--dump-single-json",
        "--playlist-end", str(FEED_PAGES),
    ]
    if limit:
        args += ["--playlist-items", "1:{0}".format(limit)]
    args.append(SOURCES[source]["url"])
    try:
        payload = C.run_ytdlp(args, timeout=120)
    except C.VideoError:
        return []
    try:
        entries = (json.loads(payload) or {}).get("entries") or []
    except ValueError:
        return []
    return [e for e in entries if isinstance(e, dict)]


def takeout_path(override):
    if override:
        return override
    if not os.path.isfile(C.TAKEOUT_PATH):
        return None
    try:
        return C.read_json(C.TAKEOUT_PATH).get("watch_history")
    except (ValueError, OSError):
        return None


def from_takeout(path):
    """(ordered ids, {id: {"watched_at", "times"}}) from a Takeout export.

    Takeout ships the whole history newest-first in one file. Ads have no
    titleUrl and are dropped; the "Watched " prefix is what separates a real
    watch from a "Visited" or "Liked" row.
    """
    if not path or not os.path.isfile(path):
        return [], {}
    try:
        rows = C.read_json(path)
    except (ValueError, OSError):
        return [], {}
    if not isinstance(rows, list):
        return [], {}

    stamps = {}
    ordered = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        products = row.get("products") or []
        title = row.get("title") or ""
        if "YouTube" not in products or not title.startswith("Watched "):
            continue
        url = row.get("titleUrl") or ""
        video_id = C.video_id_from(url)
        if not video_id or "music.youtube.com" in url or "/shorts/" in url:
            continue
        when = parse_time(row.get("time"))
        if video_id in stamps:
            stamps[video_id]["times"] += 1
            if when and when > stamps[video_id]["watched_at"]:
                stamps[video_id]["watched_at"] = when
        else:
            stamps[video_id] = {"watched_at": when, "times": 1}
            ordered.append(video_id)

    ordered.sort(
        key=lambda vid: stamps[vid]["watched_at"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return ordered, stamps


def parse_time(value):
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def build(source, limit, days, history_override):
    """Ordered, deduplicated, filtered candidates with whatever dates we have."""
    takeout_ids, stamps = from_takeout(takeout_path(history_override))
    used = []

    entries = []
    wanted = ["history", "watch-later"] if source == "both" else [source]
    for name in wanted:
        found = from_session(name, FEED_PAGES)
        if found:
            entries.extend(found)
            used.append("{0} via session".format(SOURCES[name]["label"]))
        else:
            used.append("{0}: no session data".format(SOURCES[name]["label"]))

    if entries:
        order = []
        for entry in entries:
            video_id = entry.get("id") or C.video_id_from(entry.get("url"))
            if video_id and video_id not in order:
                order.append(video_id)
    elif takeout_ids:
        order = takeout_ids
    else:
        return [], {}, used, 0

    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)) if days else None
    candidates = []
    for video_id in order:
        stamp = stamps.get(video_id, {})
        watched_at = stamp.get("watched_at")
        # The window only applies where we actually know when it was watched.
        # Session-only entries come from a feed that is already newest-first.
        if cutoff and watched_at and watched_at < cutoff:
            continue
        candidates.append({
            "video_id": video_id,
            "watched_at": watched_at.strftime("%Y-%m-%d") if watched_at else None,
            "times": stamp.get("times", 0),
        })
        if len(candidates) >= limit:
            break

    undated = sum(1 for c in candidates if not c["watched_at"])
    return candidates, stamps, used, undated


def table(candidates, stamps):
    print("")
    print("  #  Watched    Times  Video")
    print("  " + "-" * 72)
    for index, item in enumerate(candidates, 1):
        when = item["watched_at"] or "unknown"
        times = str(item["times"]) if item["times"] else "-"
        print("  {0:<2} {1:<10} {2:<6} {3}".format(index, when, times, item["video_id"]))
    print("")
    print("  {0} candidates. Run fetch_video.py --from-candidates next.".format(len(candidates)))


def main():
    parser = argparse.ArgumentParser(description="Shortlist videos from your watch history.")
    parser.add_argument("--source", choices=sorted(SOURCES) + ["both"], default="history")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--history", help="Takeout watch-history.json to read instead")
    args = parser.parse_args()

    C.clear_run_dir()
    candidates, _stamps, used, undated = build(args.source, args.limit, args.days, args.history)

    print("")
    for line in used:
        print("  source: " + line)
    if undated:
        print("  note:   {0} have no watch date; they will be dated when written".format(undated))

    if not candidates:
        print("")
        print("  NOTHING FOUND.")
        print("  Check that {0} exists and is a real export.".format(C.COOKIES_PATH))
        print("  See references/setup.md, or pass explicit ids to fetch_video.py.")
        return 1

    C.write_json(C.FRONT_PATH, {"source": args.source, "candidates": candidates})
    table(candidates, _stamps)
    return 0


if __name__ == "__main__":
    sys.exit(main())