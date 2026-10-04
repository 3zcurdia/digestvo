#!/usr/bin/env python3
"""Fetch the Hacker News and Lobsters front pages, and one story's thread.

Usage:
    fetch.py front [--hn 6] [--lb 5] [--min-hn-comments 15] [--min-lb-comments 5]
                   [--only hn|lobsters]
    fetch.py story <hn|lobsters> <id> [--max 60] [--chars 600] [--budget 15000]

`front` clears the run directory (.opencode/tmp/digest), writes front.json,
and prints the shortlist plus one ready-to-paste researcher prompt per story.
`story` writes story-<source>-<id>.json (story fields + trimmed comments) and
prints where the researcher must write its brief.

Both commands hit JSON APIs only (Algolia for HN, lobste.rs/*.json). Errors go
to stderr with exit code 1.
"""

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

HN_SEARCH = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"
HN_ITEM = "https://hn.algolia.com/api/v1/items/{0}"
LB_HOTTEST = "https://lobste.rs/hottest.json"
LB_ITEM = "https://lobste.rs/s/{0}.json"

SELF_POST_PREFIXES = ("Ask HN", "Show HN", "Tell HN", "Launch HN")


# ------------------------------------------------------------------ front ---

def hn_front():
    hits = C.fetch_json(HN_SEARCH).get("hits") or []
    stories = []
    for h in hits:
        title = h.get("title") or ""
        points, comments = h.get("points") or 0, h.get("num_comments") or 0
        sid = str(h.get("objectID"))
        stories.append({
            "source": "hn",
            "id": sid,
            "headline": title,
            "url": h.get("url"),
            "url_key": C.url_key(h.get("url")),
            "self_post": not h.get("url") or title.startswith(SELF_POST_PREFIXES),
            "points": points,
            "comment_count": comments,
            "discussion_url": "https://news.ycombinator.com/item?id={0}".format(sid),
            "tags_hint": [],
            # Comments outweigh points: the digest reports the argument.
            "weight": points + 3 * comments,
        })
    return stories


def lb_front():
    raw = C.fetch_json(LB_HOTTEST)
    if not isinstance(raw, list):
        raise C.DigestError("expected a JSON list from " + LB_HOTTEST)
    stories = []
    for s in raw:
        score, comments = s.get("score") or 0, s.get("comment_count") or 0
        discussion = s.get("comments_url") or ""
        sid = C.lobsters_id_from(discussion) or s.get("short_id") or ""
        stories.append({
            "source": "lobsters",
            "id": sid,
            "headline": s.get("title") or "",
            "url": s.get("url"),
            "url_key": C.url_key(s.get("url")),
            "self_post": not s.get("url"),
            "points": score,
            "comment_count": comments,
            "discussion_url": discussion,
            "tags_hint": s.get("tags") or [],
            "weight": score + 3 * comments,
        })
    return stories


def shortlist(stories, limit, min_comments):
    stories = sorted(stories, key=lambda s: s["weight"], reverse=True)
    picked = [s for s in stories if s["comment_count"] >= min_comments]
    if len(picked) < limit:
        # Not enough lively threads: top up with the heaviest thin ones so a
        # quiet day still produces a digest. They are flagged in the table.
        thin = [s for s in stories if s["comment_count"] < min_comments]
        picked += thin[: limit - len(picked)]
    return picked[:limit]


TOPIC_STOP = {
    "Show", "Ask", "Tell", "Launch", "The", "This", "That", "What", "When",
    "Why", "How", "With", "From", "Into", "Over", "Your", "Open", "Free",
    "New", "First", "Last", "Best", "Part", "Release", "Notes", "Using",
    "Build", "Building", "Making", "Guide", "Introducing", "Announcing",
}


def topic_tokens(headline):
    toks = re.findall(r"\b[A-Z][A-Za-z0-9.+-]{3,}\b", headline or "")
    return {t.rstrip(".") for t in toks if t not in TOPIC_STOP}


def same_topic_pairs(rows):
    pairs = []
    for i, a in enumerate(rows):
        for j in range(i + 1, len(rows)):
            b = rows[j]
            if a["url_key"] and a["url_key"] == b["url_key"]:
                pairs.append((a, b, "same article (both sites)"))
                continue
            shared = topic_tokens(a["headline"]) & topic_tokens(b["headline"])
            if shared:
                pairs.append((a, b, "share " + ", ".join(sorted(shared))))
    return pairs


def reset_run_dir():
    os.makedirs(C.BRIEFS_DIR, exist_ok=True)
    for path in glob.glob(os.path.join(C.RUN_DIR, "*.json")) + glob.glob(
        os.path.join(C.BRIEFS_DIR, "*.json")
    ):
        os.remove(path)


def researcher_prompt(story):
    return (
        "Research one story for the digestvo newsletter. Read {doc} and follow "
        "it exactly. Story: source={source} id={id} headline={headline}. "
        "Working directory is the repo root. Do not ask questions. Write "
        "nothing except the brief file. When done, reply with only the brief "
        "file path, or 'FAILED: <reason>'."
    ).format(
        doc=C.RESEARCHER_DOC,
        source=story["source"],
        id=story["id"],
        headline=C.yaml_quote(story["headline"]),
    )


def cmd_front(args):
    reset_run_dir()
    out = {"fetched_at": C.now_stamp()[1], "hn": [], "lobsters": [], "errors": {}}
    plan = []
    if args.only in (None, "hn"):
        plan.append(("hn", hn_front, args.hn, args.min_hn_comments))
    if args.only in (None, "lobsters"):
        plan.append(("lobsters", lb_front, args.lb, args.min_lb_comments))

    for source, fn, limit, min_c in plan:
        try:
            out[source] = shortlist(fn(), limit, min_c)
        except C.DigestError as exc:
            out["errors"][source] = str(exc)
            print("error: {0}: {1}".format(source, exc), file=sys.stderr)

    rows = out["hn"] + out["lobsters"]
    if not rows:
        C.write_json(C.FRONT_PATH, out)
        C.fail("no source could be fetched; nothing to research")

    for n, s in enumerate(rows, 1):
        s["row"] = n
    C.write_json(C.FRONT_PATH, out)

    print("Shortlist ({0} stories) -> {1}".format(len(rows), C.FRONT_PATH))
    print()
    print("| # | Src | id | pts | cmts | Headline |")
    print("|---|-----|----|-----|------|----------|")
    for s in rows:
        thin = ""
        min_c = args.min_hn_comments if s["source"] == "hn" else args.min_lb_comments
        if s["comment_count"] < min_c:
            thin = " (thin thread)"
        print("| {0} | {1} | {2} | {3} | {4} | {5}{6} |".format(
            s["row"], C.SOURCES[s["source"]]["short"], s["id"], s["points"],
            s["comment_count"], s["headline"].replace("|", "/"), thin,
        ))
    for source, msg in out["errors"].items():
        print()
        print("SOURCE DOWN: {0} could not be fetched ({1}). Continue with the other "
              "source and say so in the final report.".format(source, msg))

    pairs = same_topic_pairs(rows)
    if pairs:
        print()
        print("Possible same topic (research both anyway; merge.py and the user decide):")
        for a, b, why in pairs:
            print("- #{0} and #{1}: {2}".format(a["row"], b["row"], why))

    print()
    print("Researcher prompts — spawn one `general` subagent per line, all in one message:")
    print()
    for s in rows:
        print("[#{0}] {1}".format(s["row"], researcher_prompt(s)))
        print()


# ------------------------------------------------------------------ story ---

def trim_comments(comments, max_n, chars, budget):
    kept, spent, trimmed = comments[:max_n], 0, []
    for c in kept:
        if budget - spent <= 0:
            break
        text = c["text"]
        if len(text) > chars:
            text = text[:chars].rsplit(" ", 1)[0] + " …"
        spent += len(text)
        trimmed.append({**c, "text": text})
    return trimmed


def hn_story(story_id, args):
    if not story_id.isdigit():
        raise C.DigestError("an HN id is an integer, got {0!r}".format(story_id))
    item = C.fetch_json(HN_ITEM.format(story_id))
    comments = []

    def walk(node, depth):
        for child in node.get("children") or []:
            text = C.clean(child.get("text"))
            if text:
                comments.append({"author": child.get("author"), "depth": depth, "text": text})
            walk(child, depth + 1)

    walk(item, 0)
    title = item.get("title") or ""
    url = item.get("url")
    return {
        "headline": title,
        "url": url,
        "self_post": not url or title.startswith(SELF_POST_PREFIXES),
        "self_text": C.clean(item.get("text")),
        "points": item.get("points") or 0,
        "discussion_url": "https://news.ycombinator.com/item?id={0}".format(story_id),
        "tags_hint": [],
    }, comments


def lb_story(story_id, args):
    if not re.fullmatch(r"[A-Za-z0-9]+", story_id or ""):
        raise C.DigestError("a Lobsters short id is alphanumeric, got {0!r}".format(story_id))
    item = C.fetch_json(LB_ITEM.format(story_id))
    comments = []
    for c in item.get("comments") or []:
        if c.get("is_deleted") or c.get("is_moderated"):
            continue
        text = C.clean(c.get("comment_plain") or c.get("comment"))
        if text:
            comments.append({
                "author": c.get("commenting_user"),
                "depth": c.get("depth") or 0,
                "score": c.get("score") or 0,
                "text": text,
            })
    url = item.get("url")
    return {
        "headline": item.get("title") or "",
        "url": url,
        "self_post": not url,
        "self_text": C.clean(item.get("description_plain") or item.get("description")),
        "points": item.get("score") or 0,
        "discussion_url": item.get("comments_url") or "https://lobste.rs/s/{0}".format(story_id),
        "tags_hint": item.get("tags") or [],
    }, comments


def cmd_story(args):
    source, story_id = args.source, args.item_id
    try:
        head, comments = (hn_story if source == "hn" else lb_story)(story_id, args)
    except C.DigestError as exc:
        C.fail("{0} {1}: {2}".format(source, story_id, exc))

    trimmed = trim_comments(comments, args.max, args.chars, args.budget)
    record = {
        "source": source,
        "id": story_id,
        **head,
        "url_key": C.url_key(head["url"]),
        "comment_count": len(comments),
        "returned": len(trimmed),
        "truncated": len(comments) > len(trimmed),
        "weight": head["points"] + 3 * len(comments),
        "brief_path": C.brief_path(source, story_id),
        "comments": trimmed,
    }
    path = C.story_path(source, story_id)
    C.write_json(path, record)

    print("Story file: {0}".format(path))
    print("Headline:   {0}".format(record["headline"]))
    if record["self_post"]:
        print("Article:    none — this is a self post; skip webfetch, use self_text in the story file")
    else:
        print("Article:    {0}".format(record["url"]))
    print("Comments:   {0} total, {1} in the file".format(record["comment_count"], record["returned"]))
    print("Brief path: {0}".format(record["brief_path"]))
    print("Next: read the story file, read the article, write the brief, then run:")
    print("  python3 .opencode/skills/digest/scripts/validate_brief.py {0}".format(record["brief_path"]))


# ------------------------------------------------------------------- main ---

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    front = sub.add_parser("front", help="shortlist both front pages")
    front.add_argument("--hn", type=int, default=6, help="HN stories to keep (default 6)")
    front.add_argument("--lb", type=int, default=5, help="Lobsters stories to keep (default 5)")
    front.add_argument("--min-hn-comments", type=int, default=15)
    front.add_argument("--min-lb-comments", type=int, default=5)
    front.add_argument("--only", choices=["hn", "lobsters"], help="fetch one source only")
    front.set_defaults(func=cmd_front)

    story = sub.add_parser("story", help="fetch one story and its thread")
    story.add_argument("source", choices=["hn", "lobsters"])
    story.add_argument("item_id")
    story.add_argument("--max", type=int, default=60, help="max comments (default 60)")
    story.add_argument("--chars", type=int, default=600, help="max chars per comment")
    story.add_argument("--budget", type=int, default=15000, help="max total chars (default 15000)")
    story.set_defaults(func=cmd_story)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
