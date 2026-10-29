#!/usr/bin/env python3
"""Wait for the GitHub Actions deploy of a commit and report the outcome.

Usage:
    watch_deploy.py [--commit SHA] [--workflow deploy.yml] [--timeout 900]

Finds the workflow run triggered by `--commit` (default: HEAD), waits until it
completes, and prints a REPORT block. The site is only live once this reports
success, which is why the publish skill runs it before Telegram.

Exit codes: 0 the deploy succeeded; 1 it failed or was cancelled; 2 no run
appeared or the wait timed out. The script never touches git and never
retries a deploy; it only reads run state through the `gh` CLI.
"""

import argparse
import json
import subprocess
import sys
import time

FIND_ATTEMPTS = 10   # a run takes a few seconds to appear after a push
FIND_INTERVAL = 6    # seconds between attempts while it is being created
POLL_INTERVAL = 15   # seconds between status polls once it exists


def gh(*args):
    return subprocess.run(["gh"] + list(args), capture_output=True, text=True)


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def run_list(commit, workflow):
    res = gh("run", "list", "--commit", commit, "--workflow", workflow,
             "--json", "databaseId,status,conclusion,url")
    if res.returncode != 0:
        fail("`gh run list` failed:\n" + (res.stderr or res.stdout).strip())
    try:
        return json.loads(res.stdout or "[]")
    except json.JSONDecodeError:
        fail("`gh run list` returned unparseable output:\n" + res.stdout.strip())


def run_view(run_id):
    res = gh("run", "view", str(run_id), "--json", "status,conclusion,url")
    if res.returncode != 0:
        fail("`gh run view {0}` failed:\n{1}".format(
            run_id, (res.stderr or res.stdout).strip()))
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        fail("`gh run view` returned unparseable output:\n" + res.stdout.strip())


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--commit", default=None,
                        help="commit SHA to watch (default: HEAD)")
    parser.add_argument("--workflow", default="deploy.yml",
                        help="workflow file name (default: deploy.yml)")
    parser.add_argument("--timeout", type=int, default=900,
                        help="max seconds to wait (default: 900)")
    args = parser.parse_args()

    commit = args.commit
    if not commit:
        res = subprocess.run(["git", "rev-parse", "HEAD"],
                             capture_output=True, text=True)
        if res.returncode != 0:
            fail("not inside a git work tree; run from the repo root")
        commit = res.stdout.strip()

    deadline = time.time() + args.timeout

    run = None
    for _ in range(FIND_ATTEMPTS):
        runs = run_list(commit, args.workflow)
        if runs:
            run = runs[0]
            break
        if time.time() + FIND_INTERVAL > deadline:
            break
        time.sleep(FIND_INTERVAL)

    if run is None:
        print("REPORT")
        print("NO RUN - no `{0}` run found for {1} within {2}s.".format(
            args.workflow, commit[:12], args.timeout))
        sys.exit(2)

    run_id = run["databaseId"]
    while run.get("status") != "completed":
        if time.time() >= deadline:
            print("REPORT")
            print("TIMEOUT - run {0} is still {1} after {2}s: {3}".format(
                run_id, run.get("status"), args.timeout, run.get("url", "")))
            sys.exit(2)
        time.sleep(POLL_INTERVAL)
        run = run_view(run_id)

    conclusion = run.get("conclusion") or "(none)"
    print("REPORT")
    print("Run {0} ({1}): {2}".format(run_id, args.workflow, conclusion))
    print(run.get("url", ""))
    if conclusion == "success":
        return
    sys.exit(1)


if __name__ == "__main__":
    main()
