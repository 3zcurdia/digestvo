#!/usr/bin/env python3
"""Fetch metadata and the transcript for each shortlisted video.

One yt-dlp call per video does both: the info JSON carries title, channel,
runtime, upload date, view count, description, chapters and thumbnail URLs, and
the subtitle track carries the transcript. No YouTube Data API key, no quota,
no OAuth.

A video with no captions at all is transcribed locally with whisper.cpp, which
is why the audio may be downloaded for that case only. Anything that fails is
recorded in the output file and the run continues — a missing transcript
degrades the write-up, it does not stop the pipeline.

Usage:
    python3 .opencode/skills/videos/scripts/fetch_video.py --from-candidates
    python3 .opencode/skills/videos/scripts/fetch_video.py --ids ZHjH9qSiJzQ,dQw4w9WgXcQ
    python3 .opencode/skills/videos/scripts/fetch_video.py URL [URL ...]

Options:
    --from-candidates   Read the shortlist candidates.py wrote.
    --ids A,B,C         Comma-separated video ids.
    --no-transcribe     Do not fall back to local transcription.
    --keep-going        Report every failure instead of stopping at the first.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

# English first, which includes YouTube's auto-translations of anything. Live
# chat is excluded: on a stream it is a wall of other people's messages rather
# than the speaker.
SUB_LANGS = "en.*,en,-live_chat"

# json3 is the format YouTube serves internally: clean text runs with timings.
# vtt is the fallback, so both have to be readable.
TIMESTAMP_RE = re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->")


def resolve_ids(args):
    if args.ids:
        return [vid for vid in (C.video_id_from(v.strip()) for v in args.ids.split(",")) if vid]
    if args.urls:
        return [vid for vid in (C.video_id_from(u) for u in args.urls) if vid]
    if args.from_candidates and os.path.isfile(C.FRONT_PATH):
        front = C.read_json(C.FRONT_PATH)
        return [item["video_id"] for item in front.get("candidates", [])]
    return []


def subtitle_files(video_id):
    """Subtitle files yt-dlp wrote for this video, json3 before vtt."""
    found = glob.glob(os.path.join(C.MEDIA_DIR, "{0}.*".format(video_id)))
    for extension in ("json3", "vtt", "srv1", "srv2", "srv3"):
        matches = sorted(p for p in found if os.path.splitext(p)[1] == "." + extension)
        if matches:
            return matches
    return []


def parse_json3(path):
    try:
        payload = json.loads(C.read_text(path))
    except (ValueError, OSError):
        return ""
    lines = []
    for event in payload.get("events") or []:
        text = "".join(seg.get("utf8", "") for seg in event.get("segs") or [])
        text = text.replace("\n", " ").strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def parse_vtt(path):
    lines = []
    for raw in C.read_text(path).split("\n"):
        line = raw.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if TIMESTAMP_RE.match(line) or line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line)
        if line:
            lines.append(line)
    return "\n".join(lines)


def clean_transcript(text):
    """Join wrapped lines into paragraphs and drop non-speech annotations.

    Auto-captions arrive one short clause per line, which reads as a teleprinter
    rather than a talk. Sentences that end in terminal punctuation start a new
    block; everything else is joined into the one before it.
    """
    blocks = []
    current = []
    for line in (text or "").split("\n"):
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"[\[\(].*[\]\)]", line):
            continue
        current.append(line)
        if re.search(r"[.!?][\"')\]]?$", line):
            blocks.append(" ".join(current))
            current = []
    if current:
        blocks.append(" ".join(current))
    return "\n\n".join(blocks)


def fetch_metadata(video_id):
    """The info JSON as a dict.

    A separate call from the transcript on purpose: --dump-single-json implies
    simulate, and a simulated run silently writes no subtitle file. Asking for
    both at once looks right and returns a video with no transcript.
    """
    payload = C.run_ytdlp([
        "--dump-single-json",
        "--socket-timeout", "30",
        C.watch_url(video_id),
    ], timeout=120)
    try:
        return json.loads(payload)
    except ValueError:
        raise C.VideoError("yt-dlp returned unparseable JSON")


def fetch_transcript(video_id, sub_langs):
    """The transcript as plain text, or "" when there is nothing to fetch.

    A 429 is YouTube rate-limiting, which happens when a run touches a lot of
    videos in quick succession. It is not this video's fault, so it returns ""
    and lets the caller fall through to local transcription rather than
    failing the run.
    """
    args = C.ytdlp_base_args() + C.cookies_args() + [
        "--no-playlist",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", sub_langs,
        "--sub-format", "json3/vtt",
        "--socket-timeout", "30",
        "--retries", "2",
        "-o", os.path.join(C.MEDIA_DIR, "{0}.%(ext)s".format(video_id)),
        C.watch_url(video_id),
    ]
    try:
        C.run_ytdlp(args, timeout=180)
    except C.VideoError as exc:
        if "429" in str(exc):
            return ""
        raise

    for path in subtitle_files(video_id):
        text = parse_json3(path) if path.endswith(".json3") else parse_vtt(path)
        if text.strip():
            return clean_transcript(text)
    return ""


def caption_languages(info):
    """(first choice, fallback) caption language codes, best first.

    A popular video can carry 150-odd auto-translated caption tracks, so
    "--sub-langs all" is never the answer: it downloads every one of them. The
    original-language track is the one worth falling back to when English is
    missing, and yt-dlp marks it with an -orig suffix.
    """
    manual = sorted((info.get("subtitles") or {}).keys())
    if manual:
        english = [code for code in manual if code.startswith("en")]
        return (english or manual)[0], None

    auto = (info.get("automatic_captions") or {}).keys()
    original = sorted(code for code in auto if code.endswith("-orig"))
    return None, (original[0] if original else None)


def transcribe_locally(video_id):
    """Download the audio and run whisper.cpp over it. Returns text or None."""
    cli = C.whisper_cmd()
    model = C.whisper_model()
    if not cli or not model:
        return None

    args = C.ytdlp_base_args() + C.cookies_args() + [
        "--no-playlist",
        "-f", "bestaudio/best",
        "-x", "--audio-format", "wav", "--audio-quality", "5",
        "--socket-timeout", "30",
        "-o", os.path.join(C.MEDIA_DIR, "{0}.%(ext)s".format(video_id)),
        C.watch_url(video_id),
    ]
    C.run_ytdlp(args, timeout=900)

    audio = os.path.join(C.MEDIA_DIR, "{0}.wav".format(video_id))
    if not os.path.isfile(audio):
        candidates = glob.glob(os.path.join(C.MEDIA_DIR, "{0}.wav".format(video_id)))
        if not candidates:
            return None
        audio = candidates[0]

    try:
        subprocess.run(
            [cli, "-m", model, "-f", audio, "-otxt", "-of",
             os.path.join(C.MEDIA_DIR, video_id), "-nt"],
            capture_output=True, text=True, timeout=3600, check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    finally:
        # The audio is a means, not an artefact. A two-hour talk is ~150MB and
        # nothing downstream wants it.
        if os.path.isfile(audio):
            os.remove(audio)

    out = os.path.join(C.MEDIA_DIR, "{0}.txt".format(video_id))
    return C.read_text(out) if os.path.isfile(out) else None


def pick_thumbnail(thumbnails):
    """The largest 16:9 thumbnail, preferring maxres then high."""
    usable = [t for t in thumbnails or [] if t.get("url") and t.get("width")]
    if not usable:
        return None
    def rank(thumb):
        name = str(thumb.get("id") or "")
        bonus = {"maxres": 3, "sddefault": 1, "hqdefault": 2}.get(name, 0)
        return (bonus, thumb["width"])
    return max(usable, key=rank)["url"]


def chapters_of(info):
    return [
        {"title": c.get("title", "").strip(), "start": c.get("start_time")}
        for c in (info.get("chapters") or [])
        if c.get("title")
    ]


def build(video_id, info, transcript, error):
    upload_date = info.get("upload_date") or ""
    published = None
    if len(upload_date) == 8 and upload_date.isdigit():
        published = "{0}-{1}-{2}".format(upload_date[:4], upload_date[4:6], upload_date[6:8])
    return {
        "video_id": video_id,
        "title": info.get("title") or "",
        "channel": info.get("channel") or info.get("uploader") or "",
        "channel_id": info.get("channel_id") or "",
        "channel_url": info.get("channel_url") or info.get("uploader_url") or "",
        "video_url": info.get("webpage_url") or C.watch_url(video_id),
        "duration": info.get("duration"),
        "duration_string": C.duration_string(info.get("duration")),
        "published": published,
        "view_count": info.get("view_count"),
        "description": C.clean_description(info.get("description")),
        "chapters": chapters_of(info),
        "thumbnail_url": pick_thumbnail(info.get("thumbnails")),
        "live_status": info.get("live_status"),
        "transcript": transcript,
        "transcript_error": error,
    }


def unprocessable(record):
    """Why this video will not become a page, or None if it is fine."""
    if record["live_status"] in ("is_live", "is_upcoming"):
        return "live or upcoming"
    if record["duration"] is not None and record["duration"] < C.MIN_DURATION:
        return "under {0}s".format(C.MIN_DURATION)
    if not record["title"]:
        return "no title"
    return None


def handle(video_id, args):
    """Fetch one video. Returns (status, message)."""
    try:
        info = fetch_metadata(video_id)
    except C.VideoError:
        info = None

    if info is None:
        # Unavailable, private, or deleted. A transcript for it would be a lie.
        return "fail", "unavailable, private, or deleted"

    # English first, which includes YouTube's auto-translations. Failing that,
    # the original-language track — a talk captioned only in German is still
    # readable, and reading it beats guessing from metadata alone.
    transcript = fetch_transcript(video_id, SUB_LANGS)
    if not transcript:
        _first, original = caption_languages(info)
        if original:
            print("      no English captions, trying {0}".format(original))
            transcript = fetch_transcript(video_id, original)

    error = None
    if not transcript:
        error = "no caption track"
        if not args.no_transcribe:
            print("      no captions, transcribing locally (slow)...")
            spoken = transcribe_locally(video_id)
            if spoken and spoken.strip():
                transcript = clean_transcript(spoken)
                error = None
            else:
                error = "no captions and local transcription unavailable"

    record = build(video_id, info, transcript, error)
    reason = unprocessable(record)
    if reason:
        C.write_json(C.video_json_path(video_id), dict(record, skipped=reason))
        return "skip", reason

    C.write_json(C.video_json_path(video_id), record)
    if record["transcript"]:
        return "ok", "{0} words".format(C.count_words(record["transcript"]))
    return "ok", "NO TRANSCRIPT ({0})".format(record["transcript_error"])


def main():
    parser = argparse.ArgumentParser(description="Fetch video metadata and transcripts.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--from-candidates", action="store_true")
    group.add_argument("--ids", help="Comma-separated video ids")
    group.add_argument("urls", nargs="*", help="YouTube URLs or bare ids")
    parser.add_argument("--no-transcribe", action="store_true",
                        help="Do not fall back to local transcription")
    parser.add_argument("--keep-going", action="store_true",
                        help="Report every failure instead of stopping at the first")
    args = parser.parse_args()

    ids = resolve_ids(args)
    if not ids:
        C.fail("no video ids given. Use --from-candidates, --ids, or pass a URL.")
    os.makedirs(C.MEDIA_DIR, exist_ok=True)

    print("")
    print("  fetching {0} video(s)\n".format(len(ids)))
    kept, skipped, failed = [], [], []
    for index, video_id in enumerate(ids, 1):
        print("  [{0}/{1}] {2}".format(index, len(ids), video_id))
        status, message = handle(video_id, args)
        if status == "ok":
            kept.append(video_id)
            print("      ok  {0}".format(message))
        elif status == "skip":
            skipped.append((video_id, message))
            print("      SKIP {0}".format(message))
        else:
            failed.append((video_id, message))
            print("      FAIL {0}".format(message))
            if not args.keep_going:
                print("")
                C.fail("stopped at the first failure. Re-run with --keep-going to see them all.")

    print("")
    print("  {0} ready, {1} skipped, {2} failed".format(len(kept), len(skipped), len(failed)))
    for video_id, reason in skipped:
        print("    SKIP {0}  {1}".format(video_id, reason))
    for video_id, reason in failed:
        print("    FAIL {0}  {1}".format(video_id, reason))
    print("")
    if not kept:
        print("  Nothing to analyse.")
        return 1
    print("  Spawn one analyst per video in .opencode/tmp/videos/video-*.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())