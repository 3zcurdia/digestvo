#!/usr/bin/env python3
"""Write new posts and enrich existing ones from candidates.json.

Usage:
    write_post.py --keep 1,3,5          # row numbers from merge.py's table
    write_post.py --keep all
    write_post.py --keep 2 --dry-run    # show what would change, write nothing

For a `new` candidate it writes src/_posts/YYYY-MM-DD-<slug>.md from the
template shape. For a `refresh` candidate it edits the existing file: it
replaces only the take(s) for the source(s) researched today, appends a
missing source and its URL key, and never touches title, date, summary, tags
or existing keys. It then re-parses every file it touched and prints the
report block for the user.
"""

import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

REQUIRED_KEYS = ("layout", "title", "date", "categories", "source_url", "summary")


# ---------------------------------------------------------------- render ---

def render_body(sections):
    """sections: {source: take}. One source -> plain body; two -> lead-ins."""
    if len(sections) == 1:
        return C.wrap(next(iter(sections.values()))) + "\n"
    parts = []
    for s in C.SOURCE_ORDER:
        if s in sections:
            parts.append(C.wrap("**On {0}.** {1}".format(C.SOURCES[s]["label"], sections[s])))
    return "\n\n".join(parts) + "\n"


def render_new(cand, stamp):
    lines = [
        "---",
        "layout: post",
        "title: " + C.yaml_quote(cand["headline"]),
        "date: " + stamp,
        "categories: digest",
        "tags: [" + C.yaml_quote(cand["category"]) + "]",
    ]
    # A self post (Ask HN, Tell HN) has no article: the thread *is* the story,
    # so only the discussion link is drawn, not a duplicate "Read the original".
    if not cand.get("self_post"):
        lines.append("source_url: " + C.yaml_quote(cand["url"]))
    for s in C.SOURCE_ORDER:
        if s in cand["discussion_urls"]:
            lines.append("{0}: {1}".format(C.SOURCES[s]["key"], C.yaml_quote(cand["discussion_urls"][s])))
    lines.append("summary: >-")
    lines.append(C.wrap(cand["summary"], width=78, indent="  "))
    lines.append("---")
    return "\n".join(lines) + "\n\n" + render_body(cand["takes"])


def unique_path(posts_dir, day, slug):
    path = os.path.join(posts_dir, "{0}-{1}.md".format(day, slug))
    n = 2
    while os.path.exists(path):
        path = os.path.join(posts_dir, "{0}-{1}-{2}.md".format(day, slug, n))
        n += 1
    return path


# --------------------------------------------------------------- enrich ---

def add_key_line(fm_text, source, url):
    """Insert `<key>: "<url>"` after hn_url (for lobsters) or source_url (for hn)."""
    key = C.SOURCES[source]["key"]
    anchor = "hn_url" if source == "lobsters" else "source_url"
    lines = fm_text.split("\n")
    new_line = "{0}: {1}".format(key, C.yaml_quote(url))
    for i, line in enumerate(lines):
        if line.startswith(anchor + ":"):
            lines.insert(i + 1, new_line)
            return "\n".join(lines)
    # No anchor found: put it before summary, else at the end.
    for i, line in enumerate(lines):
        if line.startswith("summary:"):
            lines.insert(i, new_line)
            return "\n".join(lines)
    return fm_text + "\n" + new_line


def enrich(path, cand):
    original = C.read_text(path)
    parts = C.split_post(original)
    if not parts:
        raise C.DigestError("{0} has no front matter; refusing to edit".format(path))
    fm_text, body = parts
    keys = C.front_matter_keys(fm_text)
    existing_sources = [s for s in C.SOURCE_ORDER if keys.get(C.SOURCES[s]["key"])]

    sections = C.split_body_sections(body)
    if "_single" in sections:
        owner = existing_sources[0] if len(existing_sources) == 1 else (
            "hn" if "hn" in existing_sources or not existing_sources else existing_sources[0])
        sections = {owner: sections["_single"]} if sections["_single"] else {}

    replaced, added = [], []
    for s, take in cand["takes"].items():
        if s in sections:
            if sections[s] != take:
                replaced.append(s)
        else:
            added.append(s)
        sections[s] = take
        if not keys.get(C.SOURCES[s]["key"]):
            fm_text = add_key_line(fm_text, s, cand["discussion_urls"][s])
            if s not in added:
                added.append(s)

    new_text = "---\n" + fm_text + "\n---\n\n" + render_body(sections)
    if new_text == original:
        return original, None, [], [], []
    untouched = [s for s in sections if s not in cand["takes"]]
    return original, new_text, replaced, added, untouched


# -------------------------------------------------------------- verify ---

def verify(path):
    problems = []
    parts = C.split_post(C.read_text(path))
    if not parts:
        return ["no front matter"]
    keys = C.front_matter_keys(parts[0])
    for k in REQUIRED_KEYS:
        if k not in ("summary", "source_url") and not keys.get(k):
            problems.append("missing " + k)
    if "summary:" not in parts[0]:
        problems.append("missing summary")
    if not any(keys.get(C.SOURCES[s]["key"]) for s in C.SOURCE_ORDER):
        problems.append("no hn_url or lobsters_url")
    if not parts[1].strip():
        problems.append("empty body")
    ruby = shutil.which("ruby")
    if ruby:
        code = ("fm = File.read(ARGV[0]).split(/^---\\s*$/, 3)[1]; "
                "YAML.safe_load(fm, permitted_classes: [Date, Time])")
        res = subprocess.run([ruby, "-ryaml", "-rdate", "-e", code, path], capture_output=True, text=True)
        if res.returncode != 0:
            problems.append("front matter does not parse as YAML: " + res.stderr.strip().split("\n")[-1])
    return problems


# ---------------------------------------------------------------- main ---

def parse_keep(spec, rows):
    if spec.strip().lower() == "all":
        return sorted(rows)
    try:
        wanted = sorted({int(x) for x in spec.replace(",", " ").split()})
    except ValueError:
        C.fail("--keep wants row numbers like 1,3,5 or 'all'")
    missing = [n for n in wanted if n not in rows]
    if missing:
        C.fail("no such row(s) in the table: {0}".format(", ".join(map(str, missing))))
    if not wanted:
        C.fail("--keep is empty; nothing to publish")
    return wanted


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keep", required=True, help="row numbers from merge.py, or 'all'")
    parser.add_argument("--posts-dir", default=C.POSTS_DIR)
    parser.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = parser.parse_args()

    if not os.path.isfile(C.CANDIDATES_PATH):
        C.fail("{0} not found. Run merge.py first.".format(C.CANDIDATES_PATH))
    data = C.read_json(C.CANDIDATES_PATH)
    by_row = {c["row"]: c for c in data["candidates"]}
    keep = parse_keep(args.keep, set(by_row))
    os.makedirs(args.posts_dir, exist_ok=True)
    day, stamp = C.now_stamp()

    report = {"created": [], "updated": [], "unchanged": [], "failed": [], "kept_rows": keep,
              "dry_run": args.dry_run}
    for row in keep:
        cand = by_row[row]
        try:
            if cand["state"] == "new":
                path = unique_path(args.posts_dir, day, C.slugify(cand["headline"]))
                text = render_new(cand, stamp)
                if not args.dry_run:
                    C.write_text(path, text)
                report["created"].append({"row": row, "path": path, "headline": cand["headline"],
                                          "sources": cand["sources"]})
            else:
                path = cand["post_path"]
                result = enrich(path, cand)
                if result[1] is None:
                    report["unchanged"].append({"row": row, "path": path, "headline": cand["headline"]})
                else:
                    _, text, replaced, added, untouched = result
                    if not args.dry_run:
                        C.write_text(path, text)
                    report["updated"].append({"row": row, "path": path, "headline": cand["headline"],
                                              "replaced": replaced, "added": added, "untouched": untouched})
        except (C.DigestError, OSError) as exc:
            report["failed"].append({"row": row, "headline": cand["headline"], "error": str(exc)})

    if not args.dry_run:
        for entry in report["created"] + report["updated"]:
            problems = verify(entry["path"])
            if problems:
                entry["verify"] = problems
                report["failed"].append({"row": entry["row"], "headline": entry["headline"],
                                         "error": "written but failed verification: " + "; ".join(problems)})
        C.write_json(C.REPORT_PATH, report)

    # ---- the block the model copies into its final report ----
    touched = report["created"] + report["updated"]
    both = sum(1 for e in touched if len(by_row[e["row"]]["sources"]) == 2)
    lb_only = sum(1 for e in touched if by_row[e["row"]]["sources"] == ["lobsters"])
    hn_only = sum(1 for e in touched if by_row[e["row"]]["sources"] == ["hn"])
    print("{0}REPORT".format("DRY RUN — " if args.dry_run else ""))
    print("Candidates offered: {0}. Kept rows: {1}.".format(len(by_row), ", ".join(map(str, keep))))
    print("New posts: {0}. Refreshed posts: {1}. Unchanged: {2}. Failed: {3}.".format(
        len(report["created"]), len(report["updated"]), len(report["unchanged"]), len(report["failed"])))
    print("Of the posts written: {0} Hacker News only, {1} Lobsters only, {2} on both sites.".format(
        hn_only, lb_only, both))
    for e in report["created"]:
        print("- created {0}  ({1})".format(e["path"], "+".join(C.SOURCES[s]["short"] for s in e["sources"])))
    for e in report["updated"]:
        bits = []
        if e["replaced"]:
            bits.append("replaced take: " + ", ".join(C.SOURCES[s]["label"] for s in e["replaced"]))
        if e["added"]:
            bits.append("added source: " + ", ".join(C.SOURCES[s]["label"] for s in e["added"]))
        if e["untouched"]:
            bits.append("left alone: " + ", ".join(C.SOURCES[s]["label"] for s in e["untouched"]))
        print("- updated {0}  ({1})".format(e["path"], "; ".join(bits) or "no change"))
    for e in report["unchanged"]:
        print("- unchanged {0}  (fresh take identical to the stored one)".format(e["path"]))
    for e in report["failed"]:
        print("- FAILED row {0} {1}: {2}".format(e["row"], e["headline"], e["error"]))
    for source, msg in data.get("source_errors", {}).items():
        print("- SOURCE DOWN during fetch: {0} ({1})".format(source, msg))
    if data.get("skipped"):
        print("- {0} researcher brief(s) were invalid and skipped.".format(len(data["skipped"])))
    for row in keep:
        c = by_row[row]
        if c.get("alt_summary"):
            print("- row {0} had two summaries; the Hacker News one was used.".format(row))
    if not args.dry_run:
        print()
        print("Next: run `bundle exec rake deploy`. If it fails, paste the error in your report and stop.")
    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
