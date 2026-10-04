---
name: lb-digest
description: Worker skill that scrapes the Lobsters hottest page, researches each shortlisted story and its comment thread in parallel subagents, and returns JSON briefs. It deliberately does NOT interview the user or write posts — the parent /digest skill does that after merging this with hn-digest. Load when the user runs /lb-digest or explicitly asks to scrape Lobsters for the digest. Do not auto-load for general news summarising.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# lb-digest

Input: a candidate count, default 5 (the prompt, or `$ARGUMENTS`).
Output: a single JSON object of research briefs, one per shortlisted Lobsters
story.

## This is a worker skill

It scrapes, researches, and stops. It does **not** ask the user anything, does
not choose what to publish, and writes no post files. The parent `/digest`
skill runs this and `hn-digest` as subagents, merges the two result sets, then
interviews the user and writes the posts. If the user invokes `/lb-digest`
directly, show them the briefs as a readable table and point them at `/digest`
for publishing.

Keeping the boundary sharp is the point: the interview, the category choice,
and the post format all live in exactly one place, so the two sources cannot
drift apart.

## Step 1 — Fetch the hottest page

```sh
python3 .opencode/skills/lb-digest/scripts/fetch.py front --limit 7
```

Hits the Lobsters JSON API — no scraping. Returns `id` (the short id used by
the comments endpoint), `headline`, `url`, `url_key`, `score`,
`comment_count`, `discussion_url`, `tags_hint`, and a `weight` of
`score + 3 * comment_count`.

`url_key` is the URL reduced to a stable identity (no scheme, no `www.`, no
tracking params, no trailing slash). Pass it through to the parent verbatim —
it is how a story that also ran on Hacker News gets recognised as the same
story. Do not recompute or tidy it.

If the script exits non-zero, say so plainly and stop. Do not fall back to
inventing a front page.

## Step 2 — Shortlist

Pick **5** (or whatever the user asked for) from the 7 fetched:

- Favour threads with 5+ comments. Lobsters threads are genuinely short — a
  7-comment thread is a healthy thread *for Lobsters*, not a thin one. Judging
  it against Hacker News norms would reject nearly the whole site.
- **De-duplicate by topic.** Two Rust compiler posts on one page is one story
  plus noise — keep the heavier and drop the rest.
- Keep a mix of categories, and prefer posts that are not already likely to be
  on HN. The parent merges by `url_key`, so a story both sites ran becomes one
  post carrying both icons — high value, but the digest is more worth reading
  when it is not *only* stories HN already surfaced.

## Step 3 — Research each story in a subagent

Spawn one subagent per shortlisted story with the `general` agent type, **4 at a
time**, waiting for each batch before starting the next. More than ~6 concurrent
fetches starts tripping rate limits and makes failures hard to attribute.

Use this prompt verbatim, substituting the story's fields:

```
Research one Lobsters story for a newsletter digest. Return JSON only —
no prose before or after the object.

Story:
- Headline: {headline}
- Article URL: {url}
- Thread: {discussion_url}   (short id: {id})
- {score} score, {comment_count} comments
- Lobsters' own tags: {tags_hint}   // a hint for categorising, not the answer
- url_key: {url_key}          // return this EXACTLY as given, unedited

Steps:
1. Read the story. Use webfetch on {url}. If the fetch fails, is paywalled, or
   returns a cookie/consent wall, do NOT guess at the content — set
   "readable": false and carry on using the discussion.
2. Read the discussion:
     python3 .opencode/skills/lb-digest/scripts/fetch.py comments {id}
   The JSON gives commenter, nesting depth, score and comment_plain, with
   deleted and moderated comments already removed.
3. Return exactly this shape as bare JSON — no code fence wrapped around it, no
   preamble, no trailing commentary:

{
  "source": "lobsters",
  "url_key": "...",     // the url_key given above, exactly
  "headline": "...",    // as given above, verbatim
  "url": "...",         // the article URL
  "discussion_url": "...",
  "category": "...",    // one bucket from the taxonomy below
  "readable": true,     // false if the article could not be read
  "summary": "...",     // 3-4 sentences, 70-95 words: what it is, the
                        // specifics that matter, and why a reader should care
  "take": "...",        // 3-5 sentences, 110-160 words: the dominant view, the
                        // pushback, and the specifics people argue about
  "sentiment": "..."    // enthusiasm | skeptical | mixed | neutral
}

Lobsters threads are small, so "take" is mostly about being precise rather than
being brief: a single detailed practitioner reply is worth more than a vague
summary of three one-liners. Name what people actually built, measured, or
disagreed about.

**These budgets are higher than hn-digest's, on purpose.** Lobsters threads have
few comments but each one is dense and technical; an HN thread is long and
diffuse. The same 3-sentence floor needs more words here to say something real
rather than something padded. Measured output lands at ~85 words of summary and
~155 of take, which is what these ranges are set around — if you find yourself
routinely under the floor you have skipped something worth saying, and if you
find yourself over the ceiling you are surveying comments instead of arguing
them.

Both budgets are two-sided. The floor is a real requirement: a summary of one
sentence tells the reader nothing they could not get from the headline, and a
take of one sentence is not a summary of a discussion — it is a fragment. Three
sentences is the minimum for each, so if you only have two real points, find the
third rather than padding, and if you genuinely have fewer, say which part of
the picture is missing rather than inventing it. The ceiling is also real:
several subagents' briefs land in one parent context, and an unbounded thread
note crowds out the others. Every reader who wants the full argument has the
thread link — your job is the shape of the argument, not its transcript.

Aim for the shape "most commenters land on X, on the grounds that A; the
sharpest objection is Y, because B" — one or two real positions developed, not a
survey of everyone who spoke. Naming the specific disagreement is what makes
this worth reading; "commenters were divided" is not.

Taxonomy — pick exactly one: AI/ML, Dev Tools, Security & Privacy, Startups &
Business, Systems & Infra, Science, Policy & Law, Web & Platforms, Hardware,
Show HN, Culture. Lobsters' own tags are a reliable prior but a different,
finer taxonomy: `rust` points at Dev Tools, it is not a value you can use
directly. The full rules are in ../digest/references/categories.md.

sentiment describes the thread's mood, not the news. Use enthusiasm or
skeptical when one side clearly wins; reserve mixed for threads that split on
something substantive; use neutral for short threads with no real argument.
```

If a brief comes back fenced or wrapped in prose, strip it — but if the content
is there, do not throw the subagent's work away over a formatting nit.

If a subagent fails outright, drop that story and carry on — four briefs is
fine. Never backfill a failed subagent with your own guess at the article.

## Return

Aggregate the surviving briefs into one object and print it as bare JSON, with
no commentary around it — the parent skill parses this directly:

```json
{
  "source": "lobsters",
  "count": 5,
  "stories": [
    {
      "source": "lobsters",
      "url_key": "ziglang.org/download/0.17.0/release-notes.html",
      "headline": "Zig 0.17.0 Release Notes",
      "url": "https://ziglang.org/download/0.17.0/release-notes.html",
      "discussion_url": "https://lobste.rs/s/wcmfft/zig_0_17_0_release_notes",
      "category": "Dev Tools",
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