import os
from dotenv import load_dotenv
from notion_client import Client
from pathlib import Path

load_dotenv()
token = os.getenv("NOTION_TOKEN")
assert token, "NOTION_TOKEN missing in .env"

client = Client(auth=token)
print("OK: Notion client created. Your token length =", len(token))

root = os.getenv("TARGET_REPO_DIR")
assert root, "TARGET_REPO_DIR missing in .env"

# Check if directory exists
root_path = Path(root)
if not root_path.exists():
    raise SystemExit(f"TARGET_REPO_DIR does not exist: {root}")

if not root_path.is_dir():
    raise SystemExit(f"TARGET_REPO_DIR is not a directory: {root}")

print(f"OK: Target directory exists: {root}")

# List directory contents
print(f"\nDirectory contents of {root}:")
try:
    for item in sorted(root_path.iterdir()):
        item_type = "DIR" if item.is_dir() else "FILE"
        print(f"  {item_type}: {item.name}")
except PermissionError:
    print("  Error: Permission denied to list directory contents")