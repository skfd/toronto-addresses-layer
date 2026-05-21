"""Publish build/site/ to the orphan gh-pages branch (single commit, force-push).

The tile pyramid is tens of thousands of files. Keeping it on an orphan branch
that is recreated and force-pushed each build means the repo history never grows.
"""

import os
import shutil
import subprocess
from datetime import date

from src import config

WORKTREE = os.path.join(config.BUILD_DIR, ".gh-pages-wt")


def publish():
    """Force-push build/site/ as a single commit on the gh-pages branch."""
    if not os.path.isdir(config.SITE_DIR):
        raise RuntimeError(f"No site to publish: {config.SITE_DIR}. Run 'site' first.")

    # Remove any leftover worktree / local branch from a previous run.
    _git("worktree", "remove", "--force", WORKTREE, check=False)
    shutil.rmtree(WORKTREE, ignore_errors=True)
    _git("worktree", "prune")
    _git("branch", "-D", "gh-pages", check=False)

    _git("worktree", "add", "--detach", WORKTREE)
    try:
        # Orphan branch keeps the working tree/index from HEAD; clear it, then
        # drop in only the site contents.
        _git("checkout", "--orphan", "gh-pages", cwd=WORKTREE)
        _git("rm", "-rf", "--quiet", ".", cwd=WORKTREE, check=False)
        for name in os.listdir(config.SITE_DIR):
            src = os.path.join(config.SITE_DIR, name)
            dst = os.path.join(WORKTREE, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        _git("add", "-A", cwd=WORKTREE)
        _git("commit", "-m", f"site {date.today().isoformat()}", cwd=WORKTREE)
        _git("push", "--force", "origin", "gh-pages", cwd=WORKTREE)
        print("Published to the gh-pages branch.")
    finally:
        _git("worktree", "remove", "--force", WORKTREE, check=False)
        _git("worktree", "prune")


def _git(*args, cwd=None, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or config.PROJECT_DIR,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed (exit {result.returncode}):\n"
            f"{result.stderr.strip()}"
        )
    return result
