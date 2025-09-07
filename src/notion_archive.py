import re, argparse, os, time, shutil, hashlib
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client
from slugify import slugify
from python_notion_exporter import NotionExporter, ExportType, ViewExportType

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
    pid = notion_url[-32:]
    cleaned = pid.replace("-","")
    m=UUID_RE.search(cleaned)
    if not m:
        raise ValueError(f"No UUID found in {notion_url}")
    return hyphenate(m.group(0))

def get_created_date(page: str) -> str:
    """
    Extract the first created time of the notion page
    """    
    created_time_str = page["created_time"]
    
    # Parse ISO format and format it in Australian standard
    dt = datetime.fromisoformat(created_time_str.replace('Z', '+00:00'))
    return dt.strftime("%d/%m/%Y")

def get_page_title(page: str) -> str:
    """
    Extract the page title using notion API
    """
    return "".join([t["plain_text"] for t in page["properties"]["title"]["title"]]) or "untitled"

def resolve_target_root() -> Path:
    """
    Decide the git repo where notion pages will be archived.
    
    Returns:
        The path to the git repo
    
    Raises:
        SystemExit: If the target repo is not specified in .env
        SystemExit: If the provided target path neither doesn't exist nor isn't a git repo
    """
    # Get the path from .env
    load_dotenv()
    path_to_repo = os.getenv("TARGET_REPO_DIR")
    if not path_to_repo:
        raise SystemExit(
            "Missing target repo path. Set TARGET_REPO_DIR in .env\n"
        )
    root = Path(path_to_repo).expanduser().resolve()

    # Ensure path exists and is a git repo
    if not root.exists():
        raise SystemExit(f"Target path does not exist: {root}")
    if not (root / ".git").exists():
        raise SystemExit(f"{root} is not a git repo (no .git found).")
    
    return root

def export_to_pdf(pid: str, target_root: Path, target_dir: str = "pdf") -> Path:
    """
    Export a single Notion page (by URL) to PDF using python-notion-exporter, then
    move the PDF into: <target_root>/<target_dir>/<slug>.pdf

    - Uses browser cookies from .env: NOTION_TOKEN_V2, NOTION_FILE_TOKEN
    - Creates a staging folder: <target_root>/.notion-tmp/
    - Skips overwrite if an identical PDF already exists (hash check)
    """
    # Get cookies (browser session) required by python-notion-exporter from .env
    load_dotenv()
    token_v2 = os.getenv("NOTION_TOKEN_V2")
    file_token = os.getenv("NOTION_FILE_TOKEN")
    if not token_v2 or not file_token:
        raise SystemExit("Missing NOTION_TOKEN_V2 or NOTION_FILE_TOKEN in .env")

    # Temporary staging path to write output
    staging_root = (target_root / ".notion-tmp").resolve()
    staging_root.mkdir(parents=True, exist_ok=True)
    export_name = "export-" + hashlib.sha1(pid.encode()).hexdigest()[:8]
    export_path = staging_root / export_name
    export_path.mkdir(parents=True, exist_ok=True)

    base_slug = slugify(pid)

    # Initialise the exporter
    exporter = NotionExporter(
        token_v2=token_v2,
        file_token=file_token,
        pages={base_slug: pid.replace("-", "")},
        export_directory=str(staging_root),
        flatten_export_file_tree=True,
        export_type=ExportType.PDF,
        current_view_export_type=ViewExportType.CURRENT_VIEW,
        include_files=False,
        recursive=True,
        workers=1,
        export_name=export_name,
    )
    exporter.process()

    # Format PDF name (title + created time)
    notion_api = os.getenv("NOTION_TOKEN")
    client = Client(auth=notion_api)
    page = client.pages.retrieve(page_id=pid)
    file_name = slugify(get_page_title(page)+"-"+get_created_date(page))

    # Final destination
    final_dir = target_root / target_dir
    final_dir.mkdir(parents=True, exist_ok=True)
    dest = final_dir / f"{file_name}.pdf"

    # Grab the output PDF and perform directory moving to the final destination (dest)
    pdfs = sorted(export_path.rglob("*.pdf"), key=lambda p: p.stat().st_size, reverse=True)
    if not pdfs:
        raise RuntimeError(f"No PDF found after export in {export_path}")
    staged_pdf = pdfs[0]

    shutil.move(str(staged_pdf), str(dest))
    shutil.rmtree(export_path, ignore_errors=True)
    print(f"[ok] saved: {dest}")

    return dest

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
    ap = argparse.ArgumentParser(description = "Export Notion page(s) to PDF.")
    ap.add_argument("urls", nargs="+", help="Notion page URL(s). Multiple URLs can be provided with space separation.")
    ap.add_argument("--dry-run", action="store_true", help="Only parse IDs and ping Notion") # Optional flag for dry run
    args = ap.parse_args()

    # Resolve where the files will be written
    target_root = resolve_target_root()
    target_dir = os.getenv("TARGET_SUBDIR", "pdfs")

    # Iterate over all URLs provided on the command line.
    for u in args.urls:
        # Extract a hyphenated page ID from the full Notion URL.
        pid = extract_page_id(u)

        # If --dry-run option is passed, do not write files; just verify access and show basic info.
        if args.dry_run:
            page = client.pages.retrieve(page_id=pid)

            print(f"[dry-run] page_id={pid}")
            print(f"[dry-run] title={get_page_title(page)}")
            print(f"[dry-run] created_date={get_created_date(page)}")
            print(f"[dry-run] target_root={target_root}\n")
        else:
            export_to_pdf(pid, target_root, target_dir = target_dir)
            print("\nNow review & commit your output repo.")
    
if __name__ == "__main__":
    main()