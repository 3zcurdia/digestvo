#!/usr/bin/env python3
"""Join briefs with their story files, merge both-site stories, detect posts
that already exist, and print the table the user chooses from.

Usage:
    merge.py [--posts-dir src/_posts] [--merge 3,5 ...]

Reads .opencode/tmp/digest/briefs/*.json and the matching story files, writes
.opencode/tmp/digest/candidates.json and prints a numbered table. Row numbers
in that table are what write_post.py --keep refers to.

--merge A,B forces two rows from a previous run of this command to be treated
as the same article (for a near-duplicate the url_key missed). Repeatable.
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402
import collide  # noqa: E402
import validate_brief  # noqa: E402


def load_briefs():
    """-> (list of {story..., brief...}, list of skipped messages)."""
    items, skipped = [], []
    for path in sorted(glob.glob(os.path.join(C.BRIEFS_DIR, "*.json"))):
        parsed = C.parse_brief_name(path)
        if not parsed:
            skipped.append("{0}: bad filename".format(path))
            continue
        problems = validate_brief.validate(path)
        if problems:
            skipped.append("{0}: {1}".format(path, "; ".join(problems)))
            continue
        story = C.read_json(C.story_path(*parsed))
        brief = C.read_json(path)
        story.pop("comments", None)
        items.append({**story, **brief, "brief_path": path})
    return items, skipped


def effective_url(item):
    """Self posts have no article; the discussion is the thing to link."""
    return item.get("url") or item.get("discussion_url")


def group(items, forced_pairs):
    """Group briefs into candidates by exact url_key, plus forced pairs."""
    groups = {}
    order = []
    for it in items:
        key = C.url_key(effective_url(it))
        it["_key"] = key
        groups.setdefault(key, []).append(it)
        if key not in order:
            order.append(key)
    # Forced merges refer to row numbers from a previous candidates.json.
    if forced_pairs:
        previous = C.read_json(C.CANDIDATES_PATH)["candidates"] if os.path.isfile(C.CANDIDATES_PATH) else []
        by_row = {c["row"]: c for c in previous}
        for a, b in forced_pairs:
            if a not in by_row or b not in by_row:
                C.fail("--merge {0},{1}: no such rows in the previous table".format(a, b))
            ka, kb = by_row[a]["url_key"], by_row[b]["url_key"]
            if ka in groups and kb in groups and ka != kb:
                groups[ka].extend(groups.pop(kb))
                order.remove(kb)
    return [groups[k] for k in order]


def build_candidate(members, posts):
    members.sort(key=lambda m: C.SOURCE_ORDER.index(m["source"]))
    lead = members[0]  # HN first when both are present
    sources = {m["source"]: m for m in members}
    url = effective_url(lead)
    key = C.url_key(url)

    existing = None
    for p in posts:
        if p["url_key"] == key and key:
            existing = p
            break
        if "hn" in sources and p["hn_id"] and p["hn_id"] == sources["hn"]["id"]:
            existing = p
            break
        if "lobsters" in sources and p["lobsters_id"] and p["lobsters_id"] == sources["lobsters"]["id"]:
            existing = p
            break

    return {
        "headline": lead["headline"],
        "url": url,
        "url_key": key,
        "self_post": all(m.get("self_post") for m in members),
        "sources": list(sources),
        "both_sites": len(sources) == 2,
        "category": lead["category"],
        "summary": lead["summary"],
        "alt_summary": sources["lobsters"]["summary"] if len(sources) == 2 else None,
        "readable": all(m["readable"] for m in members),
        "sentiment": {s: m["sentiment"] for s, m in sources.items()},
        "discussion_urls": {s: m["discussion_url"] for s, m in sources.items()},
        "takes": {s: m["take"] for s, m in sources.items()},
        "ids": {s: m["id"] for s, m in sources.items()},
        "weight": sum(m["weight"] for m in members),
        "state": "refresh" if existing else "new",
        "post_path": existing["path"] if existing else None,
    }


def near_duplicates(cands):
    out = []
    for i, a in enumerate(cands):
        for b in cands[i + 1:]:
            ka, kb = a["url_key"], b["url_key"]
            if not ka or not kb or ka == kb:
                continue
            ha, pa = (ka.split("?")[0].split("/", 1) + [""])[:2]
            hb, pb = (kb.split("?")[0].split("/", 1) + [""])[:2]
            if ha != hb:
                continue
            if pa == pb or pa.startswith(pb + "/") or pb.startswith(pa + "/"):
                out.append((a["row"], b["row"]))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--posts-dir", default=C.POSTS_DIR)
    parser.add_argument("--merge", action="append", default=[], metavar="A,B",
                        help="treat rows A and B of the previous table as one article")
    args = parser.parse_args()

    forced = []
    for spec in args.merge:
        try:
            a, b = (int(x) for x in spec.split(","))
        except ValueError:
            C.fail("--merge wants two row numbers like 3,5")
        forced.append((a, b))

    items, skipped = load_briefs()
    if not items:
        C.fail("no valid briefs in {0}. Did the researchers finish?".format(C.BRIEFS_DIR))

    posts = collide.published(args.posts_dir)["posts"]
    cands = [build_candidate(g, posts) for g in group(items, forced)]
    cands.sort(key=lambda c: (not c["both_sites"], -c["weight"]))
    for n, c in enumerate(cands, 1):
        c["row"] = n
    dups = near_duplicates(cands)

    front = C.read_json(C.FRONT_PATH) if os.path.isfile(C.FRONT_PATH) else {}
    expected = len(front.get("hn", [])) + len(front.get("lobsters", []))
    out = {
        "candidates": cands,
        "briefs_used": len(items),
        "briefs_expected": expected,
        "skipped": skipped,
        "near_duplicates": dups,
        "source_errors": front.get("errors", {}),
    }
    C.write_json(C.CANDIDATES_PATH, out)

    print("Candidates ({0}) -> {1}".format(len(cands), C.CANDIDATES_PATH))
    print()
    print("| # | Article | Where | State | Category | Article read | Mood |")
    print("|---|---------|-------|-------|----------|--------------|------|")
    for c in cands:
        where = "+".join(C.SOURCES[s]["short"] for s in c["sources"])
        mood = ", ".join("{0} {1}".format(C.SOURCES[s]["short"], m) for s, m in c["sentiment"].items())
        state = "refresh (edits {0})".format(os.path.basename(c["post_path"])) if c["state"] == "refresh" else "new"
        print("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
            c["row"], c["headline"].replace("|", "/"), where, state, c["category"],
            "yes" if c["readable"] else "NO", mood))
    print()
    for c in cands:
        print("{0}. {1}".format(c["row"], c["summary"]))
    print()
    if expected and len(items) < expected:
        print("NOTE: {0} of {1} researchers delivered a valid brief.".format(len(items), expected))
    for s in skipped:
        print("SKIPPED: " + s)
    for source, msg in out["source_errors"].items():
        print("SOURCE DOWN: {0} ({1})".format(source, msg))
    for a, b in dups:
        print("NEAR-DUPLICATE: rows {0} and {1} share host and path. If they are the same "
              "article, rerun: merge.py --merge {0},{1}".format(a, b))
    both = [c for c in cands if c["both_sites"]]
    if both:
        print("BOTH SITES: rows {0} ran on Hacker News and Lobsters.".format(
            ", ".join(str(c["row"]) for c in both)))
    print()
    print("Next: ask the user which rows to keep, then run write_post.py --keep <rows>")


if __name__ == "__main__":
    main()
