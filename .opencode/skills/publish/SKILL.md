---
name: publish
description: Publish digestvo to the site and the Telegram channel - commit + push on main, wait for the GitHub Actions deploy to go green, then announce the new posts on Telegram. Use when the user runs /publish or asks to publish, deploy, ship or announce the digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# publish

Publishing is commit + push + deploy watch + Telegram. GitHub Actions builds
and deploys on every push to main (`.github/workflows/deploy.yml`); nothing is
built locally. One script per mechanical step. **Never run `git commit`,
`git push` or the `gh` CLI yourself — always go through the scripts.**

- Working directory: the repo root.
- Scripts: `.opencode/skills/publish/scripts/`.
- Input (`$ARGUMENTS`): the commit message, short imperative style matching
  the history ("Add 2026-10-13 digest", "Copy fix"). If empty, write one
  from what changed — usually the post files — and pass it quoted.

## If something fails

| What happened | Do this |
|---|---|
| `publish.py` exits non-zero | Stop. Paste its error verbatim. Do not pull, rebase, force-push, or retry to work around it. |
| It prints `NOTHING TO COMMIT` | Tell the user there is nothing to publish. Stop. |
| The push is rejected | The commit exists locally, the remote does not. Show the error and ask the user how to proceed. |
| `watch_deploy.py` exits non-zero | The push succeeded but the deploy did not. Paste its REPORT verbatim and stop — no Telegram. Do not retry the deploy or edit posts to work around a build failure. |
| `telegram_post.py` fails | Stop and paste the error verbatim — a failed run may already have sent some messages, and the error names which ones. |
| It prints `NOTHING TO SEND` | Say so and stop. That is a normal outcome for a commit with no new posts (a "Copy fix", a translation of an older post). |

## Step 1 — Preview (only if the changes are unclear)

```sh
python3 .opencode/skills/publish/scripts/publish.py --dry-run
```

Shows what would be committed. Skip it when the session's changes are already
known (e.g. right after `/digest`).

## Step 2 — Commit and push

```sh
python3 .opencode/skills/publish/scripts/publish.py "$ARGUMENTS"
```

The script stages everything (`.gitignore` still applies), commits on `main`
with the given message, pushes to `origin/main`, and prints a `REPORT` block.
It refuses to run on another branch or with merge conflicts, and never pulls,
rebases, or force-pushes.

## Step 3 — Watch the deploy

```sh
python3 .opencode/skills/publish/scripts/watch_deploy.py
```

Finds the `.github/workflows/deploy.yml` run of the pushed commit and waits
until it completes, printing a `REPORT` with the conclusion and run URL. The
site — and every link the Telegram messages will carry — is only live when
this reports `success`. If the user wants to watch it live instead:
`gh run watch` from the repo root.

## Step 4 — Telegram

After a **successful deploy**, announce the new posts on the Telegram public
channel. This runs automatically at the end of a publish — the user does not
have to ask for it. Skip only when the user says not to (e.g. "no telegram"),
or when Step 3 did not succeed.

```sh
python3 .opencode/skills/publish/scripts/telegram_post.py
```

One message per post: title, hook, and links (site, original, HN/Lobsters
when present). In its default form (no file args) it takes the posts Added in
the HEAD commit and skips Modified ones (pass `--include-updated` to include
them, or pass explicit `src/_posts/…md` paths). `--dry-run` previews the
messages without sending. `--chat @handle` overrides `TELEGRAM_CHANNEL` for
one run. Telegram-only (no commit needed): pass explicit post paths — the
script touches git only when no files are given.

- Config (environment, never committed): `TELEGRAM_BOT_TOKEN` (from
  @BotFather), `TELEGRAM_CHANNEL` (e.g. `@digestvo`). The bot must be an
  administrator of the channel. The script never prints the token.

## Step 5 — Report

Paste the `REPORT` blocks from Steps 2 to 4. Then add: the commit landed on
`main`, the deploy conclusion, and which posts were announced (or why none
were). Finish with: `/` lists the latest 10 posts, `/posts` all of them.
