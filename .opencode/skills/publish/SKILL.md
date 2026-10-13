---
name: publish
description: Commit every pending change and push to main, which deploys the site via GitHub Actions. Use when the user runs /publish or asks to publish, ship, deploy, or push the current changes.
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
