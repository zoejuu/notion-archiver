import re
import hashlib

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

def create_short_hash(text: str, length: int = 8) -> str:
    """Create short hash from text."""
    return hashlib.sha1(text.encode()).hexdigest()[:length]