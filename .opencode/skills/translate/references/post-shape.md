# Post shape (translate skill)

Front matter is data, never markup. This is the contract from
`.opencode/skills/digest/references/post-template.md`, restated for the
translator: you change values, never the schema.

```markdown
---
layout: post            # NEVER translate, never touch
title: "..."            # TRANSLATE (headline)
date: ...               # NEVER touch
categories: digest      # NEVER touch — shapes the permalink
tags: ["..."]           # NEVER translate — English taxonomy, drives
                        # /tags/ archives and related-post matching
source_url: "..."       # NEVER touch
hn_url: "..."           # NEVER touch (presence draws the HN link)
lobsters_url: "..."     # NEVER touch (presence draws the Lobsters link)
share_text: "..."       # TRANSLATE, ≤128 chars after translation
summary: >-             # TRANSLATE (3-5 sentences, stands alone)
  ...
---

<The take, translated. Single source: plain paragraphs. Both sites:
**En Hacker News.** … blank line … **En Lobsters.** …>
```

Rules:

- A key is present or absent, never empty — do not add a key that was not
  there (`lobsters_url` absent means single-source; adding it draws a link
  to nowhere).
- Key order and quoting style stay as-is. `summary: >-` folding stays as-is.
- `tags` stays verbatim English even though it is reader-facing: translating
  `Dev Tools` to `Herramientas` would fork the `/tags/` archive and break
  `TagTaxonomy.related_posts` grouping. Localising tag display names is a
  site change, not a per-post translation.
- The body renders under a "The discussion" label (in `src/_layouts/post.erb`)
  with a drop cap — that label lives in the layout and is out of scope.
  The body itself still opens with a sentence, not a heading or list.
