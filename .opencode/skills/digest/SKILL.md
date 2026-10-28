---
name: digest
description: Publish today's Hacker News and Lobsters front pages as digestvo posts in src/_posts/. Use when the user runs /digest or asks for a digest, HN digest, Lobsters digest, tech-news roundup or newsletter issue.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# digest

You run five commands, spawn researcher subagents, curate each story with
the user one by one, and report. Scripts do everything else. **Never write
or edit a file under `src/_posts/` yourself.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/digest/scripts/`.
- Run files: `.opencode/tmp/digest/` (Step 1 creates and clears it).
- One-time screenshot setup on a fresh checkout, after `npm install`:

  ```sh
  PLAYWRIGHT_BROWSERS_PATH=0 npx playwright install chromium
  ```

  Playwright and its Chromium live under `node_modules/`; no browser is
  needed by CI or by `rake deploy`.
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
| Step 5 reports a failed or timed-out screenshot | If the error says `Executable doesn't exist`, run the one-time setup above and run Step 5 again with the same `--keep`. Otherwise paste the error and stop; rows that failed were not written. |
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

Prints a numbered table plus one summary per row and writes the same rows
to `.opencode/tmp/digest/candidates.json`. If it prints
`NEAR-DUPLICATE: rows A and B`, look at the two headlines. If they are the
same article, run `merge.py --merge A,B` and use the new table instead.

## Step 4 — Curate with the user, one story at a time

Do not print the full table. Read `.opencode/tmp/digest/candidates.json`
and walk rows 1 to N in table order, one story per turn:

- `$ARGUMENTS` says "top N": keep rows 1 to N. Do not ask.
- `$ARGUMENTS` names a category to drop, such as "no AI": keep every row
  whose Category is not that one. Do not ask.
- Otherwise, for each row show exactly this card, then ask:

  ```
  Story <row>/<total>: <headline>
  Where: <HN / LB / HN+LB> · State: <new | refresh (edits <file>)> · Category: <category>
  Article read: <yes | NO> · Mood: <mood>[ · on both sites]
  Summary: <summary>
  ```

  Call the `question` tool with single selection: options `Keep` and
  `Discard`. If the tool is not available, ask in plain text
  `Keep row <row>? (y/n)` and wait. Record the answer before moving to
  the next row. A `NO` article read or an `on both sites` flag stays
  inline on that story's card — do not save it for a separate preamble.

After the last row, list the kept and discarded row numbers. If the user
kept nothing, say so and stop. Write nothing.

Keep exactly what the user chose. Never add a row they did not pick.

## Step 5 — Write

```sh
python3 .opencode/skills/digest/scripts/write_post.py --keep 1,3,5
```

Use the row numbers from Step 3's table, or `all`. The script captures one
1200x630 screenshot per kept story from the original article first — the
HN/Lobsters discussion for a self post — stores it under
`src/images/digest/`, and writes `image: "/images/digest/<post>.jpg"` into
the post. An existing screenshot file is never overwritten. A story whose
screenshot cannot be captured is reported as `FAILED` and is not written; the script
then exits non-zero, so stop and paste its error.

The script creates new posts, refreshes existing ones in place (adding the
missing image key when needed), verifies every file it touched — including
the screenshot's existence and dimensions — and prints a `REPORT` block.

## Step 6 — Build

```sh
bundle exec rake deploy
```

## Step 7 — Report

Paste the `REPORT` block from Step 5. Then add: whether the build passed, which
rows the user kept, and any `SOURCE DOWN`, `SKIPPED`, `FAILED` or screenshot
capture lines from Steps 1 to 5. Finish with: `/` lists the latest 10 posts,
`/posts` all of them.

## Reference

- `references/researcher.md` — what each researcher subagent does. The prompt
  from Step 1 tells them to read it; you do not need to.
- `references/post-template.md` — the post shape `write_post.py` produces.
- `references/categories.md` — the taxonomy and its tie-break rules.
- `references/rationale.md` — why the pipeline is shaped this way.
