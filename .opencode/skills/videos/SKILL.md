---
name: videos
description: Turn YouTube watch history into digestvo video pages in src/_videos/, each with a summary and the key insights from the transcript. Use when the user runs /videos or asks to publish, review or digest videos they watched.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# videos

You run six commands, spawn analyst subagents, curate each video with the user
one by one, and report. Scripts do everything else. **Never write or edit a
file under `src/_videos/` yourself.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/videos/scripts/`.
- Run files: `.opencode/tmp/videos/` (Step 1 clears it).
- Input (`$ARGUMENTS`): empty, a source such as "watch later", a count such as
  "top 5", or a filter such as "no AI". Step 4 says what to do with it.

Only videos the analyst recommends are ever published. A `skip` is reported and
dropped.

## If something fails

| What happened | Do this |
|---|---|
| A script exits non-zero | Stop. Paste its error to the user. Do not improvise the result. |
| `check_setup.py` says NOT READY | Paste its output. It names the fix. Do not go hunting yourself. |
| A video has no transcript | Say which, and carry on. Note it in the report. |
| `brew upgrade yt-dlp` fixes it | A video used to have captions and now does not. Try this before anything else — YouTube changes its player often and a stale build silently loses subtitles. |
| An analyst replies `FAILED` | Spawn it once more with the same prompt. If it fails again, drop it and continue. |
| `validate_brief.py` prints `INVALID` | Those briefs are bad. Continue without them. Mention it. |
| The user keeps nothing | Say so and stop. Write nothing. |
| Step 7 build fails | Paste the error. Do not edit pages to work around it. |

## Step 0 — Check the setup

Only when something looks wrong, or the first time you run this:

```sh
python3 .opencode/skills/videos/scripts/check_setup.py
```

## Step 1 — Shortlist

```sh
python3 .opencode/skills/videos/scripts/candidates.py
```

Prints the candidates and writes `front.json`. It reads your history through
yt-dlp using your own browser session and falls back to a Takeout export when
there is no session. Defaults: last 30 days, 20 videos, watch history.

`$ARGUMENTS`:
- names a source — `watch later` becomes `--source watch-later`,
  `both` becomes `--source both`
- names a count — `top 5` becomes `--limit 5`
- otherwise leave the defaults

Do not change the list. The user chooses later, in Step 5.

If it prints `NOTHING FOUND`, stop and paste the message. It means there is no
session file and no Takeout export; `references/setup.md` has both.

## Step 2 — Fetch metadata and transcripts

```sh
python3 .opencode/skills/videos/scripts/fetch_video.py --from-candidates
```

One yt-dlp call per video for the metadata and one for the subtitles — they are
separate because `--dump-single-json` implies simulate, and a simulated run
silently writes no subtitle file. Writes
`.opencode/tmp/videos/video-<id>.json`. Videos under three minutes, live
streams and anything unavailable are dropped and listed. A video with no
captions is transcribed locally with whisper.cpp when a model is installed.

## Step 3 — Analyse

Spawn one `general` subagent per video in `front.json` that Step 2 kept, **all in
a single message** so they run in parallel. Paste each prompt exactly as printed.
Each analyst reads `references/analyst.md`, reads the transcript, decides a
verdict and writes a six-field brief. Wait until every subagent has replied. Do
not read the brief files yourself.

## Step 4 — Merge

```sh
python3 .opencode/skills/videos/scripts/merge.py
```

Prints two groups: `WORTH YOUR TIME` and `PASSED ON`, and writes
`candidates.json`. The first group is numbered 1 to N and is what the user
curates. The second is reported, never asked about.

## Step 5 — Curate with the user, one video at a time

Do not print the full table. Read `.opencode/tmp/videos/candidates.json` and
walk the recommended rows 1 to N in order, one video per turn:

- `$ARGUMENTS` says "top N": keep rows 1 to N. Do not ask.
- `$ARGUMENTS` filters a category out, such as "no AI": keep every row whose
  category is not that one. Do not ask.
- Otherwise, for each row show exactly this card, then ask:

  ```
  Video <row>/<total>: <title>
  Where: <channel> · <duration> · <category> · <new | refresh (edits <file>)>
  Watched: <date | unknown>
  Transcript: <yes, N words | NONE — <reason>>
  Summary: <summary>
  ```

  Call the `question` tool with single selection: options `Keep` and
  `Discard`. If the tool is not available, ask in plain text
  `Keep row <row>? (y/n)` and wait. Record the answer before moving to the next
  row. A missing transcript stays inline on that video's card.

After the last row, list the kept and discarded row numbers, and state how many
were passed on. If the user kept nothing, say so and stop. Write nothing.

Keep exactly what the user chose. Never add a row they did not pick.

## Step 6 — Write

```sh
python3 .opencode/skills/videos/scripts/write_video.py --keep 1,3,5
```

Use the row numbers from Step 4's table, or `all`. The script writes new pages,
refreshes existing ones in place, downloads the thumbnail, refuses any row the
analyst passed on, re-parses every file it touched, and prints a `REPORT` block.

## Step 7 — Build

```sh
bundle exec rake deploy
```

## Step 8 — Report

Paste the `REPORT` block from Step 6. Then add: whether the build passed, which
rows the user kept, how many were passed on, any video with no transcript, and
any skipped or failed video from Steps 2 to 4. Finish with: `/videos` lists
them all, newest first.

## Reference

- `references/setup.md` — the two one-time steps: yt-dlp and the cookies file.
- `references/analyst.md` — what each analyst subagent does. The prompt from
  Step 3 tells them to read it; you do not need to.
- `references/video-template.md` — the page shape `write_video.py` produces.