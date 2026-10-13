#!/usr/bin/env python3
"""Stage everything, commit, and push to main. That is the whole deploy.

Usage:
    publish.py "Add 2026-10-13 digest"
    publish.py --dry-run "Copy fix"

`git add -A` respects .gitignore, so build output, caches and run files
never enter the commit. The push triggers .github/workflows/deploy.yml,
which builds the site on GitHub Actions; nothing is built locally.

The script refuses to run off main, with unresolved conflicts, or on an
empty message. It never pulls, rebases, or force-pushes.
"""

import argparse
import subprocess
import sys

BRANCH = "main"
REMOTE = "origin"


def git(*args):
    """Run git quietly; never raises on a non-zero exit."""
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def must_git(*args):
    res = git(*args)
    if res.returncode != 0:
        detail = (res.stderr or res.stdout).strip()
        fail("`git {0}` failed:\n{1}".format(" ".join(args), detail))
    return res


def staged_files():
    out = must_git("diff", "--cached", "--name-status").stdout
    return [line for line in out.splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("message", nargs="?", help="commit message")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would be committed, touch nothing")
    args = parser.parse_args()

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        fail("not inside a git work tree; run from the repo root")

    branch = git("branch", "--show-current").stdout.strip()
    if branch != BRANCH:
        fail("on branch `{0}`, not `{1}`. Only a push to {1} deploys; "
             "switch branches yourself if that is what you want.".format(
                 branch or "(detached HEAD)", BRANCH))

    if git("ls-files", "--unmerged").stdout.strip():
        fail("there are unresolved merge conflicts; resolve them before publishing")

    if args.dry_run:
        status = git("status", "--porcelain").stdout.splitlines()
        print("REPORT")
        print("DRY RUN — nothing was staged, committed, or pushed.")
        if not status:
            print("NOTHING TO COMMIT — the working tree is clean.")
            return
        print("Would commit {0} path(s) on {1}:".format(len(status), BRANCH))
        for line in status:
            print("- " + line)
        return

    message = (args.message or "").strip()
    if not message:
        fail("a commit message is required, e.g. "
             "`publish.py \"Add 2026-10-13 digest\"`")

    must_git("add", "-A")
    files = staged_files()
    if not files:
        print("REPORT")
        print("NOTHING TO COMMIT — every change is ignored by .gitignore; "
              "nothing was staged, committed, or pushed.")
        return

    must_git("commit", "-m", message)
    sha = git("rev-parse", "--short", "HEAD").stdout.strip()

    push = git("push", REMOTE, BRANCH)
    if push.returncode != 0:
        detail = (push.stderr or push.stdout).strip()
        fail("push to {0}/{1} failed:\n{2}\n"
             "The commit {3} exists locally but was not published.".format(
                 REMOTE, BRANCH, detail, sha))

    print("REPORT")
    print("Committed {0} on {1}: {2}".format(sha, BRANCH, message))
    print("Pushed to {0}/{1}; GitHub Actions now builds and deploys the site.".format(
        REMOTE, BRANCH))
    print("Files changed ({0}):".format(len(files)))
    for line in files:
        print("- " + line)


if __name__ == "__main__":
    main()
