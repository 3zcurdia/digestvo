---
name: lb-digest
description: Read-only preview of today's Lobsters shortlist for the digest. Use when the user runs /lb-digest. Publishing is /digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# lb-digest

Preview only. Run, from the repo root:

```sh
python3 .opencode/skills/digest/scripts/fetch.py front --only lobsters
```

Show the user the table it prints. Then say: to research and publish these,
run `/digest`. Do not spawn researchers and do not write any files.
