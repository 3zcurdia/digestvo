---
name: hn-digest
description: Worker skill that scrapes the Hacker News front page, researches each shortlisted story and its comment thread in parallel subagents, and returns JSON briefs. It deliberately does NOT interview the user or write posts — the parent /digest skill does that after merging this with lb-digest. Load when the user runs /hn-digest or explicitly asks to scrape Hacker News for the digest. Do not auto-load for general news summarising.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# hn-digest

Input: a candidate count, default 6 (the prompt, or `$ARGUMENTS`).
Output: a single JSON object of research briefs, one per shortlisted HN story.

## This is a worker skill

It scrapes, researches, and stops. It does **not** ask the user anything, does
not choose what to publish, and writes no post files. The parent `/digest`
skill runs this and `lb-digest` as subagents, merges the two result sets, then
interviews the user and writes the posts. If the user invokes `/hn-digest`
directly, show them the briefs as a readable table and point them at `/digest`
for publishing.

Keeping the boundary sharp is the point: the interview, the category choice,
and the post format all live in exactly one place, so the two sources cannot
drift apart.

## Step 1 — Fetch the front page

```sh
python3 .opencode/skills/hn-digest/scripts/fetch.py front --limit 8
```

Hits the Algolia HN API — no scraping, no rate-limit drama. Returns `id`,
`headline`, `url`, `url_key`, `points`, `comment_count`, `discussion_url`, and
a `weight` of `points + 3 * comment_count`. Comments are weighted over points
because the digest reports the argument, not the applause.

`url_key` is the URL reduced to a stable identity (no scheme, no `www.`, no
tracking params, no trailing slash). Pass it through to the parent verbatim —
it is how a story that also ran on Lobsters gets recognised as the same story.
Do not recompute or tidy it.

If the script exits non-zero, say so plainly and stop. Do not fall back to
inventing a front page.

## Step 2 — Shortlist

Pick **6** (or whatever the user asked for) from the 8 fetched:

- Favour threads with 15+ comments. The "what people are saying" paragraph is
  the reason this digest exists, and a 3-comment thread has nothing to say.
  At most one thin thread is worth including.
- **De-duplicate by topic.** Three AI-launch stories on one front page is one
  story plus noise — keep the heaviest and drop the rest. Same for anything
  ongoing (a lawsuit, an outage, a company in crisis).
- Keep a mix of categories. Six stories that are all AI is not a digest, it is
  a fan page.

## Step 3 — Research each story in a subagent

Spawn one subagent per shortlisted story with the `general` agent type, **4 at a
time**, waiting for each batch before starting the next. More than ~6 concurrent
fetches starts tripping rate limits and makes failures hard to attribute.

Use this prompt verbatim, substituting the story's fields:

```
Research one Hacker News story for a newsletter digest. Return JSON only —
no prose before or after the object.

Story:
- Headline: {headline}
- Article URL: {url}          (null means Ask HN / Show HN: the story is the post)
- Thread: {discussion_url}
- {points} points, {comment_count} comments
- url_key: {url_key}          // return this EXACTLY as given, unedited

Steps:
1. Read the story. Use webfetch on {url}. If url is null, or the fetch fails,
   is paywalled, or returns a cookie/consent wall, do NOT guess at the content —
   set "readable": false and carry on using the thread.
2. Read the discussion:
     python3 .opencode/skills/hn-digest/scripts/fetch.py comments {id} --max 60
   The JSON gives author, nesting depth and clean plain text, pre-order so a
   reply follows what it answers. Raise --max for threads over 150 comments.
3. Return exactly this shape as bare JSON — no code fence wrapped around it, no
   preamble, no trailing commentary:

{
  "source": "hn",
  "url_key": "...",     // the url_key given above, exactly
  "headline": "...",    // as given above, verbatim
  "url": "...",         // the article URL
  "discussion_url": "...",
  "category": "...",    // one bucket from the taxonomy below
  "readable": true,     // false if the article could not be read
  "summary": "...",     // 3-4 sentences, 45-70 words: what it is, the
                        // specifics that matter, and why a reader should care
  "take": "...",        // 3-5 sentences, 70-110 words: the dominant view, the
                        // pushback, and the specifics people argue about
  "sentiment": "..."    // enthusiasm | skeptical | mixed | neutral
}

Both budgets are two-sided. The floor is a real requirement: a summary of one
sentence tells the reader nothing they could not get from the headline, and a
take of one sentence is not a summary of a discussion — it is a fragment. Three
sentences is the minimum for each, so if you only have two real points, find the
third rather than padding, and if you genuinely have fewer, say which part of
the picture is missing rather than inventing it.

The ceiling is also real: several subagents' briefs land in one parent context,
and a 300-word thread note crowds out the others. Measured output lands at ~69
words of summary and ~110 of take, which is what these ranges are set around.
These budgets are tighter than lb-digest's because an HN thread is long but
diffuse — there is more comment volume to compress, so the same sentence count
needs fewer words. Every reader who wants the full argument has the thread link;
your job is the shape of the argument, not its transcript.

Aim for the shape "most commenters land on X, on the grounds that A; the
sharpest objection is Y, because B" — one or two real positions developed, not a
survey of everyone who spoke. Naming the specific disagreement (a stale
benchmark, a $25k prize in scrip, a 4-of-6 HLA match) is what makes this worth
reading; "commenters were divided" is not.

Taxonomy — pick exactly one: AI/ML, Dev Tools, Security & Privacy, Startups &
Business, Systems & Infra, Science, Policy & Law, Web & Platforms, Hardware,
Show HN, Culture. The full rules, including the ties that come up weekly, are
in ../digest/references/categories.md.

sentiment describes the thread's mood, not the news. Use enthusiasm or
skeptical when one side clearly wins; reserve mixed for threads that split on
something substantive; use neutral for thin threads with no real argument.
```

If a brief comes back fenced or wrapped in prose, strip it — but if the content
is there, do not throw the subagent's work away over a formatting nit.

If a subagent fails outright, drop that story and carry on — five briefs is
fine. Never backfill a failed subagent with your own guess at the article.

## Return

Aggregate the surviving briefs into one object and print it as bare JSON, with
no commentary around it — the parent skill parses this directly:

```json
{
  "source": "hn",
  "count": 6,
  "stories": [
    {
      "source": "hn",
      "url_key": "aleph-alpha.com/en/blog/...",
      "headline": "Kolibri: A Sovereign Open-Weight Model",
      "url": "https://aleph-alpha.com/en/blog/...",
      "discussion_url": "https://news.ycombinator.com/item?id=49942706",
      "category": "AI/ML",
      "readable": true,
      "summary": "...",
      "take": "...",
      "sentiment": "mixed"
    }
  ]
}
```

Keep every field. `url_key` in particular is not optional — dropping it
silently splits a story that appeared on both sites into two posts.