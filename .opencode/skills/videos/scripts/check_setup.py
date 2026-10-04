#!/usr/bin/env python3
"""Report whether this machine can run the videos skill, and what is missing.

Run this before anything else. Every other script assumes the tools here exist,
and each one names the exact command that fixes it.

Usage:
    python3 .opencode/skills/videos/scripts/check_setup.py

Exits 0 when the skill can run, 1 when a hard requirement is missing.
"""

import os
import stat
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

OK = "  ok  "
WARN = " warn "
BAD = " MISS "


def line(mark, name, detail, fix=None):
    print("[{0}] {1:<14} {2}".format(mark, name, detail))
    if fix:
        print("         {0}".format(C.wrap(fix, width=70, indent="fix: ")))


def check_ytdlp():
    cmd = C.ytdlp_cmd()
    label = " ".join(cmd)
    try:
        proc = subprocess.run(cmd + ["--version"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        line(BAD, "yt-dlp", "not runnable", "brew install yt-dlp")
        return False
    if proc.returncode != 0:
        line(BAD, "yt-dlp", "not runnable", "brew install yt-dlp")
        return False

    version = proc.stdout.strip()
    if cmd[0] == "yt-dlp":
        # Homebrew and other third-party installs disable `-U`, so the only way
        # forward is the package manager. A stale extractor is the single most
        # common cause of "subtitles came back empty", so this is worth printing
        # every run rather than only on failure.
        line(OK, "yt-dlp", "{0} (homebrew)".format(version))
        print("         if a video stops yielding subtitles, run: brew upgrade yt-dlp")
    else:
        line(WARN, "yt-dlp", "{0} (via uv, not installed)".format(version))
        print("         to make this the normal path: brew install yt-dlp")
    return True


def check_ffmpeg():
    path = C.shutil.which("ffmpeg")
    if not path:
        line(WARN, "ffmpeg", "missing", "needed only for the local-transcription fallback")
        return
    line(OK, "ffmpeg", path)


def check_cookies():
    if not C.cookies_available():
        line(WARN, "cookies", "no session file at {0}".format(C.COOKIES_PATH))
        print("         without it there is no watch history. Either export one, or")
        print("         point takeout.json at a Takeout export. See references/setup.md")
        return None

    mode = stat.S_IMODE(os.stat(C.COOKIES_PATH).st_mode)
    size = os.path.getsize(C.COOKIES_PATH)
    if size < 100:
        line(WARN, "cookies", "file is only {0} bytes — probably not a real export".format(size))
        print("         export it while sitting on youtube.com, in Netscape format")
        return None
    if mode & 0o077:
        line(WARN, "cookies", "world/group readable (mode {0:o})".format(mode))
        print("         a cookies.txt is a live signed-in session. Run:")
        print("         chmod 600 {0}".format(C.COOKIES_PATH))
    else:
        line(OK, "cookies", "{0} bytes, mode 0600".format(size))
    return True


def check_takeout():
    if not os.path.isfile(C.TAKEOUT_PATH):
        line(WARN, "takeout", "not configured (optional fallback)")
        return
    try:
        config = C.read_json(C.TAKEOUT_PATH)
        history = config.get("watch_history")
    except (ValueError, OSError):
        line(BAD, "takeout", "{0} is not readable JSON".format(C.TAKEOUT_PATH))
        return
    if not history or not os.path.isfile(history):
        line(WARN, "takeout", "watch_history path does not exist")
        return
    line(OK, "takeout", history)


def whisper_target_dir():
    """Where to tell the user to put a model: an existing search directory if
    there is one, otherwise the first entry the search would look in."""
    for directory in C.WHISPER_MODEL_DIRS:
        if os.path.isdir(os.path.expanduser(directory)):
            return directory
    return C.WHISPER_MODEL_DIRS[0]


def check_whisper():
    cli = C.whisper_cmd()
    model = C.whisper_model()
    if not cli:
        line(WARN, "whisper", "not installed — videos with no captions fall back to metadata")
        print("         brew install whisper.cpp")
        return
    if not model:
        target = os.path.expanduser(whisper_target_dir())
        line(WARN, "whisper", "whisper-cli found, but no usable model (a real one is 75MB+)")
        print("         searched: {0}".format(", ".join(C.WHISPER_MODEL_DIRS)))
        print("         fetch one:")
        print("         mkdir -p {0}".format(target))
        print("         curl -L -o {0}/ggml-small.en.bin \\".format(target))
        print("           https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin")
        return
    size_mb = os.path.getsize(model) / 1048576
    line(OK, "whisper", "{0} ({1:.0f} MB)".format(model, size_mb))


def check_output_dirs():
    missing = []
    for path in (C.VIDEOS_DIR, C.THUMBS_DIR):
        if os.path.isdir(path):
            line(OK, os.path.basename(path), path)
        else:
            os.makedirs(path, exist_ok=True)
            line(OK, os.path.basename(path), "created {0}".format(path))
            missing.append(path)
    return not missing


def main():
    print("videos skill setup\n")

    ytdlp_ok = check_ytdlp()
    check_ffmpeg()
    check_whisper()
    cookies = check_cookies()
    check_takeout()
    check_output_dirs()

    print()
    if not ytdlp_ok:
        print("NOT READY — yt-dlp is the one hard requirement.")
        return 1
    if cookies is None and not os.path.isfile(C.TAKEOUT_PATH):
        print("NOT READY — no way to discover what you watched.")
        print("  Export a cookies.txt, or point takeout.json at a Takeout export.")
        print("  Both are covered in references/setup.md.")
        print("  Passing explicit --ids to fetch_video.py bypasses discovery entirely.")
        return 1

    print("READY — run candidates.py next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())