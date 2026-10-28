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
- `image` is required on every post. It is the site-relative path to a
  1200x630 screenshot of the original article — the discussion page for a
  self post — captured by `write_post.py` under `src/images/digest/`. It
  feeds `og:image` and `twitter:image`; it is not rendered in the article
  body. Never hand-write or replace one: the capture script owns the file.
- `categories: digest` on every post. It is the only key that shapes the
  permalink (`/digest/YYYY/MM/DD/slug/`). The reader-facing bucket goes in
  `tags`, which never reaches the URL.
- `summary` renders twice: as the standfirst under the headline and as the
  story text on the index. It must stand alone.
- `share_text` feeds the share-to-X link (`Shared::ShareLinks`): one hook
  line, 128 characters or fewer, plain text. Hashtags and mentions allowed;
  no other markdown, no emoji. It must stand alone next to the post URL.
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
image: "/images/digest/<post basename>.jpg"
hn_url: "https://news.ycombinator.com/item?id=<id>"
share_text: "<one hook line, 128 chars or fewer>"
summary: >-
  <3-5 sentences>
---

<The take: what the thread agreed on, where it split, the sharpest objection.>
```

A self post (Ask HN, Tell HN) has no `source_url`; the thread is the story,
and `image` is a screenshot of that thread.

## Both sites

Both keys, Hacker News first, and one bolded lead-in per site. The layout turns
off the drop cap for these so it does not split the label.

```markdown
---
...
source_url: "<article URL>"
image: "/images/digest/<post basename>.jpg"
hn_url: "https://news.ycombinator.com/item?id=<id>"
lobsters_url: "https://lobste.rs/s/<short id>/<slug>"
share_text: "<one hook line, 128 chars or fewer>"
summary: >-
  <3-5 sentences>
---

**On Hacker News.** <the HN take>

**On Lobsters.** <the Lobsters take>
```

## Refresh

When a story is already published, `write_post.py` edits that file in place:
it replaces the take for each source researched today, appends a missing
source with its URL key, captures and appends `image` when the post predates
screenshots, and leaves `title`, `date`, `summary`, `share_text`, `tags` and
every existing key untouched. It never replaces an existing screenshot,
removes a section or a key, and never writes a second file for the same
article.
