# Translation guide

Neutral Latin-American Spanish for the whole post. The reader is technical
and reads Spanish natively — the prose must feel written in Spanish, not
translated from English.

## Voice

- Second person only when the English uses it. Default to impersonal
  constructions (`se`, passive with `se`) over inventing a subject.
- Keep the digest register: "Most commenters land on…" becomes
  "La mayoría de los comentarios coinciden en…", not a word-for-word gloss.
  Translate the argument, keep the sharpness.
- Diacritics are not optional: `discusión`, `técnica`, `código`, `ultimo`
  is always `último`. When unsure, RAE spelling wins.

## Terminology

- Tech terms with a settled borrowing stay borrowed: *software, hardware,
  plugin, daemon, sandbox, background subagent, hot-reload, scroll,
  WebGL, Pixel, MacBook*. Do not invent calques (`demonio` for daemon,
  `arena` for sandbox).
- Translate the concept when Spanish has the word: *release → versión*,
  *take → balance / lectura*, *thread → hilo*, *post → publicación*
  (but `Ask HN` / `Show HN` / `Tell HN` never translate), *performance →
  rendimiento*, *build → compilación* only for the software build.
- Proper nouns never translate: OpenCode, Hacker News, Lobsters, Code Mode,
  MCP, OpenAPI, M3/M4, TUI. `On Hacker News / On Lobsters` lead-ins become
  `En Hacker News / En Lobsters` — the site name stays English.
- Acronyms keep their English expansion on first use only if the English
  post expands them; otherwise leave them bare.

## What stays in English, always

Code spans and fences, commands, package names (`@opencode/client`),
URLs, Hacker News IDs, dates, numbers, and quoted error strings. If a
sentence quotes UI text (`"Night edition"`), translate the sentence around
it and leave the quoted string verbatim.

## share_text

One hook line, ≤128 characters, plain text, must stand alone next to the
post URL. Translate last and compress: drop articles and subordinate
clauses before dropping information. Count characters, not words.
