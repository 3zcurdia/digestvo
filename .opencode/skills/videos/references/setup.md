# One-time setup

Two things, both yours to do. Nothing else is needed — no Google Cloud project,
no API key, no OAuth client, no consent screen, no quota.

`scripts/check_setup.py` reports what is present and names the command that
fixes what is not.

## 1. yt-dlp

```sh
brew install yt-dlp
```

Homebrew and other third-party installs disable `yt-dlp -U`, so the update path
is `brew upgrade yt-dlp`. This matters more than it sounds: YouTube changes its
player and signing often enough that a stale build quietly starts returning
**no subtitles on videos that worked last week**. When a video has no transcript
and you know it used to, upgrade before anything else.

If yt-dlp is ever missing entirely the scripts fall back to
`uv tool run yt-dlp`, which needs no install. Homebrew is the intended path.

## 2. A cookies file

This is what lets the skill read your watch history and Watch Later. YouTube's
own Data API refuses both outright — it answers `403 watchHistoryNotAccessible`
— so the only way to see your real history is to act as a signed-in browser.

**Why not `--cookies-from-browser`:** it does not work on your machine. Chrome
has used Application-Bound Encryption since 2024 and yt-dlp cannot decrypt it;
its own maintainer says the option is broken for current Chromium browsers.
Firefox is the browser it works with, and you do not have one installed.

So: install a cookies-export extension in Chrome — the "Get cookies.txt
LOCALLY" family is the usual one, or any extension that writes Netscape format.

Then, **while sitting on `youtube.com`**:

1. Run the extension and export.
2. Save the file to `~/.config/digestvo/cookies.txt`.
3. `mkdir -p ~/.config/digestvo && chmod 600 ~/.config/digestvo/cookies.txt`

Two traps worth knowing:

- Extensions scoped to "the current tab" will export a header with no cookies if
  the active tab is not youtube.com. That is the usual reason for "the file
  exists and yt-dlp says zero cookies".
- If your export is JSON rather than plain text, it is the wrong extension —
  yt-dlp reads Netscape format only.

**Re-export when the session expires.** A cookies file is a session with a
lifetime, and `check_setup.py` warns when it has gone stale.

### What a cookies.txt is

A live signed-in session in plain text. Anyone who reads it is logged in as you,
with no password and no second factor — that is why it lives outside the repo at
mode 600, and why it must never be committed. It is also why the scripts never
print it and never echo its contents into an error.

Downloader-shaped sessions occasionally get flagged by sites, so if you would
rather not risk your primary account, use the Takeout route below instead.

## Optional: a Takeout export as fallback

Takeout is Google's official data export and needs no extension. It is slower to
produce (a few minutes to hours) and always behind, but it carries the exact
time you watched each video, which the cookies route cannot.

1. Go to <https://takeout.google.com>.
2. Deselect everything, then select only **YouTube and YouTube Music**.
3. Inside it, keep only **History**.
4. Choose **JSON** for the format, not HTML.
5. Export, download, unzip.
6. Write the path to the file:

   ```sh
   mkdir -p ~/.config/digestvo
   printf '{"watch_history": "%s"}\n' \
     "/Users/you/Downloads/Takeout/YouTube and YouTube Music/history/watch-history.json" \
     > ~/.config/digestvo/takeout.json
   chmod 600 ~/.config/digestvo/takeout.json
   ```

With both present, `candidates.py` discovers through the cookies and takes the
watch dates from Takeout, so the dates on the pages are exact. With only
Takeout, it reads that. With neither, pass ids directly:

```sh
python3 .opencode/skills/videos/scripts/fetch_video.py --ids ZHjH9qSiJzQ
```

## Optional: local transcription

A video with no captions at all is transcribed locally rather than dropped.
`whisper-cli` and a model are already on this machine —
`~/.cache/whisper-cpp/ggml-base.bin`, the multilingual base model — so this path
works out of the box and `check_setup.py` will confirm it.

`ggml-base` is the smallest model that produces usable prose. It is noticeably
sharper on English with the `.en` build, and `small.en` is better still. Both are
optional upgrades:

```sh
mkdir -p ~/.cache/whisper-cpp
curl -L -o ~/.cache/whisper-cpp/ggml-small.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
```

Drop the file in `~/.cache/whisper-cpp/` and it is picked up on the next run —
the scripts search the cache directories whisper.cpp has used across builds
rather than assuming one name, and take the largest model they find.

This path downloads the audio first, which for a two-hour talk is ~150MB. The
audio is deleted immediately after transcription. Pass `--no-transcribe` to
`fetch_video.py` to skip it.

## Privacy

The skill is read-only against YouTube. It never passes `--mark-watched` (which
yt-dlp fires even under `--simulate`), never inserts into or deletes from a
playlist, and never modifies a video. Thumbnails are downloaded into
`src/images/videos/` and committed rather than hotlinked, so the published page
makes no third-party request at all.