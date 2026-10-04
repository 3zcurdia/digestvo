---
name: digest
description: Publish today's Hacker News and Lobsters front pages as digestvo posts in src/_posts/. Use when the user runs /digest or asks for a digest, HN digest, Lobsters digest, tech-news roundup or newsletter issue.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# digest

You run five commands, spawn researcher subagents, ask the user one question,
and report. Scripts do everything else. **Never write or edit a file under
`src/_posts/` yourself.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/digest/scripts/`.
- Run files: `.opencode/tmp/digest/` (Step 1 creates and clears it).
- Input (`$ARGUMENTS`): empty, a count such as "top 5", or a filter such as
  "no AI stories". Step 4 says what to do with it.

## If something fails

| What happened | Do this |
|---|---|
| A script exits non-zero | Stop. Paste its error to the user. Do not improvise the result. |
| Step 1 prints `SOURCE DOWN` | Continue with the other source. Mention it in the report. |
| A researcher replies `FAILED` or never writes its brief | Spawn it once more with the same prompt. If it fails again, drop it and continue. |
| Step 3 prints `SKIPPED` | Those briefs were invalid. Continue without them. Mention it. |
| The user keeps nothing | Say so and stop. Write nothing. |
| Step 6 build fails | Paste the error. Do not edit posts to work around it. |

## Step 1 — Fetch

```sh
python3 .opencode/skills/digest/scripts/fetch.py front
```

Prints the shortlist and one researcher prompt per story. Do not change the
list. The user chooses later, in Step 4.

## Step 2 — Research

Spawn one `general` subagent per prompt printed by Step 1, **all in a single
message** so they run in parallel. Paste each prompt exactly as printed. Wait
until every subagent has replied. Do not read the brief files yourself.

## Step 3 — Merge

```sh
python3 .opencode/skills/digest/scripts/merge.py
```

Prints a numbered table plus one summary per row. If it prints
`NEAR-DUPLICATE: rows A and B`, look at the two headlines. If they are the
same article, run `merge.py --merge A,B` and use the new table instead.

## Step 4 — Ask the user

Show the table and the summaries exactly as printed. Then:

- `$ARGUMENTS` says "top N": keep rows 1 to N. Do not ask.
- `$ARGUMENTS` names a category to drop, such as "no AI": keep every row
  whose Category is not that one. Do not ask.
- Otherwise call the `question` tool with multiple selection enabled, one
  option per row. Label: `<row> · <headline>`. Description: the row's State
  (`new`, or `refresh (edits existing post)`). If the tool is not available,
  ask in plain text "Which row numbers do you want to keep?" and wait.

Before asking, point out rows listed under `BOTH SITES` (two communities picked
the same story) and rows whose `Article read` column says `NO`.

Keep exactly what the user chose. Never add a row they did not pick.

## Step 5 — Write

```sh
python3 .opencode/skills/digest/scripts/write_post.py --keep 1,3,5
```

Use the row numbers from Step 3's table, or `all`. The script creates new
posts, refreshes existing ones in place, verifies every file it touched, and
prints a `REPORT` block.

## Step 6 — Build

```sh
bundle exec rake deploy
```

## Step 7 — Report

Paste the `REPORT` block from Step 5. Then add: whether the build passed, which
rows the user kept, and any `SOURCE DOWN`, `SKIPPED` or `FAILED` lines from
Steps 1 to 3. Finish with: `/` lists the latest 10 posts, `/posts` all of them.

## Reference

- `references/researcher.md` — what each researcher subagent does. The prompt
  from Step 1 tells them to read it; you do not need to.
- `references/post-template.md` — the post shape `write_post.py` produces.
- `references/categories.md` — the taxonomy and its tie-break rules.
- `references/rationale.md` — why the pipeline is shaped this way.
