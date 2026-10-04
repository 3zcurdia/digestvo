---
name: hn-digest
description: Read-only preview of today's Hacker News shortlist for the digest. Use when the user runs /hn-digest. Publishing is /digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# hn-digest

Preview only. Run, from the repo root:

```sh
python3 .opencode/skills/digest/scripts/fetch.py front --only hn
```

Show the user the table it prints. Then say: to research and publish these,
run `/digest`. Do not spawn researchers and do not write any files.
