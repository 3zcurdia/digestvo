---
name: translate
description: Translate digestvo posts from English to Spanish in place in src/_posts/. Use when the user runs /translate or asks to translate a post, translate the digest, translate to Spanish, or backfill translations.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# translate

You translate English digest posts to neutral Spanish, overwriting the same
file. No scripts — you read, translate, and write directly.

- Working directory: the repo root.
- Input (`$ARGUMENTS`): one `src/_posts/…md` path, several space-separated
  paths, or `--all` for every `src/_posts/*.md` (the backfill after `/digest`).
  If empty, ask which post to translate and stop.

## If something fails

| What happened | Do this |
|---|---|
| A path is not under `src/_posts/` or does not exist | Stop. Say which path and why. Do not translate anything else. |
| A file has no front matter or a missing `title` / `summary` / body | Say so for that file, skip it, continue with the rest. |
| The build fails | Paste the error. Do not edit the post to work around it. |

## Step 1 — Resolve targets

- `$ARGUMENTS` contains `--all`: every `src/_posts/*.md`, oldest first.
- Otherwise: the listed paths in the order given. Confirm each exists before
  touching any file.
- Never create a `-es` copy, never rename, never touch `src/` outside
  `src/_posts/`.

## Step 2 — Translate, one file at a time

Read the whole file, split front matter from body, and overwrite the same
path with the Spanish version:

- **Translate:** `title`, `summary`, `share_text`, and the full body.
- **Never touch:** `layout`, `date`, `categories`, `tags`, `source_url`,
  `hn_url`, `lobsters_url`, or any other URL / ID / code span / code block.
  `categories: digest` shapes the permalink; `tags` is the English taxonomy
  (`references/post-shape.md` explains why both stay verbatim).
- **Keep the shape:** same keys in the same order, same paragraph breaks,
  same markdown. A both-sites body keeps its two paragraphs and bold
  lead-ins, translated as `**En Hacker News.**` / `**En Lobsters.**`. The
  body still opens with a sentence, never a heading or list. No HTML, no
  emoji, no new links.
- **`share_text` stays ≤128 characters** after translation — shorten the
  wording, never pad. Hashtags and mentions allowed, same as English.
- **Spanish voice:** neutral Latin-American Spanish, usted-neutral, no
  voseo, no peninsular colloquialisms. Digest register (see
  `references/translation-guide.md`): faithful, not literal — a fluent
  reader must never feel the English underneath.
- One file at a time: read → translate → write → move to the next. Do not
  batch untranslated content across files.

## Step 3 — Build

```sh
bundle exec rake deploy
```

## Step 4 — Report

List each file translated plus whether the build passed. Finish with: `/`
lists the latest 10 posts, `/posts` all of them.

## Reference

- `references/translation-guide.md` — voice, terminology, and what stays
  in English.
- `references/post-shape.md` — which front-matter keys are data and why
  `tags` / `categories` never translate.
