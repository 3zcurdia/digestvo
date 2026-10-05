#!/usr/bin/env python3
"""Write (or refresh) one digest post from scraped tweets and a brief.

Usage:
    write_tweet_post.py --tweets <id-or-URL,...> --brief <brief.json>
    write_tweet_post.py --tweets 20 --brief .opencode/tmp/digest/tweet-brief-20.json --dry-run

The first tweet is the original post; the rest are tweets related to it
(same thread, quote-tweets, notable replies). Every ID must already have
a tweet-<id>.json from fetch_tweet.py. The brief is written by the skill
(not by this script) and holds exactly four fields — title, category,
summary, take — validated here with the same rules as the digest
researcher briefs. Ids and URLs come from the tweet files, never from
the brief.

New posts go to src/_posts/YYYY-MM-DD-<slug>.md. When a post already
links one of the tweets (a re-run, or a related tweet added later), it is
refreshed in place: the take is replaced, missing related links are
appended, and title, date, summary, tags and existing keys are untouched.
Every file touched is re-parsed, and a REPORT block is printed.

Errors go to stderr with exit code 1.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "digest", "scripts"))
import _common as C  # noqa: E402
from fetch_tweet import parse_id  # noqa: E402
from validate_brief import check_text  # noqa: E402

REQUIRED_KEYS = ("layout", "title", "date", "categories", "tags",
                 "x_url", "summary")
BRIEF_FIELDS = {"title": str, "category": str, "summary": str, "take": str}
TITLE_WORDS = (2, 15)
TITLE_CHARS = 100
STATUS_RE = re.compile(r"/status/(\d{2,25})")


# ---------------------------------------------------------------- brief ---

def validate_brief(path):
    problems = []
    if not os.path.isfile(path):
        return None, ["file not found: {0}".format(path)]
    try:
        data = C.read_json(path)
    except (ValueError, OSError) as exc:
        return None, ["not valid JSON ({0}). Write a bare JSON object, "
                      "no code fence, no comments.".format(exc)]
    if not isinstance(data, dict):
        return None, ["top level must be a JSON object with: " +
                      ", ".join(sorted(BRIEF_FIELDS))]
    for key, typ in BRIEF_FIELDS.items():
        if key not in data:
            problems.append("missing field: {0}".format(key))
        elif not isinstance(data[key], typ):
            problems.append("{0}: must be a string".format(key))
    if problems:
        return None, problems
    extra = sorted(set(data) - set(BRIEF_FIELDS))
    if extra:
        problems.append("remove extra field(s): {0}. Only title, category, "
                        "summary and take are allowed.".format(", ".join(extra)))

    title = data["title"]
    n_w = C.count_words(title)
    if not (TITLE_WORDS[0] <= n_w <= TITLE_WORDS[1]):
        problems.append("title: {0} words, keep it {1} to {2}.".format(
            n_w, *TITLE_WORDS))
    if len(title) > TITLE_CHARS:
        problems.append("title: {0} characters, cut to {1} or "
                        "fewer.".format(len(title), TITLE_CHARS))
    if "\n" in title.strip():
        problems.append("title: one line only.")
    if re.search(r"[*_#`<>]", title):
        problems.append("title: plain prose only — no markdown or HTML.")
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", title):
        problems.append("title: remove the emoji.")

    if data["category"] not in C.CATEGORIES:
        problems.append("category: {0!r} is not in the taxonomy. Pick one "
                        "of: {1}".format(data["category"],
                                         " | ".join(C.CATEGORIES)))
    elif data["category"] == "Show HN":
        problems.append('category: tweets never take "Show HN"; use the '
                        "bucket the post belongs to.")

    check_text("summary", data["summary"], C.SUMMARY_SENTENCES,
               C.SUMMARY_WORDS, problems)
    check_text("take", data["take"], C.TAKE_SENTENCES, C.TAKE_WORDS,
               problems)
    if problems:
        return None, problems
    return data, []


# ---------------------------------------------------------------- posts ---

def tweet_ids_in_front_matter(fm_text):
    """Status IDs linked from x_url / related_x_urls / source_url lines."""
    ids = set()
    in_related = False
    for line in fm_text.split("\n"):
        if line.startswith(("x_url:", "source_url:")):
            ids.update(STATUS_RE.findall(line))
            in_related = False
        elif line.startswith("related_x_urls:"):
            in_related = True
        elif in_related:
            if re.match(r"\s+-\s+", line):
                ids.update(STATUS_RE.findall(line))
            elif line.strip():
                in_related = False
    return ids


def find_post(posts_dir, ids):
    """Path of the post already linking any of ids, or None."""
    if not os.path.isdir(posts_dir):
        return None
    for name in sorted(os.listdir(posts_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(posts_dir, name)
        parts = C.split_post(C.read_text(path))
        if not parts:
            continue
        if tweet_ids_in_front_matter(parts[0]) & set(ids):
            return path
    return None


def render_new(brief, original_url, related_urls, stamp):
    lines = [
        "---",
        "layout: post",
        "title: " + C.yaml_quote(brief["title"]),
        "date: " + stamp,
        "categories: digest",
        "tags: [" + C.yaml_quote(brief["category"]) + "]",
        # The thread is the story (like an Ask HN self post), so there is
        # no source_url — the tweet links below are the whole contract with
        # Shared::SourceLinks, which draws them.
        "x_url: " + C.yaml_quote(original_url),
    ]
    if related_urls:
        lines.append("related_x_urls:")
        for url in related_urls:
            lines.append("  - " + C.yaml_quote(url))
    lines.append("summary: >-")
    lines.append(C.wrap(brief["summary"], width=78, indent="  "))
    lines.append("---")
    return "\n".join(lines) + "\n\n" + C.wrap(brief["take"]) + "\n"


def unique_path(posts_dir, day, slug):
    path = os.path.join(posts_dir, "{0}-{1}.md".format(day, slug))
    n = 2
    while os.path.exists(path):
        path = os.path.join(posts_dir, "{0}-{1}-{2}.md".format(day, slug, n))
        n += 1
    return path


def status_of(url):
    m = STATUS_RE.search(url or "")
    return m.group(1) if m else None


def refresh(path, brief, original_url, related_urls):
    original = C.read_text(path)
    parts = C.split_post(original)
    if not parts:
        raise C.DigestError("{0} has no front matter; refusing to "
                            "edit".format(path))
    fm_text, _body = parts
    linked = tweet_ids_in_front_matter(fm_text)

    lines = fm_text.split("\n")
    added = []
    if "x_url:" not in fm_text and "source_url:" not in fm_text:
        for i, line in enumerate(lines):
            if line.startswith("summary:"):
                lines.insert(i, "x_url: " + C.yaml_quote(original_url))
                added.append(original_url)
                break
    missing = [u for u in related_urls if status_of(u) not in linked]
    if missing:
        block = ["related_x_urls:"] + ["  - " + C.yaml_quote(u) for u in missing]
        placed = False
        for i, line in enumerate(lines):
            if line.startswith("related_x_urls:"):
                j = i + 1
                while j < len(lines) and re.match(r"\s+-\s+", lines[j]):
                    j += 1
                lines[j:j] = ["  - " + C.yaml_quote(u) for u in missing]
                placed = True
                break
        if not placed:
            for i, line in enumerate(lines):
                if line.startswith("summary:"):
                    lines[i:i] = block
                    placed = True
                    break
            if not placed:
                lines += block
        added.extend(missing)

    new_text = ("---\n" + "\n".join(lines) + "\n---\n\n" +
                C.wrap(brief["take"]) + "\n")
    if new_text == original:
        return original, None, []
    return original, new_text, added


def verify(path):
    problems = []
    parts = C.split_post(C.read_text(path))
    if not parts:
        return ["no front matter"]
    keys = C.front_matter_keys(parts[0])
    for k in REQUIRED_KEYS:
        if k == "summary":
            if "summary:" not in parts[0]:
                problems.append("missing summary")
        elif not keys.get(k):
            problems.append("missing " + k)
    if not parts[1].strip():
        problems.append("empty body")
    ruby = shutil.which("ruby")
    if ruby:
        code = ("fm = File.read(ARGV[0]).split(/^---\\s*$/, 3)[1]; "
                "YAML.safe_load(fm, permitted_classes: [Date, Time])")
        res = subprocess.run([ruby, "-ryaml", "-rdate", "-e", code, path],
                             capture_output=True, text=True)
        if res.returncode != 0:
            problems.append("front matter does not parse as YAML: " +
                            res.stderr.strip().split("\n")[-1])
    return problems


# ----------------------------------------------------------------- main ---

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tweets", required=True,
                        help="comma/space-separated tweet IDs or URLs; first is the original post")
    parser.add_argument("--brief", required=True, help="path to the tweet brief JSON")
    parser.add_argument("--posts-dir", default=C.POSTS_DIR)
    parser.add_argument("--dry-run", action="store_true", help="validate and plan, write nothing")
    args = parser.parse_args()

    ids = []
    for raw in args.tweets.replace(",", " ").split():
        sid = parse_id(raw)
        if sid not in ids:
            ids.append(sid)

    brief, problems = validate_brief(args.brief)
    if problems:
        print("INVALID brief — fix these and run again:")
        for p in problems:
            print("- " + p)
        sys.exit(1)

    tweets = []
    for sid in ids:
        path = os.path.join(C.RUN_DIR, "tweet-{0}.json".format(sid))
        if not os.path.isfile(path):
            print("error: tweet file missing: {0}. Run fetch_tweet.py on "
                  "{1} first.".format(path, sid), file=sys.stderr)
            sys.exit(1)
        tweets.append(C.read_json(path))
    original_url = tweets[0]["canonical_url"]
    related_urls = [t["canonical_url"] for t in tweets[1:]]

    os.makedirs(args.posts_dir, exist_ok=True)
    day, stamp = C.now_stamp()

    report = {"created": None, "updated": None, "unchanged": None,
              "failed": None, "dry_run": args.dry_run}
    existing = find_post(args.posts_dir, ids)
    try:
        if existing is None:
            path = unique_path(args.posts_dir, day, C.slugify(brief["title"]))
            text = render_new(brief, original_url, related_urls, stamp)
            if not args.dry_run:
                C.write_text(path, text)
            report["created"] = path
        else:
            _, text, added = refresh(existing, brief, original_url, related_urls)
            if text is None:
                report["unchanged"] = existing
            else:
                if not args.dry_run:
                    C.write_text(existing, text)
                report["updated"] = {"path": existing, "added": added}
    except (C.DigestError, OSError) as exc:
        report["failed"] = str(exc)

    touched = report["created"] or (report["updated"] or {}).get("path")
    if touched and not args.dry_run:
        problems = verify(touched)
        if problems:
            report["failed"] = ("written but failed verification: " +
                                "; ".join(problems))

    print("{0}REPORT".format("DRY RUN — " if args.dry_run else ""))
    print("Original: {0}".format(original_url))
    print("Related tweets: {0}.".format(
        ", ".join(related_urls) if related_urls else "none"))
    print("Brief: {0!r}, category {1}, summary {2} words, take {3} "
          "words.".format(brief["title"], brief["category"],
                           C.count_words(brief["summary"]),
                           C.count_words(brief["take"])))
    if report["created"]:
        print("New post: {0}".format(report["created"]))
    if report["updated"]:
        added = report["updated"]["added"]
        print("Refreshed post: {0} (replaced take{1}).".format(
            report["updated"]["path"],
            "; added {0} related link(s)".format(len(added)) if added
            else ", no new links"))
    if report["unchanged"]:
        print("Unchanged: {0} (take and links already current).".format(
            report["unchanged"]))
    if report["failed"]:
        print("FAILED: {0}".format(report["failed"]))
    if not args.dry_run and not report["failed"]:
        print()
        print("Next: run `bundle exec rake deploy`. If it fails, paste the "
              "error in your report and stop.")
    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
