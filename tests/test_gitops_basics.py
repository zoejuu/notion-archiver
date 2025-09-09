import os
import subprocess
from pathlib import Path
import tempfile

import notion_archiver.gitops as g
import notion_archiver.config as c

def test_identity_and_branch():
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        subprocess.run(["git", "init"], cwd=repo, check=True)

        git_branch = c.get_git_branch()
        git_user, git_email = c.get_git_identity()
        shoud_auto_push = c.should_auto_push()

        g.ensure_git_identity(repo)
        g.ensure_branch(repo, git_branch)

        # validation
        name = subprocess.check_output(["git", "config", "user.name"], cwd=repo, text=True).strip()
        email = subprocess.check_output(["git", "config", "user.email"], cwd=repo, text=True).strip()
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=repo, text=True).strip()

        assert name == git_user
        assert email == git_email
        assert branch == git_branch

        print(f"branch: {branch} | username: {name} | email: {email}")

def test_run_git_command():
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        subprocess.run(["git", "init"], cwd=repo, check=True)

        result = g.run("git status --porcelain", repo)
        assert result.returncode == 0
        assert isinstance(result.stdout, str)

        print(f"\nTarget repo: {repo}")
        print(f"{result}")