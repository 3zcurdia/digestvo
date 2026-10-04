# Post shape

`scripts/write_post.py` writes every digest post. Do not hand-write one; this
file documents what the script produces so a human can recognise a correct
post and fix the script, not the post, when something looks wrong.

Front matter is the whole interface between the digest and the site. It holds
data, never markup:

- **No HTML, SVG, icons or emoji in a post.** The source marks, the "Read the
  original" link and the date are drawn by
  `src/_components/shared/source_links.erb` and `src/_layouts/post.erb` from
  the keys below.
- **A key is present or absent, never empty.** `hn_url` and `lobsters_url`
  are the flags that draw the Hacker News and Lobsters links.
- `categories: digest` on every post. It is the only key that shapes the
  permalink (`/digest/YYYY/MM/DD/slug/`). The reader-facing bucket goes in
  `tags`, which never reaches the URL.
- `summary` renders twice: as the standfirst under the headline and as the
  story text on the index. It must stand alone.
- The body renders under a "The discussion" label with a drop cap on its first
  letter, so it opens with a sentence, not a heading or list.

## Single source

```markdown
---
layout: post
title: "<headline, verbatim>"
date: <local time, YYYY-MM-DD HH:MM:SS +zzzz>
categories: digest
tags: ["<one bucket from categories.md>"]
source_url: "<article URL>"
hn_url: "https://news.ycombinator.com/item?id=<id>"
summary: >-
  <3-5 sentences>
---

<The take: what the thread agreed on, where it split, the sharpest objection.>
```

A self post (Ask HN, Tell HN) has no `source_url`; the thread is the story.

## Both sites

Both keys, Hacker News first, and one bolded lead-in per site. The layout turns
off the drop cap for these so it does not split the label.

```markdown
---
...
hn_url: "https://news.ycombinator.com/item?id=<id>"
lobsters_url: "https://lobste.rs/s/<short id>/<slug>"
summary: >-
  <3-5 sentences>
---

**On Hacker News.** <the HN take>

**On Lobsters.** <the Lobsters take>
```

## Refresh

When a story is already published, `write_post.py` edits that file in place:
it replaces the take for each source researched today, appends a missing
source with its URL key, and leaves `title`, `date`, `summary`, `tags` and
every existing key untouched. It never removes a section or a key, and never
writes a second file for the same article.
