from datetime import datetime
from notion_client import Client
from .config import get_notion_token

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

def get_page_info(pid: str) -> tuple[str, str]:
    """Get page title and created time"""
    client = Client(auth=get_notion_token())
    page = client.pages.retrieve(page_id=pid)
    return get_page_title(page), get_created_date(page)