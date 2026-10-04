# Post template

Copy one of these into `src/_posts/YYYY-MM-DD-<slug>.md` and replace every
`<…>` placeholder. Front matter is the whole interface between the digest and
the site: write data here, never markup.

- **No HTML, SVG, icons or emoji in a post.** The source marks, the "Read the
  original" link and the date line are all drawn by
  `src/_components/shared/source_links.erb` and `src/_layouts/post.erb` from
  the keys below. A post that hand-draws an icon drifts from every other post
  the first time the component changes.
- **Drop a key you have no value for.** Do not leave it empty: an empty
  `lobsters_url:` is still a key, and keeps the template honest only by luck.
- `summary` renders twice: as the italic standfirst under the headline, and as
  the story text on the index. Write it to stand alone, 3-4 sentences.
- The body renders under a "The discussion" label with a drop cap on its first
  letter, so it must open with a sentence, not a heading, list or quote.

## Single source

Use for a story that ran on one site. Keep exactly one of `hn_url` /
`lobsters_url`. The body is that site's take, with no bolded lead-in.

```markdown
---
layout: post
title: "<headline, verbatim>"
date:   <output of: date "+%Y-%m-%d %H:%M:%S %z">
categories: digest
tags: ["<one bucket from references/categories.md>"]
source_url: <article URL>
hn_url: https://news.ycombinator.com/item?id=<id>
summary: >-
  <3-4 sentences: what the article says, standing on its own.>
---

<The discussion summary: what the thread agreed on, where it split, and the
sharpest objection. No second summary of the article, no "Read more".>
```

## Both sites

Use when the story ran on Hacker News and Lobsters. Both keys, and one bolded
lead-in paragraph per site, Hacker News first. The layout turns off the drop
cap for these posts so it does not split the "On Hacker News." label.

```markdown
---
layout: post
title: "<headline, verbatim>"
date:   <output of: date "+%Y-%m-%d %H:%M:%S %z">
categories: digest
tags: ["<one bucket from references/categories.md>"]
source_url: <article URL>
hn_url: https://news.ycombinator.com/item?id=<id>
lobsters_url: https://lobste.rs/s/<short id>/<slug>
summary: >-
  <3-4 sentences: what the article says, standing on its own.>
---

**On Hacker News.** <the HN take>

**On Lobsters.** <the Lobsters take>
```
