import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
token = os.getenv("NOTION_TOKEN")
assert token, "NOTION_TOKEN missing in .env"

client = Client(auth=token)
print("OK: Notion client created. Your token length =", len(token))