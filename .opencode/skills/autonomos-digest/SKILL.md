---
name: autonomos-digest
description: Run the whole digestvo pipeline end to end in one go - ingest (fetch, research, merge), digest (curate with the user and write the posts), translate the new posts to Spanish, publish (commit + push, watch the GitHub deploy, announce on Telegram). Use when the user runs /autonomos-digest or wants the full pipeline without invoking each phase.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# autonomos-digest

The whole pipeline, four phases in order:

```
ingest -> digest -> translate -> publish
```

Each phase is its own skill: read its `SKILL.md` and follow it exactly, then
move to the next. This skill only sequences them and carries the handoffs; it
adds no rules of its own. Every phase's own failure table applies — when a
phase says stop, stop and report what happened instead of running the later
phases.

- Working directory: the repo root.
- Input (`$ARGUMENTS`): forwarded to digest curation — empty, a count such as
  "top 5", or a filter such as "no AI stories".

## The chain

1. **Ingest** — read `.opencode/skills/ingest/SKILL.md` and follow it.
   Fetch, spawn the researchers, merge. Ends with the numbered candidate
   table and `.opencode/tmp/digest/candidates.json`. Do not ask the user to
   choose stories here.
2. **Digest** — read `.opencode/skills/digest/SKILL.md` and follow it with
   `$ARGUMENTS`. This is the phase that talks to the user: one Keep/Discard
   per story, one at a time. Keep its `REPORT` block — Phase 3 needs the
   post file paths it lists as created or refreshed. If the user keeps
   nothing, stop the whole pipeline and say so.
3. **Translate** — read `.opencode/skills/translate/SKILL.md` and follow it
   on exactly the post files listed in the digest `REPORT` (created and
   refreshed), nothing else. The posts `write_post.py` produces are in
   English; they must all be Spanish before anything is published.
4. **Publish** — read `.opencode/skills/publish/SKILL.md` and follow it.
   Commit message: `Add YYYY-MM-DD digest`, with the date taken from the post
   file names in the digest `REPORT`. Do not stop after the push: the deploy
   must go green and then the new posts are announced on Telegram
   automatically.

## If something fails

| What happened | Do this |
|---|---|
| A phase reports a failure its own table covers | Follow that table. If it says stop, stop there and report; later phases do not run. |
| The user keeps nothing | Stop. Nothing is written, translated, published or announced. |
| The build fails | Stop before publishing. Paste the error; do not edit posts to work around it. |
| The deploy does not succeed | Do not send anything to Telegram. The pushed commit stays as it is; report and let the user decide. |

## Report

End with the publish `REPORT` blocks (commit, deploy conclusion, Telegram
messages), which rows the user kept and discarded, and any `SOURCE DOWN`,
`SKIPPED`, `FAILED` or screenshot capture lines from the earlier phases.
Finish with: `/` lists the latest 10 posts, `/posts` all of them.
