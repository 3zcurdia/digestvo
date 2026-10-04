#!/usr/bin/env python3
"""Shared helpers for the videos skill. Not a CLI.

Everything mechanical lives here so the model only runs commands, spawns
analysts, curates one video at a time, and reports.

There is no API key and no OAuth client in this skill. yt-dlp does everything
the YouTube Data API would have done — title, channel, runtime, view count,
upload date, description, chapters and thumbnails — using your own browser
session, so the only secret involved is a cookies.txt file outside the repo.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------- layout ---

RUN_DIR = ".opencode/tmp/videos"
BRIEFS_DIR = os.path.join(RUN_DIR, "briefs")
FRONT_PATH = os.path.join(RUN_DIR, "front.json")
CANDIDATES_PATH = os.path.join(RUN_DIR, "candidates.json")
REPORT_PATH = os.path.join(RUN_DIR, "report.json")
MEDIA_DIR = os.path.join(RUN_DIR, "media")
VIDEOS_DIR = "src/_videos"
THUMBS_DIR = "src/images/videos"

# Secrets live outside the repo at 0600, the way this machine already stores
# them. cookies.txt is the only one: it is a live signed-in session and anyone
# who reads it is logged in as you, with no password and no second factor.
CONFIG_DIR = os.path.expanduser("~/.config/digestvo")
COOKIES_PATH = os.path.join(CONFIG_DIR, "cookies.txt")
TAKEOUT_PATH = os.path.join(CONFIG_DIR, "takeout.json")

# Sources of "what you watched", in the order candidates.py prefers them.
HISTORY_FEED = "https://www.youtube.com/feed/history"
WATCH_LATER_FEED = "https://www.youtube.com/playlist?list=WL"

# Anything shorter is a clip, not something worth a page.
MIN_DURATION = 180

CATEGORIES = [
    "AI/ML",
    "AI Release",
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
# Same taxonomy as the digest, so a reader learns one set of buckets site-wide.
VERDICTS = ["recommend", "skip"]

BRIEF_FIELDS = {
    "category": str,
    "readable": bool,
    "verdict": str,
    "summary": str,
    "insights": list,
    "take": str,
}
SUMMARY_SENTENCES = (3, 6)
SUMMARY_WORDS = (40, 110)
TAKE_SENTENCES = (3, 7)
TAKE_WORDS = (60, 200)
INSIGHT_COUNT = (3, 5)
INSIGHT_WORDS = (8, 30)

UA = "digestvo-videos-skill/1.0 (newsletter aggregator)"

VIDEO_ID_RE = re.compile(r"(?:[?&]v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)


class VideoError(Exception):
    """A failure the calling model should report verbatim and stop on."""


def fail(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------- yt-dlp ---

def ytdlp_cmd():
    """Homebrew's yt-dlp when it is installed, `uv tool run` otherwise.

    Homebrew is the documented path and what check_setup.py tells you to
    install. The fallback exists so a missing or broken brew build never
    hard-fails the pipeline, and so a stale one can be worked around without
    editing a script.
    """
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uv"):
        return ["uv", "tool", "run", "--quiet", "yt-dlp"]
    fail("no yt-dlp found. Install it with: brew install yt-dlp")


def ytdlp_base_args():
    """Flags every call shares.

    --ignore-config keeps a user's ~/.config/yt-dlp/config from quietly
    redirecting output or adding --mark-watched underneath us. Nothing in this
    skill writes to YouTube: --mark-watched is never passed (it fires even
    under --simulate) and no playlist is ever inserted into or deleted.
    """
    return [
        "--ignore-config",
        "--no-warnings",
        "--no-progress",
        "--no-mark-watched",
    ]


def cookies_args():
    """--cookies when a session file exists, otherwise nothing."""
    if cookies_available():
        return ["--cookies", COOKIES_PATH]
    return []


def run_ytdlp(args, timeout=180):
    """Run yt-dlp and return its stdout. Raises VideoError on failure.

    stderr is folded into the error message because yt-dlp puts the only
    useful diagnostic ("Sign in to confirm you're not a bot", "The playlist does
    not exist") there.
    """
    cmd = ytdlp_cmd() + ytdlp_base_args() + list(args)
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        raise VideoError("yt-dlp timed out after {0}s: {1}".format(timeout, " ".join(args[:2])))
    except FileNotFoundError:
        raise VideoError("yt-dlp could not be started")
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        tail = detail[-1] if detail else "exit {0}".format(proc.returncode)
        raise VideoError("yt-dlp failed: " + tail)
    return proc.stdout


def cookies_available():
    return bool(COOKIES_PATH) and os.path.isfile(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0


# whisper.cpp has used more than one cache directory name across builds, so the
# search covers all of them rather than assuming one. Anything installed from a
# package manager also drops models in its own share directory.
WHISPER_MODEL_DIRS = (
    "~/.cache/whisper-cpp",
    "~/.cache/whisper.cpp",
    "~/.cache/whispercpp",
    "/opt/homebrew/share/whisper.cpp",
    "/usr/local/share/whisper.cpp",
)

# Bigger is a better transcript. For an English talk the `.en` build beats the
# multilingual one at the same size; both are accepted, since plenty of talks
# are not in English.
WHISPER_SIZES = ("tiny", "base", "small", "medium", "large")


def whisper_model():
    """The best ggml model on this machine, or None.

    Homebrew's whisper.cpp ships only `for-tests-ggml-tiny.bin`, which is a
    575KB fixture and not fit for turning speech into an argument. A real model
    is 75MB (tiny) to 3GB (large).
    """
    best = None
    best_rank = ()
    for directory in WHISPER_MODEL_DIRS:
        root = os.path.expanduser(directory)
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            if not name.startswith("ggml-") or not name.endswith(".bin"):
                continue
            if "for-tests" in name:
                continue
            stem = name[len("ggml-"):-len(".bin")]
            english = stem.endswith(".en")
            if english:
                stem = stem[:-len(".en")]
            # Matches base, base-v3, large-v3-turbo and friends.
            size = next((s for s in WHISPER_SIZES if stem == s or stem.startswith(s + "-")), "")
            if not size:
                continue
            rank = (WHISPER_SIZES.index(size), 1 if english else 0)
            if rank > best_rank:
                best_rank, best = rank, os.path.join(root, name)
    return best


def whisper_cmd():
    return shutil.which("whisper-cli")


# ------------------------------------------------------------------ http ---

def download(url, dest, timeout=60):
    """Fetch a URL to a path. Used for thumbnails only."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        raise VideoError("HTTP {0} fetching {1}".format(exc.code, url))
    except urllib.error.URLError as exc:
        raise VideoError("could not reach {0}: {1}".format(url, exc.reason))
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(data)


# ------------------------------------------------------------------ text ---

def slugify(title, max_words=8, max_len=70):
    """Lowercase ASCII slug, stop words dropped, capped in words and length."""
    text = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    text = text.lower().replace("'", "").replace("’", "")
    words = [w for w in re.split(r"[^a-z0-9]+", text) if w]
    kept = [w for w in words if w not in STOP_WORDS] or words
    slug = "-".join(kept[:max_words])
    while len(slug) > max_len and "-" in slug:
        slug = slug.rsplit("-", 1)[0]
    return slug or "video"


STOP_WORDS = {
    "a", "an", "the", "of", "to", "and", "or", "for", "is", "are", "be", "was",
    "in", "on", "at", "as", "from", "with", "that", "this", "it", "its", "by",
    "we", "you", "your", "our", "how", "why", "what", "when", "do", "does",
    "did", "not", "no", "so", "than", "vs", "just", "more", "most", "some",
    "all", "any", "can", "will", "my", "me", "i",
}


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
    protected = re.sub(r"\b(e\.g|i\.e|vs|etc|Mr|Mrs|Dr|St|No|Inc|Ltd|Jr|Sr|v)\.", r"\1<dot>", text)
    protected = re.sub(r"(\d)\.(\d)", r"\1<dot>\2", protected)
    ends = re.findall(r"[.!?]+(?=[\s\"')\]]|$)", protected)
    return max(1, len(ends))


def in_range(value, bounds):
    low, high = bounds
    return low <= value <= high


def now_stamp():
    """(YYYY-MM-DD, 'YYYY-MM-DD HH:MM:SS %z') in the machine's local zone."""
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S %z")


def today():
    return now_stamp()[0]


def yaml_quote(value):
    """A double-quoted YAML scalar. JSON string escaping is valid YAML."""
    return json.dumps(str(value), ensure_ascii=False)


def duration_string(seconds):
    """3708 -> '1:01:48'; 2322 -> '38:42'. None for anything unusable."""
    try:
        total = int(seconds)
    except (TypeError, ValueError):
        return None
    if total <= 0:
        return None
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return "{0}:{1:02d}:{2:02d}".format(hours, minutes, secs) if hours else "{0}:{1:02d}".format(minutes, secs)


def video_id_from(url_or_id):
    """A bare 11-char id, or the id inside any YouTube URL shape, else None."""
    text = (url_or_id or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", text):
        return text
    match = VIDEO_ID_RE.search(text)
    return match.group(1) if match else None


def watch_url(video_id):
    return "https://www.youtube.com/watch?v={0}".format(video_id)


def clean_description(text, limit=4000):
    """Trim a video description to something a brief can be written from.

    Descriptions carry the chapters, the links and several paragraphs of channel
    boilerplate. Keeping the head and dropping the tail keeps the useful part
    without carrying 8KB of "follow us on" into every analyst's context.
    """
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit("\n", 1)[0] + "\n[description truncated]"


# ----------------------------------------------------------------- files ---

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


def video_json_path(video_id):
    return os.path.join(RUN_DIR, "video-{0}.json".format(video_id))


def brief_path(video_id):
    return os.path.join(BRIEFS_DIR, "{0}.json".format(video_id))


def parse_brief_name(path):
    """briefs/ZHjH9qSiJzQ.json -> 'ZHjH9qSiJzQ', else None."""
    name = os.path.splitext(os.path.basename(path))[0]
    return name if re.fullmatch(r"[A-Za-z0-9_-]{11}", name) else None


def clear_run_dir():
    """Wipe the run directory so a shortlist can never mix two runs."""
    if os.path.isdir(RUN_DIR):
        shutil.rmtree(RUN_DIR)
    os.makedirs(BRIEFS_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)


# ---------------------------------------------------------- front matter ---

def split_post(text):
    """(front_matter_text, body) or None when the file has no front matter."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    return match.group(1), text[match.end():]


def front_matter_keys(fm_text):
    """Top-level scalar keys only, by a flat line scan.

    Indented continuation lines (a `summary: >-` block) and the indented items
    of a list (`insights:`) are skipped, so they can never be mistaken for
    top-level keys.
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
            keys[name.strip()] = value
    return keys


def video_record(path):
    """What merge.py and write_video.py know about one published video."""
    parts = split_post(read_text(path))
    data = front_matter_keys(parts[0]) if parts else {}
    return {
        "path": path,
        "slug": os.path.splitext(os.path.basename(path))[0],
        "title": data.get("title"),
        "video_id": data.get("video_id"),
        "video_url": data.get("video_url"),
    }


def published_videos():
    """Every video already on the site, keyed by video_id for exact dedupe."""
    records = []
    if not os.path.isdir(VIDEOS_DIR):
        return records
    for name in sorted(os.listdir(VIDEOS_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(VIDEOS_DIR, name)
        record = video_record(path)
        if record["video_id"]:
            records.append(record)
    return records