import argparse
from .config import load_config, get_target_repo
from .utils import extract_page_id
from .notion import get_page_info
from .export import export_to_pdf

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
    load_config()

    # Set up the argument parser with a user-friendly description
    ap = argparse.ArgumentParser(description = "Export Notion page(s) to PDF.")
    ap.add_argument("urls", nargs="+", help="Notion page URL(s). Multiple URLs can be provided with space separation.")
    ap.add_argument("--dry-run", action="store_true", help="basic API call only to verify access to the provided notion page and speficied repository") # Optional flag for dry run
    args = ap.parse_args()

    # Iterate over all URLs provided on the command line.
    for u in args.urls:
        # Extract a hyphenated page ID from the full Notion URL.
        pid = extract_page_id(u)

        # If --dry-run option is passed, do not write files; just verify access and show basic info.
        if args.dry_run:
            title, created_date = get_page_info(pid)
            print(f"[dry-run] page_id={pid}")
            print(f"[dry-run] title={title}")
            print(f"[dry-run] created_date={created_date}")
            print(f"[dry-run] target_root={get_target_repo()}\n")
        else:
            export_to_pdf(pid)
    
    print("\nNow review & commit your output repo.")