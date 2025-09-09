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

