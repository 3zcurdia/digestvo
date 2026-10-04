#!/usr/bin/env python3
"""Check one researcher brief and say exactly what to fix.

Usage:
    validate_brief.py <brief.json>

Exit 0 and print "OK" when the brief is usable. Otherwise print one line per
problem and exit 1. The brief has exactly five fields: category, readable,
summary, take, sentiment. Ids and URLs come from the story file, never from
the brief.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def check_text(name, text, sentences, words, problems):
    n_s, n_w = C.count_sentences(text), C.count_words(text)
    lo_s, hi_s = sentences
    lo_w, hi_w = words
    if n_s < lo_s:
        problems.append(
            "{0}: {1} sentence(s), need at least {2}. Add a real point, not padding."
            .format(name, n_s, lo_s))
    if n_s > hi_s:
        problems.append("{0}: {1} sentences, keep it to {2} or fewer.".format(name, n_s, hi_s))
    if n_w < lo_w:
        problems.append("{0}: {1} words, need at least {2}.".format(name, n_w, lo_w))
    if n_w > hi_w:
        problems.append("{0}: {1} words, cut to {2} or fewer.".format(name, n_w, hi_w))
    if re.search(r"[*_#`<>]|\\n", text):
        problems.append("{0}: plain prose only — no markdown, HTML, backticks or line breaks.".format(name))
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
        problems.append("{0}: remove the emoji.".format(name))
    if re.match(r"\s*(the (thread|discussion|article)|commenters were divided)", text, re.I) and name == "take":
        problems.append("take: do not open with 'The thread…'; start with the dominant view itself.")


def validate(path):
    problems = []
    if not os.path.isfile(path):
        return ["file not found: {0}".format(path)]
    if not C.parse_brief_name(path):
        problems.append("filename must be <hn|lobsters>-<id>.json inside {0}".format(C.BRIEFS_DIR))
    try:
        data = json.loads(C.read_text(path))
    except json.JSONDecodeError as exc:
        return ["not valid JSON ({0}). Write a bare JSON object, no code fence, no comments.".format(exc)]
    if not isinstance(data, dict):
        return ["top level must be a JSON object with the five brief fields"]

    for key, typ in C.BRIEF_FIELDS.items():
        if key not in data:
            problems.append("missing field: {0}".format(key))
        elif not isinstance(data[key], typ):
            problems.append("{0}: must be a {1}".format(key, "boolean" if typ is bool else "string"))
    if problems:
        return problems
    extra = sorted(set(data) - set(C.BRIEF_FIELDS))
    if extra:
        problems.append("remove extra field(s): {0}. Only the five brief fields are allowed.".format(", ".join(extra)))

    if data["category"] not in C.CATEGORIES:
        problems.append("category: {0!r} is not in the taxonomy. Pick one of: {1}".format(
            data["category"], " | ".join(C.CATEGORIES)))
    if data["sentiment"] not in C.SENTIMENTS:
        problems.append("sentiment: {0!r} must be one of: {1}".format(
            data["sentiment"], " | ".join(C.SENTIMENTS)))

    check_text("summary", data["summary"], C.SUMMARY_SENTENCES, C.SUMMARY_WORDS, problems)
    check_text("take", data["take"], C.TAKE_SENTENCES, C.TAKE_WORDS, problems)

    if data["readable"] is False and not re.search(
        r"could not (be )?(open|read|fetch|access)|paywall|not readable|unreadable|behind a", data["summary"], re.I
    ):
        problems.append("summary: readable is false, so say in the summary that the article could not be opened.")

    parsed = C.parse_brief_name(path)
    if parsed:
        story = C.story_path(*parsed)
        if not os.path.isfile(story):
            problems.append("story file missing: {0}. Run fetch.py story {1} {2} first.".format(story, *parsed))
        elif data["category"] == "Show HN" and parsed[0] == "lobsters":
            problems.append("category: Lobsters has no Show HN; use the bucket the project belongs to.")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("brief", help="path to <hn|lobsters>-<id>.json")
    args = parser.parse_args()
    problems = validate(args.brief)
    if problems:
        print("INVALID — fix these and run the validator again:")
        for p in problems:
            print("- " + p)
        sys.exit(1)
    data = json.loads(C.read_text(args.brief))
    print("OK — summary {0} words, take {1} words, category {2}, sentiment {3}".format(
        C.count_words(data["summary"]), C.count_words(data["take"]), data["category"], data["sentiment"]))


if __name__ == "__main__":
    main()
