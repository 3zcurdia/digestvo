# Story categories

The canonical list for the `digest` skill, shared by both workers. Copy the
matching bucket verbatim into the post's `tags` — these are labels the
newsletter's readers will come to recognise, so consistent wording matters more
than perfect fit.

| Category | Use it for |
|---|---|
| `AI/ML` | Models, training, inference, agents, AI tooling, AI policy incidents |
| `Dev Tools` | Languages, frameworks, editors, testing, developer experience |
| `Security & Privacy` | Vulnerabilities, breaches, tracking, encryption, surveillance |
| `Startups & Business` | Funding, founders, layoffs, pricing, company strategy |
| `Systems & Infra` | Databases, networking, hardware/cloud internals, performance, outages |
| `Science` | Research papers, biology, space, physics, maths, climate |
| `Policy & Law` | Regulation, courts, legislation, elections, antitrust |
| `Web & Platforms` | Browsers, the web platform, social platforms, big tech products |
| `Hardware` | Chips, devices, manufacturing, physical computing |
| `Show HN` | Projects people are launching — anything titled "Show HN" |
| `Culture` | Media, social commentary, work and life, anything not really news |

## Rules

**Ask HN is not Show HN.** An `Ask HN: how do you…` post is a question, and its
category is whatever the question is *about* — usually `Dev Tools`, `Culture`,
or `Startups & Business`. Reserve `Show HN` for launches.

**Lobsters has no title prefixes.** There is no "Show HN" or "Ask HN" on
Lobsters, so a launch there is not automatically `Show HN` — judge it on
whether it is actually someone presenting their own project. Most Lobsters
posts are somebody's blog post about a language, tool, or compiler, which is
`Dev Tools`.

**The subject wins over the framing.** A blog post about a court ruling is
`Policy & Law` even if it is on a tech blog. A product launch covered by a news
outlet is not `Show HN`.

**One category per story.** Never `AI/ML, Security & Privacy`. If a story
genuinely straddles two, pick the one a reader would most plausibly want.

**Use Lobsters' own tags as a prior, not as the answer.** The digest fetches
`lobsters_tags` — `rust`, `security`, `linux`, `gamedev`, and so on. They are a
reliable signal about what a post is about, but they are a different taxonomy
from this table and much finer-grained. `rust` points at `Dev Tools`; it is not a
`tags` value you can use directly.

**A story on both sites gets one category, not two.** Pick whichever site the
story reads more naturally as; do not try to reflect two communities in one
label.

## Ties that come up every week

Both sites straddle these constantly, so break them the same way every time or
the same story gets labelled differently on different days:

- **Dev Tools vs Systems & Infra** — what a developer *uses* is Dev Tools
  (languages, frameworks, editors, CI). What runs underneath everyone else is
  Systems & Infra (databases, networking, cloud, performance, outages). A Git
  platform is Dev Tools; a database company is Systems & Infra.
- **Security & Privacy vs Policy & Law** — if the story is about a technical
  flaw or a system collecting data, it is Security & Privacy even when a judge
  or a bill is involved. Use Policy & Law when the *lawmaking or ruling* is the
  subject and the technology is incidental.
- **AI/ML vs Startups & Business** — an AI company raising money or laying off
  staff is Startups & Business. An AI model, capability, or safety failure is
  AI/ML.
- **Science vs Culture** — if a reader would learn something about the world,
  it is Science. If the point is the human angle, it is Culture.

## Extending the list

A category used once is a typo, not a category. If two or more stories in one
digest want the same new bucket, say so when you report back and let the user
decide — then add the row here.

The repo has no canonical category list of its own yet (no `categories.yml`,
nothing in `config/initializers.rb`), so this file is the source of truth until
someone wires it into the site. `categories: digest` on each post is a separate
axis: it is the Bridgetown post category that determines the URL, not a story
category. Story categories go in the post's `tags`.