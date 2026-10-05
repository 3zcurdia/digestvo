---
name: tweet-digest
description: Digest one X post (and its replies) as a digestvo post in src/_posts/. Use when the user runs /tweet-digest or asks to digest, summarize, or publish a tweet, its replies, quote-tweets, or what people are saying about one or more tweet URLs.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# tweet-digest

You scrape, enrich, brief, publish, and report. Scripts do everything
mechanical. **Never write or edit a file under `src/_posts/` yourself —
`write_tweet_post.py` owns slugs, dates, YAML, and refreshes.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/tweet-digest/scripts/`.
- Run files: `.opencode/tmp/digest/` (`fetch_tweet.py` writes
  `tweet-<id>.json` per tweet; you write one `tweet-brief-<id>.json`).
- Input (`$ARGUMENTS`): one tweet URL, or several space/comma-separated
  ones. The **first is the original post**; the rest are tweets related to
  it (same thread, quote-tweets, notable replies) and are folded into the
  same post. Bare numeric status IDs are accepted. If empty, ask for at
  least one and stop.

## If something fails

| What happened | Do this |
|---|---|
| A script exits non-zero | Stop. Paste its error to the user. Do not improvise the result. |
| The scrape finds no tweet data | The post is deleted, protected, or login-walled. Say so and stop. |
| The brief is INVALID | Fix exactly what the script lists, then run the writer again. |
| Step 5 build fails | Paste the error. Do not edit the post to work around it. |

## Step 1 — Scrape

```sh
python3 .opencode/skills/tweet-digest/scripts/fetch_tweet.py $ARGUMENTS
```

Scrapes X directly (no API key, no browser) and prints each tweet with its
captured replies plus a `tweet-<id>.json` path. Duplicated IDs are scraped
once. A `truncated: true` file means the thread is longer than captured —
that is the usual case, and Step 2 decides whether it matters.

A headless browser was tried and rejected: X returns HTTP 403 to automated
Chromium while the same page serves the tweet and its top replies
server-rendered to plain HTTP.

## Step 2 — Enrich (only if the thread is longer than captured)

For each file with `truncated: true`, best-effort, in this order:

1. `webfetch` the canonical URL, then a `websearch` for the tweet ID or a
   distinctive quoted phrase plus `replies` / `quote-tweets`.
2. If a tweet links an article, `webfetch` it once so the summary describes
   what was actually posted.

Cap this at ~6 fetches total. The file's `comments` (author, depth, text,
in page order) are already read — prefer them over search snippets, and a
user-pasted thread over everything fetched. Never invent reply contents.

## Step 3 — Brief

Write `.opencode/tmp/digest/tweet-brief-<original id>.json`: exactly these
four fields, bare JSON, no code fence, no comments, no other fields:

```json
{
  "title": "The first tweet and its eighteen years of replies",
  "category": "Culture",
  "summary": "...",
  "take": "..."
}
```

- **title** — one line, 2–15 words, ≤100 characters, plain prose naming
  the post, not the tweet verbatim. No markdown, HTML, or emoji.
- **category** — one bucket from
  `.opencode/skills/digest/references/categories.md` (tweets never take
  `Show HN`). The thread is the story, so categorise what the *discussion*
  is about.
- **summary** — 3–5 sentences, 40–110 words: what the original post says
  plus the related tweets' context, standing alone on the index.
- **take** — 3–6 sentences, 60–200 words, in the researcher's voice
  (`.opencode/skills/digest/references/researcher.md`): "Most repliers land
  on X, because A. The sharpest objection is Y, because B." Name the
  specific thing being argued about; cover the related tweets where they
  change the picture. When only the top replies were captured, describe
  only those; if none could be read, say so in the first sentence.

## Step 4 — Write

```sh
python3 .opencode/skills/tweet-digest/scripts/write_tweet_post.py --tweets <ids-or-URLs> --brief <brief path>
```

Use the same inputs as Step 1. The script validates the brief (it prints
`INVALID` lines on failure), creates the post or refreshes the one already
linking these tweets — replacing only the take, appending missing related
links, leaving `title`, `date`, `summary`, `tags` untouched — verifies the
file, and prints a `REPORT` block.

## Step 5 — Build

```sh
bundle exec rake deploy
```

## Step 6 — Report

Paste the `REPORT` block from Step 4. Then add: whether the build passed
and any failures from Steps 1–4. Finish with the post path.
