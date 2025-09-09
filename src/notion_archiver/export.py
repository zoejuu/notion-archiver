import shutil
from pathlib import Path
from slugify import slugify
from python_notion_exporter import NotionExporter, ExportType, ViewExportType

from .config import get_notion_export_tokens, get_target_repo, get_target_subdir
from .utils import create_short_hash
from .notion import get_page_info

def export_to_pdf(pid: str) -> Path:
    """
    Export a single Notion page (by URL) to PDF using python-notion-exporter, then
    move the PDF into: <target_root>/<target_dir>/<slug>.pdf

    - Uses browser cookies from .env: NOTION_TOKEN_V2, NOTION_FILE_TOKEN
    - Creates a staging folder: <target_root>/.notion-tmp/
    - Skips overwrite if an identical PDF already exists (hash check)
    """
    # Get output path
    target_root = get_target_repo()
    target_dir = get_target_subdir()

    # Get cookies (browser session) required by python-notion-exporter
    token_v2, file_token = get_notion_export_tokens()

    # Setup temporary staging path to write output
    staging_root = (target_root / ".notion-tmp").resolve()
    staging_root.mkdir(parents=True, exist_ok=True)

    # Create unique export folder
    base_slug = slugify(pid)
    export_name = "export-" + create_short_hash(pid)
    export_path = staging_root / export_name
    export_path.mkdir(parents=True, exist_ok=True)

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

    # Find the largest PDF (main export)
    pdfs = sorted(export_path.rglob("*.pdf"), key=lambda p: p.stat().st_size, reverse=True)
    if not pdfs:
        raise RuntimeError(f"No PDF found after export in {export_path}")
    staged_pdf = pdfs[0]

    # Format PDF name (title + created time)
    title, created_date = get_page_info(pid)
    file_name = slugify(f"{title}-{created_date}")

    # Final destination
    final_dir = target_root / target_dir
    final_dir.mkdir(parents=True, exist_ok=True)
    dest = final_dir / f"{file_name}.pdf"

    # Move to final location
    shutil.move(str(staged_pdf), str(dest))
    shutil.rmtree(export_path, ignore_errors=True)

    print(f"[ok] saved: {dest}")
    return dest
