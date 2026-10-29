---
name: ingest
description: Phase 1 of the digestvo pipeline - fetch today's Hacker News and Lobsters shortlists, spawn researcher subagents, and merge their briefs into a numbered candidate list. Use when the user runs /ingest or asks to fetch, research or refresh the digest candidates. Choosing stories is /digest; the whole pipeline is /autonomos-digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# ingest

Phase 1 of the digest pipeline: **fetch and parse**. It ends with a numbered
candidate table written to `.opencode/tmp/digest/candidates.json`. Choosing
stories, writing posts and publishing belong to `/digest`, `/translate` and
`/publish`. **Never write or edit a file under `src/_posts/` yourself. Never
ask the user which stories to keep — that is `/digest`'s job.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/digest/scripts/` (shared by both digest phases).
- Run files: `.opencode/tmp/digest/` (Step 1 creates and clears it).
- Input: none.

## If something fails

| What happened | Do this |
|---|---|
| A script exits non-zero | Stop. Paste its error to the user. Do not improvise the result. |
| Step 1 prints `SOURCE DOWN` | Continue with the other source. Mention it in the report. |
| A researcher replies `FAILED` or never writes its brief | Spawn it once more with the same prompt. If it fails again, drop it and continue. |
| Step 3 prints `SKIPPED` | Those briefs were invalid. Continue without them. Mention it. |

## Step 1 — Fetch

```sh
python3 .opencode/skills/digest/scripts/fetch.py front
```

Prints the shortlist and one researcher prompt per story. Do not change the
list. The user chooses later, in `/digest`.

## Step 2 — Research

Spawn one `general` subagent per prompt printed by Step 1, **all in a single
message** so they run in parallel. Paste each prompt exactly as printed. Wait
until every subagent has replied. Do not read the brief files yourself.

## Step 3 — Merge

```sh
python3 .opencode/skills/digest/scripts/merge.py
```

Prints a numbered table plus one summary per row and writes the same rows to
`.opencode/tmp/digest/candidates.json`. If it prints
`NEAR-DUPLICATE: rows A and B`, look at the two headlines. If they are the
same article, run `merge.py --merge A,B` and use the new table instead.

## Step 4 — Report

Paste the numbered table and the one-line summaries. Then say: run `/digest`
to curate (or `/autonomos-digest` to continue through the whole pipeline).
Stop there — do not ask Keep/Discard, do not write posts, do not build.

## Reference

Shared with the digest phase, under `.opencode/skills/digest/references/`:

- `researcher.md` — what each researcher subagent does. The prompt from Step 1
  tells them to read it; you do not need to. Research takes must follow an
  arc-based structure (see `style-guide.md`): context → consensus → main
  controversy → minor notes (or omit). One idea per paragraph, use transitions
  to show hierarchy, and frame tangents explicitly.
- `style-guide.md` — the arc structure the takes follow.
- `categories.md` — the taxonomy and its tie-break rules.
- `rationale.md` — why the pipeline is shaped this way.
