#!/usr/bin/env python3
"""Join each fetched video with its analyst brief into one curatable row.

Prints the numbered table the skill curates from and writes candidates.json.
Rows are grouped: the ones worth publishing first, then the ones the analyst
passed on. Both are shown so nothing silently disappears, but only the first
group is worth the user's time.

Usage:
    python3 .opencode/skills/videos/scripts/merge.py
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def load_rows():
    """One row per video that has both a video file and a valid brief."""
    published = {rec["video_id"]: rec for rec in C.published_videos()}
    rows = []
    problems = []

    for brief_file in sorted(glob.glob(os.path.join(C.BRIEFS_DIR, "*.json"))):
        video_id = C.parse_brief_name(brief_file)
        if not video_id:
            continue
        video_file = C.video_json_path(video_id)
        if not os.path.isfile(video_file):
            problems.append("{0}: no video file — run fetch_video.py first".format(video_id))
            continue
        try:
            brief = C.read_json(brief_file)
            video = C.read_json(video_file)
        except (ValueError, OSError) as exc:
            problems.append("{0}: unreadable ({1})".format(video_id, exc))
            continue

        existing = published.get(video_id)
        rows.append({
            "video_id": video_id,
            "title": video.get("title") or "",
            "channel": video.get("channel") or "",
            "duration": video.get("duration_string"),
            "published": video.get("published"),
            "watched_at": None,
            "transcript_words": C.count_words(video.get("transcript")),
            "readable": bool(brief.get("readable")),
            "verdict": brief.get("verdict"),
            "category": brief.get("category"),
            "summary": brief.get("summary"),
            "insights": brief.get("insights") or [],
            "take": brief.get("take"),
            "state": "refresh" if existing else "new",
            "existing_path": existing["path"] if existing else None,
            "thumbnail_url": video.get("thumbnail_url"),
            "video_url": video.get("video_url") or C.watch_url(video_id),
            "skipped": video.get("skipped"),
        })

    # Carry the watch date over from the shortlist so write_video.py does not
    # have to remember where it came from.
    if os.path.isfile(C.FRONT_PATH):
        try:
            front = C.read_json(C.FRONT_PATH)
        except (ValueError, OSError):
            front = {}
        watched = {c["video_id"]: c.get("watched_at") for c in front.get("candidates", [])}
        for row in rows:
            row["watched_at"] = watched.get(row["video_id"])

    return rows, problems


def order(rows):
    """Recommended first, then by recency of the shortlist. Numbers stick."""
    return sorted(
        rows,
        key=lambda r: (0 if r["verdict"] == "recommend" else 1, r["video_id"]),
    )


def show(rows, label):
    if not rows:
        print("  {0}: none".format(label))
        return
    print("")
    print("  {0} ({1})".format(label, len(rows)))
    for row in rows:
        state = row["state"]
        if state == "refresh":
            state = "refresh " + os.path.basename(row["existing_path"])
        spoken = "{0} words".format(row["transcript_words"]) if row["transcript_words"] else "NO TRANSCRIPT"
        print("")
        print("    {0}. {1}".format(row["row"], row["title"]))
        print("       {0} · {1} · {2} · {3} · {4} · {5}".format(
            row["channel"] or "unknown channel",
            row["duration"] or "--:--",
            row["category"],
            state,
            spoken,
            "readable" if row["readable"] else "metadata only",
        ))
        print("       {0}".format(C.wrap(row["summary"] or "", width=68, indent="       ")))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()

    rows, problems = load_rows()
    if not rows:
        print("")
        print("  No briefs to merge. Spawn one analyst per video, writing to")
        print("  {0}/<video id>.json, then run this again.".format(C.BRIEFS_DIR))
        return 1

    rows = order(rows)
    for index, row in enumerate(rows, 1):
        row["row"] = index

    keep = [r for r in rows if r["verdict"] == "recommend"]
    passed = [r for r in rows if r["verdict"] != "recommend"]

    print("")
    show(keep, "WORTH YOUR TIME")
    show(passed, "PASSED ON")

    if problems:
        print("")
        print("  incomplete:")
        for problem in problems:
            print("  - " + problem)

    C.write_json(C.CANDIDATES_PATH, {"rows": rows})
    print("")
    print("  {0} of {1} recommended. Curate the recommended ones; the rest are reported, not asked about."
          .format(len(keep), len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())