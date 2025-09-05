import re, argparse, os
from dotenv import load_dotenv
from notion_client import Client

# Compile a regex that finds a 32-character hexadecimal string (the raw Notion page ID without dashes).
UUID_RE = re.compile(r"[0-9a-f]{32}", re.IGNORECASE)

def hyphenate(uuid32: str) -> str:
    """
    Convert a 32-character hex Notion page ID into the standard hyphenated UUID form.

    Example:
        Input:  '0123456789abcdef0123456789abcdef'
        Output: '01234567-89ab-cdef-0123-456789abcdef'

    Args:
        uuid32: A 32-char hex string (no dashes).

    Returns:
        A hyphenated UUID string in 8-4-4-4-12 format.
    """
    s = uuid32.lower()
    return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:32]}"

def extract_page_id(notion_url: str) -> str:
    """
    Extract the Notion page ID from a Notion URL and return it in hyphenated UUID form.

    This accepts various URL shapes. It searches the entire string for a 32-hex token
    (with or without dashes in the original URL) and returns the hyphenated version.

    Args:
        notion_url: The full Notion URL copied from the browser.

    Returns:
        The hyphenated page ID string.

    Raises:
        ValueError: If no 32-hex page ID is found in the input URL.
    """
    cleaned = notion_url.replace("-","")
    m=UUID_RE.search(cleaned)
    if not m:
        raise ValueError(f"No UUID found in {notion_url}")
    return hyphenate(m.group(0))

def main():
    """
    Entry point for the CLI.
    - Loads configuration from .env (NOTION_TOKEN).
    - Initialises the Notion API client.
    - Parses command-line arguments (one or more Notion URLs; --dry-run flag).
    - For each URL:
        * Extracts the page ID.
        * If --dry-run: performs a light API call to verify access and prints the title.
        * Else: prints a TODO (to be implemented in later milestones).
    """

    # Get the NOTION_TOKEN from .env
    load_dotenv()
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise SystemExit("Missing NOTION_TOKEN in .env")

    # Initialise the Notion API client
    client = Client(auth=token)

    # Set up the argument parser with a user-friendly description
    ap = argparse.ArgumentParser(
        description = "Archive a Notion page into Markdown."
    )
    ap.add_argument("urls", nargs="+", help="Notion page URL(s). Multiple URLs can be provided with space separation.")
    ap.add_argument("--dry-run", action="store_true", help="Only parse IDs and ping Notion") # Optional flag for dry run
    args = ap.parse_args()

    # Iterate over all URLs provided on the command line.
    for u in args.urls:
        # Extract a hyphenated page ID from the full Notion URL.
        pid = extract_page_id(u)

        # If --dry-run option is passed, do not write files; just verify access and show basic info.
        if args.dry_run:
            print(f"[dry-run] page_id={pid}")
            page = client.pages.retrieve(page_id=pid)

            title = "".join([t["plain_text"] for t in page["properties"]["title"]["title"]]) or "untitled"
            print(f"[dry-run] title={title}")
        else:
            # Placeholder for the real work to be added in future milestones
            print(f"TODO: convert {pid} -> Markdown")
    
if __name__ == "__main__":
    main()