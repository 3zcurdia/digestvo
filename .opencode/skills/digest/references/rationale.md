# Why the pipeline is shaped this way

Nobody needs this file to run the digest. It records the reasoning so the
design is not undone by accident.

**Scripts own every mechanical step.** Merging by URL, detecting posts that
already exist, slugging, timestamps, YAML quoting and in-place edits are all
places where a model working from prose makes small, silent mistakes. The
skill is written so that the model only runs commands, spawns researchers,
asks one question and reports. A smaller or faster model can run it safely.

**Briefs are files, not replies.** A subagent's text reply gets wrapped in
prose, fenced, truncated or paraphrased. A file written to a known path and
checked by `validate_brief.py` does not. The researcher writes only the five
fields it actually produced; ids, URLs and `url_key` are joined from the story
file the script wrote, so nothing is copied by hand.

**Two levels, not three.** The parent spawns researchers directly. An earlier
version had one worker skill per site that in turn spawned researchers in
batches. Every hop lost fidelity and the batching loop was easy to get wrong.

**`url_key` is compared exactly.** Scheme, `www.`, tracking params and a
trailing slash are normalised away by one function in `_common.py`. The tracking
list cannot be exhaustive, so `merge.py` also flags same-host, same-path pairs
as near-duplicates and lets the user decide, and matches on discussion ids as a
second signal for posts already published.

**Enrich, never duplicate.** A story stays on a front page for days and running
the digest twice in one day is normal. A second post for the same article
splits its discussion across two URLs. A refresh replaces only the take for the
source researched today, adds a missing source, and keeps the post's identity
(title, date, summary, URL) so nothing that links to it breaks.

**One category per story, from a closed list.** Readers learn the buckets. A
bucket used once is a typo. The list lives in `categories.md` for humans and
in `_common.py` for the validator; change both together.

**The build is the test.** There is no test suite in this repo. `rake deploy`
takes about two seconds and parses every post, so it runs last.

**No emoji anywhere in the pipeline output.** Posts must not carry them, and a
model copies what it sees, so the tables use `HN`, `LB`, `new` and `refresh`.
