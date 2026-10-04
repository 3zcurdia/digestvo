#!/usr/bin/env python3
"""Check one analyst brief and say exactly what to fix.

Usage:
    validate_brief.py <brief.json>

Exit 0 and print "OK" when the brief is usable. Otherwise print one line per
problem and exit 1. The brief has exactly six fields: category, readable,
verdict, summary, insights, take. Ids, URLs and metadata come from the video
file, never from the brief.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
MARKUP_RE = re.compile(r"[*_#`<>]|\\n")


def check_text(name, text, sentences, words, problems, opener_re=None):
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
    if MARKUP_RE.search(text):
        problems.append(
            "{0}: plain prose only — no markdown, HTML, backticks or line breaks.".format(name))
    if EMOJI_RE.search(text):
        problems.append("{0}: remove the emoji.".format(name))
    if opener_re and re.match(opener_re, text, re.I):
        problems.append(
            "{0}: do not open with 'This video…' or 'In this video…' — start at the point.".format(name))


def validate(path):
    problems = []
    if not os.path.isfile(path):
        return ["file not found: {0}".format(path)]
    video_id = C.parse_brief_name(path)
    if not video_id:
        problems.append(
            "filename must be <video id>.json inside {0}".format(C.BRIEFS_DIR))
    try:
        data = json.loads(C.read_text(path))
    except json.JSONDecodeError as exc:
        return ["not valid JSON ({0}). Write a bare JSON object, no code fence, no comments.".format(exc)]
    if not isinstance(data, dict):
        return ["top level must be a JSON object with the six brief fields"]

    for key, typ in C.BRIEF_FIELDS.items():
        if key not in data:
            problems.append("missing field: {0}".format(key))
        elif not isinstance(data[key], typ):
            label = "boolean" if typ is bool else ("array of strings" if typ is list else "string")
            problems.append("{0}: must be {1} {2}".format(key, "a" if label[0] in "aeiou" else "an", label))
    if problems:
        return problems

    extra = sorted(set(data) - set(C.BRIEF_FIELDS))
    if extra:
        problems.append(
            "remove extra field(s): {0}. Only the six brief fields are allowed."
            .format(", ".join(extra)))

    if data["category"] not in C.CATEGORIES:
        problems.append("category: {0!r} is not in the taxonomy. Pick one of: {1}".format(
            data["category"], " | ".join(C.CATEGORIES)))
    if data["verdict"] not in C.VERDICTS:
        problems.append("verdict: {0!r} must be one of: {1}".format(
            data["verdict"], " | ".join(C.VERDICTS)))

    check_text("summary", data["summary"], C.SUMMARY_SENTENCES, C.SUMMARY_WORDS, problems,
               opener_re=r"\s*(this|in) (video|talk|episode)\b")
    check_text("take", data["take"], C.TAKE_SENTENCES, C.TAKE_WORDS, problems,
               opener_re=r"\s*(this|in) (video|talk|episode)\b")

    insights = data["insights"]
    lo, hi = C.INSIGHT_COUNT
    if not C.in_range(len(insights), C.INSIGHT_COUNT):
        problems.append("insights: {0} entries, need {1} to {2}. Each is a point worth "
                        "remembering, not a paragraph.".format(len(insights), lo, hi))
    else:
        lo_w, hi_w = C.INSIGHT_WORDS
        for index, item in enumerate(insights, 1):
            if not isinstance(item, str):
                problems.append("insights[{0}]: must be a string".format(index))
                continue
            words = C.count_words(item)
            if words < lo_w:
                problems.append("insights[{0}]: {1} words, need at least {2}."
                                .format(index, words, lo_w))
            if words > hi_w:
                problems.append("insights[{0}]: {1} words, cut to {2} or fewer."
                                .format(index, words, hi_w))
            if MARKUP_RE.search(item):
                problems.append("insights[{0}]: plain prose only — no markdown or backticks."
                                .format(index))
            if EMOJI_RE.search(item):
                problems.append("insights[{0}]: remove the emoji.".format(index))

    if data["readable"] is False and not re.search(
            r"could not (be )?(watch|read|listen|transcrib|play|access)|no (captions|transcript|"
            r"audio)|only the (title|description|metadata)", data["summary"], re.I):
        problems.append(
            "summary: readable is false, so say in the summary that the video could not be "
            "watched and describe what is known from its metadata instead.")

    if video_id:
        source = C.video_json_path(video_id)
        if not os.path.isfile(source):
            problems.append("video file missing: {0}. Run fetch_video.py first.".format(source))
    return problems


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("brief", help="path to <video id>.json")
    args = parser.parse_args()
    problems = validate(args.brief)
    if problems:
        print("INVALID — fix these and run the validator again:")
        for problem in problems:
            print("- " + problem)
        sys.exit(1)
    data = json.loads(C.read_text(args.brief))
    print("OK — verdict {0}, category {1}, summary {2} words, {3} insights, take {4} words".format(
        data["verdict"], data["category"], C.count_words(data["summary"]),
        len(data["insights"]), C.count_words(data["take"])))


if __name__ == "__main__":
    main()