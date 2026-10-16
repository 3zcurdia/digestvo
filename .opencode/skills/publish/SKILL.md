---
name: publish
description: Commit every pending change and push to main, which deploys the site via GitHub Actions, or announce new posts on the Telegram channel. Use when the user runs /publish or asks to publish, ship, deploy, or push the current changes, or to post to Telegram.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# publish

Publishing is commit + push. GitHub Actions builds and deploys on every
push to main (`.github/workflows/deploy.yml`); nothing is built locally.
One script does all of it. **Never run `git commit` or `git push`
yourself — always go through the script.**

- Working directory: the repo root.
- Script: `.opencode/skills/publish/scripts/publish.py`.
- Input (`$ARGUMENTS`): the commit message, short imperative style matching
  the history ("Add 2026-10-13 digest", "Copy fix"). If empty, write one
  from what changed — usually the post files — and pass it quoted.

## If something fails

| What happened | Do this |
|---|---|
| The script exits non-zero | Stop. Paste its error verbatim. Do not pull, rebase, force-push, or retry to work around it. |
| It prints `NOTHING TO COMMIT` | Tell the user there is nothing to publish. Stop. |
| The push is rejected | The commit exists locally, the remote does not. Show the error and ask the user how to proceed. |

## Step 1 — Preview (only if the changes are unclear)

```sh
python3 .opencode/skills/publish/scripts/publish.py --dry-run
```

Shows what would be committed. Skip it when the session's changes are
already known (e.g. right after `/digest`).

## Step 2 — Commit and push

```sh
python3 .opencode/skills/publish/scripts/publish.py "$ARGUMENTS"
```

The script stages everything (`.gitignore` still applies), commits on
`main` with the given message, pushes to `origin/main`, and prints a
`REPORT` block. It refuses to run on another branch or with merge
conflicts, and never pulls, rebases, or force-pushes.

## Step 3 — Report

Paste the `REPORT` block. Then add: the commit landed on `main` and the
site redeploys in a couple of minutes. If the user wants to watch the
run: `gh run watch` from the repo root.

## Step 4 — Telegram (opt-in, only when asked)

After a successful push, the user may ask to announce the new posts on
the Telegram public channel. Never run this step unprompted. In its
default form (no file args, takes posts from the HEAD commit) only run it
after the push succeeds; with explicit file args it can run standalone,
no commit needed. One message per post: title, hook, and links (site,
original, HN/Lobsters when present).

- Script: `.opencode/skills/publish/scripts/telegram_post.py`.
- Config (environment, never committed): `TELEGRAM_BOT_TOKEN` (from
  @BotFather), `TELEGRAM_CHANNEL` (e.g. `@digestvo`). The bot must be an
  administrator of the channel. The script never prints the token.

```sh
python3 .opencode/skills/publish/scripts/telegram_post.py --dry-run
python3 .opencode/skills/publish/scripts/telegram_post.py
```

With no file args it sends the posts Added in the HEAD commit and skips
Modified ones (pass `--include-updated` to include them, or pass explicit
`src/_posts/…md` paths). `--chat @handle` overrides `TELEGRAM_CHANNEL`
for one run. Telegram-only (no commit needed): pass explicit post paths —
the script touches git only when no files are given. If it prints `NOTHING TO SEND`, say so and stop. On any
error, stop and paste it verbatim — a failed run may already have sent
some messages, and the error names which ones.
