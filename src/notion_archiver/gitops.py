import os
import subprocess
from pathlib import Path
from .config import get_git_identity, get_git_branch, should_auto_push

def run(cmd: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run git command and return result."""
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True, shell=True)

def ensure_git_identity(cwd: Path):
    """Ensure git user identity is set."""
    try:
        run("git config user.name", cwd)
        run("git config user.email", cwd)
    except subprocess.CalledProcessError:
        name, email = get_git_identity()
        run(f'git config user.name "{name}"', cwd)
        run(f'git config user.email "{email}"', cwd)

def ensure_branch(cwd: Path, branch: str):
    """Ensure target branch exists and is checked out."""
    try:
        run(f"git rev-parse --verify {branch}", cwd)
    except subprocess.CalledProcessError:
        run(f"git checkout -b {branch}", cwd)
        return
    run(f"git checkout {branch}", cwd)

def has_changes(cwd: Path) -> bool:
    """Check if there are uncommitted changes."""
    result = run("git status --porcelain", cwd)
    return bool(result.stdout.strip())

def stage_and_commit(cwd: Path, file_path: Path, message: str) -> bool:
    """Stage all changes and commit with message."""
    try:
        rel = file_path.resolve().relative_to(cwd.resolve())
    except ValueError:
        rel = file_path.resolve()

    run(f'git add "{rel}"', cwd)

    if not has_changes(cwd):
        print("[git] no changes to commit")
        return False
    
    run(f'git commit -m "{message}"', cwd)
    print(f"[git] committed: {message}")
    return True

def auto_commit_pdf(target_root: Path, file_path: Path, commit_msg: str, branch: str = None):
    """Automatically commit PDF changes to git."""
    if branch is None:
        branch = get_git_branch()
    
    ensure_git_identity(target_root)
    ensure_branch(target_root, branch)
    
    stage_and_commit(target_root, file_path, commit_msg)

