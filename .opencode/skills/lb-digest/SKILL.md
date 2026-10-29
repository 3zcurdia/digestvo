---
name: lb-digest
description: Read-only preview of today's Lobsters shortlist for the digest. Use when the user runs /lb-digest. Ingestion is /ingest, curation is /digest.
compatibility: opencode
metadata:
  opencode/autoinvoke: "false"
---

# lb-digest

Preview only. Run, from the repo root:

```sh
python3 .opencode/skills/digest/scripts/fetch.py front --only lobsters
```

Show the user the table it prints. Then say: to research these and build the
candidate list, run `/ingest`, then `/digest` to curate and write. Do not
spawn researchers and do not write any files.
