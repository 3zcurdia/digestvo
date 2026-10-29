---
name: digest
description: Phase 2 of the digestvo pipeline - curate the ingested candidate stories one by one with the user and write the kept posts to src/_posts/. Use when the user runs /digest after /ingest, or says curate the digest / write the posts. Fetching and research is /ingest; the whole pipeline is /autonomos-digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# digest

Phase 2 of the digest pipeline: **the part that asks the user**. You curate
each story with the user one by one, then run two commands to write the kept
posts and build. Scripts do everything else. **Never write or edit a file
under `src/_posts/` yourself.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/digest/scripts/` (shared by both digest phases).
- Run files: `.opencode/tmp/digest/` — produced by `/ingest`.
- Input (`$ARGUMENTS`): empty, a count such as "top 5", or a filter such as
  "no AI stories". Step 2 says what to do with it.

## If something fails

| What happened | Do this |
|---|---|
| `.opencode/tmp/digest/candidates.json` is missing | Run the ingest phase first: read `.opencode/skills/ingest/SKILL.md` and follow it, then continue here. |
| The candidates were produced before today | Say how old they are and ask the user whether to reuse them or run the ingest phase again. |
| A script exits non-zero | Stop. Paste its error to the user. Do not improvise the result. |
| Step 3 prints `SKIPPED` | Those briefs were invalid. Continue without them. Mention it. |
| The user keeps nothing | Say so and stop. Write nothing. |
| Step 3 reports a failed or timed-out screenshot | If the error says `Executable doesn't exist`, run the one-time setup above and run Step 3 again with the same `--keep`. Otherwise paste the error and stop; rows that failed were not written. |
| Step 4 build fails | Paste the error. Do not edit posts to work around it. |

One-time screenshot setup on a fresh checkout, after `npm install`:

```sh
PLAYWRIGHT_BROWSERS_PATH=0 npx playwright install chromium
```

Playwright and its Chromium live under `node_modules/`; no browser is needed
by CI or by `rake deploy`.

## Step 1 — Candidates

Read `.opencode/tmp/digest/candidates.json` (written by the merge step of
`/ingest`; each row carries `row`, `headline`, `category`, `sources`,
`state`, `post_path`, `summary`, `both_sites` and `readable`). Confirm the
file is there before touching anything else.

## Step 2 — Curate with the user, one story at a time

Do not print the full table. Walk rows 1 to N in table order, one story per
turn:

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
  `Keep row <row>? (y/n)` and wait. Record the answer before moving to the
  next row. A `NO` article read or an `on both sites` flag stays inline on
  that story's card — do not save it for a separate preamble.

After the last row, list the kept and discarded row numbers. If the user kept
nothing, say so and stop. Write nothing.

Keep exactly what the user chose. Never add a row they did not pick.

## Step 3 — Write

```sh
python3 .opencode/skills/digest/scripts/write_post.py --keep 1,3,5
```

Use the row numbers from Step 2, or `all`. The script captures one 1200x630
screenshot per kept story from the original article first — the HN/Lobsters
discussion for a self post — stores it under `src/images/digest/`, and writes
`image: "/images/digest/<post>.jpg"` into the post. An existing screenshot
file is never overwritten. A story whose screenshot cannot be captured is
reported as `FAILED` and is not written; the script then exits non-zero, so
stop and paste its error.

The script creates new posts, refreshes existing ones in place (adding the
missing image key when needed), verifies every file it touched — including
the screenshot's existence and dimensions — and prints a `REPORT` block.

## Step 4 — Build

```sh
bundle exec rake deploy
```

## Step 5 — Report

Paste the `REPORT` block from Step 3. Then add: whether the build passed,
which rows the user kept, and any `SKIPPED` or screenshot capture lines from
this phase. Finish with: `/` lists the latest 10 posts, `/posts` all of them.

Then say: to translate the new posts run `/translate` with the file paths
from the REPORT block, or run `/publish` to ship (commit, deploy watch,
Telegram), or `/autonomos-digest` for the whole chain next time.

## Reference

- `references/post-template.md` — the post shape `write_post.py` produces.
- `references/categories.md` — the taxonomy and its tie-break rules.
- `references/rationale.md` — why the pipeline is shaped this way.
