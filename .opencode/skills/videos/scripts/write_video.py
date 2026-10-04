#!/usr/bin/env python3
"""Write the chosen videos as pages, and nothing else.

The model never writes a file under src/_videos/. This script owns the front
matter, the slug, the permalink, the thumbnail download and the in-place
refresh, then re-reads every file it touched to prove it is valid before
reporting.

A video already on the site is refreshed in place rather than duplicated, so a
second run cannot split one video's write-up across two URLs.

Usage:
    python3 .opencode/skills/videos/scripts/write_video.py --keep 1,2
    python3 .opencode/skills/videos/scripts/write_video.py --keep all
"""

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

# A key is present or absent, never empty. `permalink` is what actually shapes
# the URL; the collection's own template is only a fallback.
PUBLISHED_KEYS = ("title", "permalink", "date", "watched", "tags", "channel",
                  "channel_url", "video_id", "video_url", "duration",
                  "published", "verdict", "summary", "thumbnail")


def parse_keep(spec, rows):
    if spec == "all":
        return list(rows)
    wanted = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            C.fail("--keep takes row numbers from merge.py, not {0!r}".format(part))
        number = int(part)
        if not 1 <= number <= len(rows):
            C.fail("row {0} is out of range; merge.py listed 1 to {1}".format(number, len(rows)))
        wanted.append(rows[number - 1])
    return wanted


def safe_name(value, fallback):
    text = (value or "").strip()
    return text or fallback


def slug_for(row, taken):
    """A slug that is stable for a video and unique within the directory."""
    base = C.slugify(row["title"])
    slug, suffix = base, 2
    while slug in taken:
        slug = "{0}-{1}".format(base, suffix)
        suffix += 1
    return slug


def thumbnail_for(row, slug):
    """Download the thumbnail and return the site-relative path, or None.

    THUMBS_DIR is the on-disk path inside the source tree; the URL a page
    references drops the leading `src/`, because that is where Bridgetown's
    static-file reader picks things up from.
    """
    url = row.get("thumbnail_url")
    if not url:
        return None
    site_path = "/" + C.THUMBS_DIR.split("/", 1)[1] + "/{0}.jpg".format(slug)
    destination = os.path.join(C.THUMBS_DIR, "{0}.jpg".format(slug))
    try:
        C.download(url, destination)
    except C.VideoError as exc:
        print("       thumbnail skipped: {0}".format(exc))
        return None
    return site_path


def yaml_list(values):
    return "[" + ", ".join(C.yaml_quote(v) for v in values) + "]"


def render(row, slug, permalink, stamp, watched, thumbnail):
    """The whole file. `summary` is a folded block; insights are a YAML list
    rather than markup, so the layout can re-render them anywhere."""
    lines = ["---"]
    lines.append("layout: video")
    lines.append("title: " + C.yaml_quote(row["title"]))
    lines.append("permalink: " + C.yaml_quote(permalink))
    lines.append("date: " + stamp)
    if watched:
        lines.append("watched: " + watched)
    if row.get("category"):
        lines.append("tags: " + yaml_list([row["category"]]))
    if row.get("channel"):
        lines.append("channel: " + C.yaml_quote(safe_name(row["channel"], "Unknown")))
    if row.get("channel_url"):
        lines.append("channel_url: " + C.yaml_quote(row["channel_url"]))
    lines.append("video_id: " + C.yaml_quote(row["video_id"]))
    lines.append("video_url: " + C.yaml_quote(row["video_url"]))
    if row.get("duration"):
        lines.append("duration: " + C.yaml_quote(row["duration"]))
    if row.get("published"):
        lines.append("published: " + C.yaml_quote(row["published"]))
    lines.append("verdict: " + C.yaml_quote(safe_name(row.get("verdict"), "recommend")))
    lines.append("summary: >-")
    for line in C.wrap(row["summary"] or "", width=76).split("\n"):
        lines.append("  " + line)
    if thumbnail:
        lines.append("thumbnail: " + C.yaml_quote(thumbnail))
    lines.append("insights:")
    for insight in row.get("insights") or []:
        lines.append("  - " + C.yaml_quote(insight.strip()))
    lines.append("---")
    lines.append("")
    lines.append((row.get("take") or "").strip())
    lines.append("")
    return "\n".join(lines)


def existing_slug(row):
    """The slug already used on the site for this video, if any."""
    for record in C.published_videos():
        if record["video_id"] == row["video_id"]:
            return os.path.splitext(os.path.basename(record["path"]))[0], record["path"]
    return None, None


# Only recommendations are ever published — that is the whole point of the
# verdict. A skip that slips into --keep is reported and dropped rather than
# written, so a mistake costs a row and not a page nobody wanted.
RUBY_YAML_CHECK = (
    r"require 'yaml'; require 'date'; "
    r"fm = File.read(ARGV[0])[/\A---\s*\n(.*?)\n---\s*\n?/m, 1]; "
    r"abort('no front matter') if fm.nil?; "
    r"d = YAML.safe_load(fm, permitted_classes: [Date, Time], aliases: true); "
    r"abort('front matter is not a mapping') unless d.is_a?(Hash)"
)


def verify(path):
    """Re-read the file and check it parses. Returns a problem or None."""
    if not os.path.isfile(path):
        return "file was not created"
    text = C.read_text(path)
    parts = C.split_post(text)
    if not parts:
        return "no front matter"
    keys = C.front_matter_keys(parts[0])
    for key in ("title", "permalink", "video_id", "summary"):
        if not keys.get(key):
            return "front matter is missing {0}".format(key)
    if not parts[1].strip():
        return "body is empty"
    if not keys["permalink"].startswith("/videos/"):
        return "permalink is outside /videos/"
    try:
        subprocess.run(
            ["ruby", "-e", RUBY_YAML_CHECK, path],
            capture_output=True, text=True, timeout=60, check=True,
        )
    except subprocess.CalledProcessError as exc:
        return "YAML did not parse: {0}".format((exc.stderr or "").strip().splitlines()[-1:])
    except (subprocess.SubprocessError, OSError) as exc:
        return "could not run the YAML check: {0}".format(exc)
    return None


def write_one(row, stamp, fallback_date, taken):
    watched = row.get("watched_at") or fallback_date
    current, path = existing_slug(row)
    is_refresh = path is not None

    if not is_refresh:
        slug = slug_for(row, taken)
        taken.add(slug)
        path = os.path.join(C.VIDEOS_DIR, "{0}.md".format(slug))
    else:
        slug = current

    permalink = "/videos/{0}/".format(slug)
    thumbnail = thumbnail_for(row, slug)
    C.write_text(path, render(row, slug, permalink, stamp, watched, thumbnail))

    problem = verify(path)
    return {
        "video_id": row["video_id"],
        "title": row["title"],
        "channel": row.get("channel"),
        "path": path,
        "permalink": permalink,
        "state": "refresh" if is_refresh else "new",
        "thumbnail": thumbnail,
        "problem": problem,
    }


def report(results, kept, total):
    print("")
    print("REPORT")
    print("")
    for result in results:
        if result["problem"]:
            print("  BROKE  {0}".format(result["title"]))
            print("         {0}".format(result["problem"]))
            continue
        print("  {0:<7} {1}".format(result["state"], result["title"]))
        print("          {0}".format(result["path"]))
        print("          {0}{1}".format(
            result["permalink"], "  + thumbnail" if result["thumbnail"] else ""))
    broken = [r for r in results if r["problem"]]
    print("")
    print("  {0} written ({1} new, {2} refreshed, {3} broken) of {4} candidates."
          .format(len(results), sum(1 for r in results if r["state"] == "new"),
                  sum(1 for r in results if r["state"] == "refresh"), len(broken), total))
    C.write_json(C.REPORT_PATH, {"results": results, "kept": kept})
    return 1 if broken else 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keep", required=True,
                        help="Row numbers from merge.py, comma-separated, or 'all'")
    args = parser.parse_args()

    if not os.path.isfile(C.CANDIDATES_PATH):
        C.fail("no candidates at {0}. Run merge.py first.".format(C.CANDIDATES_PATH))
    rows = C.read_json(C.CANDIDATES_PATH).get("rows", [])
    if not rows:
        C.fail("candidates.json has no rows. Run merge.py first.")

    chosen = parse_keep(args.keep, rows)
    refused = [row for row in chosen if row.get("verdict") != "recommend"]
    chosen = [row for row in chosen if row.get("verdict") == "recommend"]
    if refused:
        print("")
        print("  REFUSED {0} row(s) the analyst passed on — only recommendations are published:".format(len(refused)))
        for row in refused:
            print("    {0}. {1}".format(row["row"], row["title"]))
    if not chosen:
        print("")
        print("  Nothing worth publishing was kept. Write nothing.")
        return 0

    _day, stamp = C.now_stamp()
    fallback_date = _day
    taken = set()
    results = []
    for row in chosen:
        results.append(write_one(row, stamp, fallback_date, taken))

    return report(results, [r["video_id"] for r in chosen], len(rows))


if __name__ == "__main__":
    sys.exit(main())