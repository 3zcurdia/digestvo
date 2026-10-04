#!/usr/bin/env python3
"""Shared helpers for the digest scripts. Not a CLI.

Every script in this directory imports from here, so URL normalisation, the
run directory layout, the taxonomy and the front-matter scanner exist exactly
once. The model never has to reproduce any of it.
"""

import html
import json
import os
import re
import sys
import textwrap
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------- layout ---

RUN_DIR = ".opencode/tmp/digest"
BRIEFS_DIR = os.path.join(RUN_DIR, "briefs")
FRONT_PATH = os.path.join(RUN_DIR, "front.json")
CANDIDATES_PATH = os.path.join(RUN_DIR, "candidates.json")
REPORT_PATH = os.path.join(RUN_DIR, "report.json")
POSTS_DIR = "src/_posts"
RESEARCHER_DOC = ".opencode/skills/digest/references/researcher.md"

SOURCES = {
    "hn": {"label": "Hacker News", "key": "hn_url", "short": "HN"},
    "lobsters": {"label": "Lobsters", "key": "lobsters_url", "short": "LB"},
}
SOURCE_ORDER = ["hn", "lobsters"]

CATEGORIES = [
    "AI/ML",
    "Dev Tools",
    "Security & Privacy",
    "Startups & Business",
    "Systems & Infra",
    "Science",
    "Policy & Law",
    "Web & Platforms",
    "Hardware",
    "Show HN",
    "Culture",
]
SENTIMENTS = ["enthusiasm", "skeptical", "mixed", "neutral"]

# Brief fields the researcher writes. Everything else is joined from the
# story file by merge.py, so the model never copies ids or URLs by hand.
BRIEF_FIELDS = {
    "category": str,
    "readable": bool,
    "summary": str,
    "take": str,
    "sentiment": str,
}
SUMMARY_SENTENCES = (3, 6)
SUMMARY_WORDS = (40, 110)
TAKE_SENTENCES = (3, 7)
TAKE_WORDS = (60, 200)

UA = "digestvo-digest-skill/2.0 (newsletter aggregator)"

# Query params that identify the referrer rather than the page. Everything
# else is kept: a YouTube watch URL lives entirely in its query string.
TRACKING = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "dclid", "igshid", "mc_cid", "mc_eid", "ref", "ref_src",
    "ref_url", "source", "spm", "at_medium", "at_campaign", "gift", "amp",
    "si", "s_cid", "sr_share", "guccounter", "yclid", "__twitter_impression",
    "mcg", "pk_campaign", "pk_kwd", "hsa_acc", "hsa_cam",
}

TAG_RE = re.compile(r"<[^>]+>")
HN_ID_RE = re.compile(r"news\.ycombinator\.com/item\?id=(\d+)")
LOBSTERS_ID_RE = re.compile(r"lobste\.rs/s/([A-Za-z0-9]+)")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)
LEAD_IN_RE = re.compile(r"^\*\*On (Hacker News|Lobsters)\.\*\*\s*", re.M)


class DigestError(Exception):
    """A failure the calling model should report verbatim and stop on."""


def fail(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


# ------------------------------------------------------------------- http ---

def fetch_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        raise DigestError("HTTP {0} from {1}".format(exc.code, url))
    except urllib.error.URLError as exc:
        raise DigestError("could not reach {0}: {1}".format(url, exc.reason))
    except json.JSONDecodeError:
        raise DigestError("non-JSON response from {0}".format(url))


# ------------------------------------------------------------------- text ---

def clean(text):
    """Strip markup, decode entities, collapse whitespace."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub(" ", text))).strip()


def url_key(url):
    """Reduce a URL to a comparable identity.

    Scheme, www, tracking params and trailing slash are normalised away; the
    path keeps its case because paths are case-sensitive. merge.py and
    collide.py compare these strings exactly.
    """
    if not url:
        return ""
    parts = urllib.parse.urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = urllib.parse.unquote(parts.path or "").rstrip("/")
    kept = [
        (k, v)
        for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in TRACKING
    ]
    kept.sort()
    query = urllib.parse.urlencode(kept)
    return host + path + ("?" + query if query else "")


def hn_id_from(url):
    m = HN_ID_RE.search(url or "")
    return m.group(1) if m else None


def lobsters_id_from(url):
    m = LOBSTERS_ID_RE.search(url or "")
    return m.group(1) if m else None


STOP_WORDS = {
    "a", "an", "the", "of", "to", "and", "or", "for", "is", "are", "be", "was",
    "were", "with", "that", "this", "its", "it", "by", "at", "as", "from",
    "we", "you", "your", "our", "in", "on", "into", "via", "about", "how",
    "why", "what", "when", "do", "does", "did", "not", "no", "so", "than",
    "vs", "going", "need", "pretty", "much", "get", "got", "trying", "just",
    "more", "most", "some", "all", "any", "can", "will", "should", "would",
}


def slugify(title, max_words=8, max_len=70):
    """Lowercase ASCII slug, stop words dropped, capped in words and length."""
    text = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    text = text.lower().replace("'", "").replace("’", "")
    text = re.sub(r"^(show|ask|tell) hn:\s*", "", text)
    words = [w for w in re.split(r"[^a-z0-9]+", text) if w]
    kept = [w for w in words if w not in STOP_WORDS] or words
    kept = kept[:max_words]
    slug = "-".join(kept)
    while len(slug) > max_len and "-" in slug:
        slug = slug.rsplit("-", 1)[0]
    return slug or "story"


def wrap(text, width=80, indent=""):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return textwrap.fill(
        text, width=width, initial_indent=indent, subsequent_indent=indent,
        break_long_words=False, break_on_hyphens=False,
    )


def count_words(text):
    return len(re.findall(r"\S+", text or ""))


def count_sentences(text):
    """Approximate: terminal punctuation followed by space or end of text."""
    text = (text or "").strip()
    if not text:
        return 0
    # Protect common abbreviations so they do not count as sentence ends.
    protected = re.sub(r"\b(e\.g|i\.e|vs|etc|Mr|Mrs|Dr|St|No|Inc|Ltd|Jr|Sr|U\.S|v)\.", r"\1<dot>", text)
    protected = re.sub(r"(\d)\.(\d)", r"\1<dot>\2", protected)
    ends = re.findall(r"[.!?]+(?=[\s\"')\]]|$)", protected)
    return max(1, len(ends))


def now_stamp():
    """(YYYY-MM-DD, 'YYYY-MM-DD HH:MM:SS +zzzz') in the machine's local zone."""
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S %z")


def yaml_quote(value):
    """A double-quoted YAML scalar. JSON string escaping is valid YAML."""
    return json.dumps(str(value), ensure_ascii=False)


# -------------------------------------------------------------------- files ---

def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def story_path(source, story_id):
    return os.path.join(RUN_DIR, "story-{0}-{1}.json".format(source, story_id))


def brief_path(source, story_id):
    return os.path.join(BRIEFS_DIR, "{0}-{1}.json".format(source, story_id))


def parse_brief_name(path):
    """briefs/hn-49942706.json -> ('hn', '49942706'), else None."""
    name = os.path.splitext(os.path.basename(path))[0]
    m = re.fullmatch(r"(hn|lobsters)-([A-Za-z0-9]+)", name)
    return (m.group(1), m.group(2)) if m else None


# ------------------------------------------------------------ front matter ---

def split_post(text):
    """(front_matter_text, body) or None when the file has no front matter."""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None
    return m.group(1), text[m.end():]


def front_matter_keys(fm_text):
    """Top-level scalar keys only, by a flat line scan.

    Indented continuation lines (a `summary: >-` block) are skipped, so they
    can never be mistaken for top-level keys. Quotes are stripped from values.
    """
    keys = {}
    for line in fm_text.split("\n"):
        if not line or line[0] in " \t-#":
            continue
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if value:
            keys[name.strip()] = html.unescape(value)
    return keys


def post_record(path):
    """What collide.py and merge.py know about one published post."""
    text = read_text(path)
    parts = split_post(text)
    data = front_matter_keys(parts[0]) if parts else {}
    source = data.get("source_url", "")
    return {
        "path": path,
        "slug": os.path.splitext(os.path.basename(path))[0],
        "title": data.get("title"),
        "source_url": source,
        "url_key": url_key(source),
        "hn_id": hn_id_from(data.get("hn_url", "")),
        "lobsters_id": lobsters_id_from(data.get("lobsters_url", "")),
    }


def split_body_sections(body):
    """Body -> {'hn': text, 'lobsters': text} or {'_single': text}.

    A both-sites body has bolded lead-ins; a single-source body has none.
    Text is returned without the lead-in, unwrapped to one line.
    """
    body = body.strip()
    matches = list(LEAD_IN_RE.finditer(body))
    if not matches:
        return {"_single": re.sub(r"\s+", " ", body)}
    sections = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        source = "hn" if m.group(1) == "Hacker News" else "lobsters"
        sections[source] = re.sub(r"\s+", " ", body[m.end():end]).strip()
    return sections
