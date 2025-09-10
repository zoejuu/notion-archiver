# Notion Archiver

A Python tool that automatically exports Notion pages to PDF files and commits them to a Git repository. Perfect for creating automated backups of your Notion knowledge base.

## Features

- 📄 **Export Notion pages to PDF** using the official Notion API
- 🔄 **Automatic Git integration** with commit and optional push
- 🧪 **Dry-run mode** to test without making changes
- 🔀 **Batch processing** of multiple URLs
- ⚙️ **Configurable** via environment variables

## Installation

### Prerequisites

- Python 3.8 or higher
- Git repository for storing exported PDFs
- Notion integration token and export tokens

### 1. Clone the repository

```bash
git clone https://github.com/zoejuu/notion-archiver.git
cd notion-archiver
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root, referring to [`.env.example`](.env.example).

Example .env:

```env
# Your official Notion API token
NOTION_TOKEN=your_notion_integration_token_here

# Notion session cookies from your browser
NOTION_TOKEN_V2=your_notion_token_v2_here
NOTION_FILE_TOKEN=your_notion_file_token_here

# The target git repository to archive notion pages
TARGET_REPO_DIR=/absolute/path/to/study-archive

# Optional: A path to the directory where the exported files will be saved within the repo
TARGET_SUBDIR=notes/2025/pdfs

# Git
TARGET_BRANCH=
GIT_USER_NAME=
GIT_USER_EMAIL=
```

## Getting Notion Tokens

### 1. Integration Token (`NOTION_TOKEN`)
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Share your pages with this integration

Detailed step-by-step guide is available [here](https://developers.notion.com/docs/create-a-notion-integration).

### 2. Export Tokens (`NOTION_TOKEN_V2`, `NOTION_FILE_TOKEN`)
1. Open your Notion page in a browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Find and copy:
   - `token_v2` → `NOTION_TOKEN_V2`
   - `file_token` → `NOTION_FILE_TOKEN`

## Usage

### Basic Usage

```bash
# Export a single page
python -m src.notion_archiver "https://www.notion.so/your-page-url"

# Export multiple pages
python -m src.notion_archiver "url1" "url2" "url3"

# Dry run (test without exporting)
python -m src.notion_archiver "https://www.notion.so/your-page-url" --dry-run

# Export and auto-push to remote
python -m src.notion_archiver "https://www.notion.so/your-page-url" -p
```

### Command Line Options

- `urls`: One or more Notion page URLs (required)
- `--dry-run`: Test mode - verify access without exporting
- `-p, --push`: Enable automatic push to remote repository

### Examples

```bash
# Test access to a page
python -m src.notion_archiver "https://www.notion.so/My-Page-123abc" --dry-run

# Export and commit (no push)
python -m src.notion_archiver "https://www.notion.so/My-Page-123abc"

# Export, commit, and push
python -m src.notion_archiver "https://www.notion.so/My-Page-123abc" --push

# Batch export multiple pages
python -m src.notion_archiver \
  "https://www.notion.so/Page1-123abc" \
  "https://www.notion.so/Page2-456def" \
  "https://www.notion.so/Page3-789ghi"
```

## Project Structure
```
notion-archiver/
├── src/notion_archiver/ # Source codes
├── tests/ # Test files for internal functional debugging
├── requirements.txt # Python dependencies
├── pytest.ini # Test configuration
└── README.md # This file
```
### Code Structure

- **`main.py`**: CLI interface and main workflow
- **`config.py`**: Environment variable management
- **`utils.py`**: URL parsing and utility functions
- **`notion.py`**: Notion API interactions
- **`export.py`**: PDF export using python-notion-exporter
- **`gitops.py`**: Git operations (commit, push, branch management)

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NOTION_TOKEN` | ✅ | - | Notion integration token |
| `NOTION_TOKEN_V2` | ✅ | - | Notion token v2 for exports |
| `NOTION_FILE_TOKEN` | ✅ | - | Notion file token for exports |
| `TARGET_REPO_DIR` | ✅ | - | Path to Git repository |
| `TARGET_SUBDIR` | ❌ | `pdfs` | Subdirectory for PDFs |
| `TARGET_BRANCH` | ❌ | `main` | Git branch name |
| `GIT_USER_NAME` | ❌ | `notion-archiver` | Git commit author name |
| `GIT_USER_EMAIL` | ❌ | `notion-archiver@example.com` | Git commit author email |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request ;)

## License

This project is licensed under the MIT License.

## Author

**Hayeon Ju** - [GitHub](https://github.com/zoejuu)


## Changelog

### v0.1.0
- Initial release
- Basic PDF export functionality
- Git integration with commit and push
- CLI interface with dry-run mode
- Environment-based configuration