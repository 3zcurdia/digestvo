# Video shape

`scripts/write_video.py` writes every video page. Do not hand-write one; this
file documents what the script produces so a human can recognise a correct page
and fix the script, not the page, when something looks wrong.

Front matter is the whole interface between the skill and the site. It holds
data, never markup:

- **No HTML, SVG, icons or emoji.** The YouTube mark, the channel link, the
  runtime and the thumbnail box are drawn by
  `src/_components/shared/video_meta.erb`, `src/_layouts/video.erb` and
  `src/_components/shared/video_meta.css`.
- **A key is present or absent, never empty.** `channel_url` and `thumbnail`
  are the flags that draw those links.
- **`permalink` is what shapes the URL**, not the collection's own template.
  The `videos` collection declares `permalink: "/videos/:slug/"` as a fallback
  for hand-written files, but `:slug` falls back to the filename, which for a
  date-prefixed file includes the date. The explicit permalink is why the URL
  is `/videos/claude-code-code-skills-resultado-bizarro/` and not
  `/videos/2026-10-04-…/`.
- `date` is when *you* watched it and drives the sort order and the month
  grouping on the index. `published` is when the video itself went up.
  `watched` is the same day as `date`, written separately so the page can print
  it as a human date while `date` stays a timestamp.
- `summary` renders twice: as the standfirst under the headline and as the row
  text on the index. It must stand alone.
- `insights` is a YAML list of plain strings, never a markdown bullet list, so
  the layout can render the list and the index can show just the first entry
  without re-parsing the body.
- The body renders under a "Why it's worth your time" label with a drop cap on
  its first letter, so it opens with a sentence.

## Generated page

```markdown
---
layout: video
title: "<video title, verbatim>"
permalink: "/videos/<slug>/"
date: 2026-10-04 12:05:05 -0600
watched: 2026-10-03
tags: ["<one bucket>"]
channel: "<channel name>"
channel_url: "<channel URL, or absent>"
video_id: "<11 character id>"
video_url: "https://www.youtube.com/watch?v=<id>"
duration: "23:57"
published: "2026-03-15"
verdict: recommend
summary: >-
  <3-5 sentences>
thumbnail: "/images/videos/<slug>.jpg"
insights:
  - "<one point, 8-30 words>"
  - "<another>"
---

<Why it is worth the reader's time: the position, the objection, what to skip.>
```

`thumbnail` is written into `src/images/videos/`, not into the collection
directory. A collection directory holds collection resources; images belong to
the static-file reader, which picks them up from anywhere under `src/`.

The thumbnail is downloaded rather than hotlinked from `i.ytimg.com`. The About
page says the site is tracked by nobody, and a live request to a third party is
a tracker. Committing the file also means the page does not break when YouTube
changes its image URLs.

## Refresh

A video already on the site is edited in place, never duplicated: the existing
file keeps its slug and therefore its URL, while `summary`, `insights`, `take`,
the verdict and the metadata are replaced. Without that, running the skill twice
would split one video's write-up across two URLs and break anything linking to
the first. `write_video.py` also refuses to write a row the analyst passed on,
so a mistake costs a row rather than a page.