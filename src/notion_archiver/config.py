import os
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load configuration from .env file."""
    load_dotenv()

def get_notion_token() -> str:
    """Get Notion API token from environment."""
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise SystemExit("Missing NOTION_TOKEN in .env")
    return token

def get_notion_export_tokens() -> tuple[str, str]:
    """Get Notion export tokens from environment."""
    token_v2 = os.getenv("NOTION_TOKEN_V2")
    file_token = os.getenv("NOTION_FILE_TOKEN")
    if not token_v2 or not file_token:
        raise SystemExit("Missing NOTION_TOKEN_V2 or NOTION_FILE_TOKEN in .env")
    return token_v2, file_token

def get_target_repo() -> Path:
    """Get target repository path from environment."""
    path = os.getenv("TARGET_REPO_DIR")
    if not path:
        raise SystemExit("Missing TARGET_REPO_DIR in .env")
    
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Target path does not exist: {root}")
    if not (root / ".git").exists():
        raise SystemExit(f"{root} is not a git repo (no .git found)")
    
    return root

def get_target_subdir() -> str:
    """Get target subdirectory for PDFs."""
    return os.getenv("TARGET_SUBDIR", "pdfs")

def get_git_branch() -> str:
    """Get target git branch."""
    return os.getenv("TARGET_BRANCH", "main")

def get_git_identity() -> tuple[str, str]:
    """Get git user name and email."""
    name = os.getenv("GIT_USER_NAME", "notion-archiver")
    email = os.getenv("GIT_USER_EMAIL", "notion-archiver@example.com")
    return name, email