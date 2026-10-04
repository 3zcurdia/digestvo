---
name: digest
description: Manual-only workflow that runs the hn-digest and lb-digest worker skills as parallel subagents against Hacker News and Lobsters, aggregates both result sets into one deduplicated candidate list, interviews the user about which articles to keep, and publishes each kept one as a digestvo post in src/_posts/ tagged with where it appeared. Load when the user runs /digest, asks for a digest, HN digest, Lobsters digest, tech-news roundup, or newsletter issue, or asks to pull today's HN or Lobsters front pages into the site's feed. Do not auto-load for scraping a single site (use hn-digest or lb-digest) or for general news summarising.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# digest

Input: nothing, or a free-text request such as "just the top 5" or "no AI
stories" (the prompt, or `$ARGUMENTS`).
Output: one post per kept article in `src/_posts/YYYY-MM-DD-<slug>.md`. Each
carries `categories: digest`, a `tags` list, `source_url`, a `summary`, and a
discussion key per site it appeared on — `hn_url` and/or `lobsters_url` — with
the discussion summary as its body, written from `references/post-template.md`.
Presence of those two keys is what draws the Hacker News and Lobsters links on
the post page. The index and `/posts` listings render title, date, and summary
only.

## The shape of the work

Two worker skills do the scraping and research, one per site, and this skill
does everything after: merging, the interview, and the writing. Keeping the
boundary sharp is deliberate. If the workers each wrote posts, the two would
drift apart on front matter and category rules within a month, and the
overlap stories would get two posts instead of one with two icons.

The worker skills return briefs as JSON. This skill is the only place that
decides what gets published.

## Step 1 — Run both workers in parallel

Spawn two subagents with the `general` agent type **in the same message**, so
they run concurrently, then wait for both.

Subagent A:

```
You are the Hacker News half of a two-source digest. Working directory is the
repo root.

Read .opencode/skills/hn-digest/SKILL.md and follow it exactly, doing only its
scraping and research. Do not interview the user. Do not write any files.

Return ONLY the bare JSON object that skill specifies — no preamble, no code
fence, no commentary after it. Keep every field on every brief, especially
url_key.
```

Subagent B:

```
You are the Lobsters half of a two-source digest. Working directory is the
repo root.

Read .opencode/skills/lb-digest/SKILL.md and follow it exactly, doing only its
scraping and research. Do not interview the user. Do not write any files.

Return ONLY the bare JSON object that skill specifies — no preamble, no code
fence, no commentary after it. Keep every field on every brief, especially
url_key.
```

Both workers fan out into their own per-story subagents, so expect a couple of
minutes. Do not start writing posts while either is still running.

If one worker comes back unusable — no JSON, or it explains it could not reach
the site — carry on with the other alone. A one-source digest is better than no
digest, and it is not worth retrying mid-run. Say plainly in the final report
which source was missing, so a silent half-digest does not look like the site's
front page was empty.

## Step 2 — Aggregate into one candidate list

Merge the two result sets by `url_key`, comparing the strings **exactly**.
Both scripts compute `url_key` the same way for a reason: it is a stable
identity, not something to be fuzzy-matched. Two briefs with the same
`url_key` are one article that ran on both sites.

For each merged article keep:

- one `headline` and one `url` (they agree — both sites link the same article)
- the `category` and `summary` from whichever brief you trust more. If the two
  summaries disagree, prefer the HN brief and merge rather than pick: keep the
  better of the two openings, then fold in any concrete detail the other had
  that the kept one missed. The result still has to clear the same 3-4 sentence
  floor — never resolve a disagreement by cutting the summary down to one
  sentence.
- every `discussion_url`, keyed by its `source`, so `hn_url` and `lobsters_url`
  can both end up on the post
- **both** `take` values when there are two, kept apart rather than blended

**Near-duplicate check.** `url_key` is exact, and the scripts' tracking-param
list is not exhaustive — newsletters invent referral params constantly, so the
same article can arrive with different `?…` suffixes and land in two groups.
Before the interview, scan for two candidates whose `url_key` shares a host and
a path prefix but differs afterwards. If you find one, that is a duplicate:
merge it by hand, or flag it in the interview so the user is not offered the
same article twice. Do not silently publish both.

## Step 3 — Check against posts that already exist

A story stays on a front page for days, and running the digest twice in one day
is normal. Either way, writing a second post for an article already published
puts a duplicate in the index and splits its discussion across two URLs.

```sh
python3 .opencode/skills/digest/scripts/collide.py src/_posts
```

It reads every post's front matter, reduces `source_url` to the same `url_key`
the workers produce, and returns the ones that have one. Compare each
candidate's `url_key` against that list **exactly**. A missing or empty
`src/_posts` is reported as `exists: false` with no posts — that is a normal
state after a wipe, not a failure, and it means nothing collides.

It also returns each post's `hn_id` and `lobsters_id`. Use those as a second
check: if a candidate's discussion id matches a published post but its
`url_key` does not, the URL must have changed (a redirect, a canonical-path
change) and that post is a collision too. Trust the id match — it is the more
reliable signal, because `url_key` depends on a tracking-param list that is
never quite exhaustive.

Mark every colliding candidate `already published`, carrying the existing
post's path and slug forward so Step 5 knows which file to enrich. Candidates
that do not collide are `new`.

Note that a collision is **not** a reason to skip research. The existing post's
comments summary is stale by definition — that is the whole reason the story is
back on the front page — so the fresh take is exactly what the enrichment
needs. Research colliding candidates normally.

## Step 4 — Interview: keep or drop

Now ask the user, per article. This is the one part of the pipeline that is not
automatable, so do not skip it and do not guess.

Print the aggregated list as a table first, so the decision is being made on
real summaries rather than headlines. Say which rows are already published:

```
| # | Article | Where | State | Cat | Take |
|---|---------|-------|-------|-----|------|
| 1 | Kolibri: A Sovereign Open-Weight Model | HN | ♻️ refresh | AI/ML | mixed |
| 2 | Why don't more developers use the platform? | HN + 🦞 | new | Dev Tools | mixed |
| 3 | Zig 0.17.0 Release Notes | 🦞 | new | Dev Tools | skeptical |
```

Then call the `question` tool with `multiple: true` — one option per article, so
the user can keep several and drop several in a single pass. A custom answer
lets them say "just 1 and 3" without the tool having to be right about labels.

Option labels go short (`3 · Zig 0.17.0 (🦞)`); the description carries the
one-sentence summary. For a refresh, say "refreshes an existing post" in the
description so a keep is a deliberate choice to overwrite, not an accident.

Tell the user, before asking:

- which articles appeared on both sites. These are the highest-signal entries
  in the whole digest — two independent communities picked the same thing — so
  it is worth flagging where their two takes disagree, because that divergence
  is the part they cannot get by clicking either link.
- which articles could not be opened (`readable: false`), so they can drop
  those knowingly.
- anything where you had to merge a near-duplicate by hand, per Step 2.

If the user already named articles or a count in their prompt, skip the
interview and go straight to Step 5 with what they asked for.

**Never publish an article the user did not keep.** If they keep none, say so
and stop without writing anything.

## Step 5 — Write new posts, enrich existing ones

Split the kept articles by the `already published` flag from Step 3. New
articles get a post written; colliding articles get their existing post's
comments summary refreshed. Never write a second file for a colliding article.

Get a real local timestamp once — Bridgetown bakes the date into every post's
permalink, and a made-up offset produces subtly wrong URLs:

```sh
date "+%Y-%m-%d %H:%M:%S %z"
```

### New articles

Write one file per new article at `src/_posts/YYYY-MM-DD-<slug>.md`, starting
from `references/post-template.md` — the single-source or the both-sites shape —
and slugging the headline by hand: `Kolibri: A Sovereign Open-Weight Model` becomes
`kolibri-sovereign-open-weight-model`.

```markdown
---
layout: post
title: "Kolibri: A Sovereign Open-Weight Model"
date:   2026-10-03 21:15:00 -0600
categories: digest
tags: ["AI/ML"]
source_url: https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/
hn_url: https://news.ycombinator.com/item?id=49942706
summary: >-
  Aleph Alpha released Kolibri, a 78B MoE (3B active) German-English model with
  1M context, Apache 2.0 weights, trained end-to-end in Germany, aimed at
  regulated public-sector deployment.
---

The thread splits on whether sovereignty is real: backers argue no lab
publishes its data pipeline, so Europe stalls when Kimi stops shipping weights.
The sharpest counter is that autarky is itself a national security risk.
```

An article from both sites carries both keys and both takes:

```markdown
---
...
hn_url: https://news.ycombinator.com/item?id=49950554
lobsters_url: https://lobste.rs/s/srduzv/why_don_t_more_developers_use_platform
summary: >-
  A blog post arguing that the platform's real problem is that nobody learns it.
---

**On Hacker News.** <the HN take>

**On Lobsters.** <the Lobsters take>
```

A single-source article carries one key and its body is just that take, with no
bolded lead-in — there is only one room to talk about.

### Already published: enrich, never duplicate

For a colliding article, edit the existing post file in place. Read it first.

**Change the body and nothing else.** The whole point is that the URL, the date,
the title and the summary stay put — an enriched post keeps its identity, so
nothing that already links to it breaks. Specifically, leave alone:

- `title`, `date`, `source_url`, `summary`, `tags`, `categories` — all untouched
- every `hn_url` / `lobsters_url` already present

So the edit is a body replacement, nothing more. If the fresh brief improved on
the stored `summary`, mention it in your report and let the user decide — do not
quietly rewrite it.

**Replace only the sections whose source you have a fresh take for.** This is
where a naive "overwrite the body" goes wrong. A post written when the article
was on both sites has two sections:

```markdown
**On Hacker News.** <old, stale>

**On Lobsters.** <old, stale>
```

If today's front page only surfaced it on HN, replace the `**On Hacker News.**`
paragraph and leave `**On Lobsters.**` exactly as it was. Clobbering the whole
body would silently delete a discussion nobody asked you to remove, and would
leave a `lobsters_url` in the front matter pointing at a take that no longer
exists on the page.

A post with a single unlabelled body (one source, no bolded lead-in) just gets
that body replaced.

**Add a missing source, never remove one.** If the existing post has only
`hn_url` and today the story is on Lobsters too, append a `**On Lobsters.**`
section with its take and add the `lobsters_url` key, so the Lobsters link
starts showing.
Additive changes are fine; removals are not.

If the existing post's body is already at least as good as the fresh take, leave
the file completely untouched and say so — a refresh that changes nothing is a
legitimate outcome, and churning the file for its own sake just makes the diff
lie about what actually changed.

Rules that matter:

- **The presence of `hn_url` / `lobsters_url` is what draws the source
  links.** `src/_components/shared/source_links.erb` renders a Hacker News link
  with the Y Combinator square for `hn_url` and a Lobsters link with its square
  mark for `lobsters_url`, so a post with neither shows only "Read the original"
  and a post from both shows both. Do not add a source field — the URL keys are
  the flag, and a second field can disagree with them.
- **Never put HTML, SVG, icons or emoji in a post.** Every mark is drawn by the
  component from front matter. If a mark looks wrong, fix the component once;
  do not patch it into posts, where it would drift from every other post.
- **`categories: digest` on every post.** It is the only key that shapes the
  permalink (`/digest/YYYY/MM/DD/slug/`), and a stable one matters because
  these posts get linked and archived. The human-readable taxonomy belongs in
  `tags`, which Bridgetown keeps out of the URL entirely — put it in
  `categories` instead and you scatter the post across `/ai-ml/2026/10/03/…`
  paths, and a multi-tag value builds one joined monstrosity like
  `/ai-ml/security-&-privacy/2026/10/03/…`, ampersand unescaped.
- `tags` renders below the title on the post page only, never in either
  listing. Keep it to the one bucket the worker chose; the taxonomy in
  `references/categories.md` is deliberately coarse so an article lands in the
  same place every time.
- `summary` shows in the listing as well as on the post page, so write it to
  stand alone — a reader may never open the post. It carries the 3-4 sentence
  floor too, since that is what it renders as on both surfaces.
- The body is the discussion summary and nothing else. No second summary, no
  "Read more", no duplicate title. Bolded lead-ins are only for a two-thread
  article.
- `title` is the headline verbatim. `source_url` links the original article.
- Use the workers' `category` as `tags` and their takes as the body. You are
  assembling, not rewriting — if a take reads badly that is the worker's output
  to fix, not something to paper over silently.
- For an unreadable article, say so in the summary ("HN's top comments on a
  story we could not open — the outlet is paywalled") and never invent its
  contents.
- No testimonials, no invented quotes, no post-hoc commentary of your own on
  whether either community is right. The digest reports the rooms, it does not
  join them.
- Write the heaviest article first. Bridgetown orders posts newest-first by
  filename date, so within one day the file order decides nothing — but it
  keeps your `git status` readable in the order you think about them.
- If a post already exists at that path, do not overwrite silently — tell the
  user and offer to refresh it.

## Step 6 — Report

Tell the user, briefly:

- how many **new** posts were written and how many **existing** posts were
  refreshed, out of how many candidates, plus the URL of the newest one. Keep
  those two counts separate — "8 posts" hides whether anything was duplicated.
- which articles they kept, so a wrong selection is easy to spot
- for each refreshed post, what changed: which source's take was replaced, and
  which were left alone. If a refresh turned out to change nothing, say that
  too.
- if a `summary` looked improvable but was left untouched, mention it so the
  user can decide rather than wondering why it was not updated
- how many posts carried the 🦞, and how many carried both icons. Say this even
  when the 🦞 count is zero — a run that silently produced an all-HN digest is
  exactly the failure worth noticing.
- which source, if either, failed or was skipped
- that `/` shows the latest 10 and `/posts` shows all of them, both rendering
  title + summary only
- any category that did not fit the taxonomy well — those are the signals that
  `references/categories.md` needs a new bucket, and adding one silently would
  hide that
- that they can run `rake deploy` to build and preview

## Categories

`references/categories.md` holds the taxonomy both workers choose from and the
rules for extending it. A bucket becomes the post's `tags` value, so pick the
nearest existing one rather than inventing a new one: a category that appears
once is not a category — it is a typo. Surface new buckets to the user instead,
and let them decide.