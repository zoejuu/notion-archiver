# notion-archiver
Notion Archiver automates the archiving process of a specific notion page to a pre-determined github repository. When you paste a link of the notion page you want to archive in your github repo, this tool will automatically generate the markdown file of the page and prompt you to commit &amp; push the file to your repo.


## Dev Milestones & Tasks

### Milestone 0 — Bootstrap
- [ ] **Init repo structure**
  - **Goal:** Base folders & files.
  - **Test:** `git status` shows scaffold.
  - **Commit:** `chore: scaffold repo with base dirs and files`
- [ ] **Python env & dependencies**
  - **Goal:** `requirements.txt`, venv setup.
  - **Test:** `pip install -r requirements.txt` succeeds.
  - **Commit:** `chore: add python deps and venv instructions`
- [ ] **Secrets handling**
  - **Goal:** Load `NOTION_TOKEN` via `dotenv`.
  - **Test:** `python -c "import os;from dotenv import load_dotenv;load_dotenv();print(bool(os.getenv('NOTION_TOKEN')))"` → `True`.
  - **Commit:** `chore: add .env.example and dotenv loading`

---

### Milestone 1 — Minimal CLI
- [ ] **CLI skeleton**
  - **Goal:** `python tools/notion_archive.py <NotionURL>` with `argparse`.
  - **Test:** `--help` prints usage.
  - **Commit:** `feat(cli): add minimal CLI skeleton`
- [ ] **Extract Notion page ID from URL**
  - **Goal:** Parse 32-char hex and hyphenate (UUID format).
  - **Test:** Print extracted ID from a real Notion URL.
  - **Commit:** `feat(url): extract and hyphenate Notion page id`
- [ ] **Verify Notion API connectivity**
  - **Goal:** `pages.retrieve(page_id)` with clear 401/403/404 errors.
  - **Test:** Try with: missing token / not invited / wrong URL.
  - **Commit:** `feat(api): connect to Notion and retrieve page`

---

### Milestone 2 — Content Fetch
- [ ] **Fetch blocks (recursive + pagination)**
  - **Goal:** `blocks.children.list` to collect full tree; handle `has_more`.
  - **Test:** Count block types; deep pages return all children.
  - **Commit:** `feat(blocks): recursive fetch with pagination`
- [ ] **Dry-run inspection**
  - **Goal:** `--dry-run` to print a summary of block types/sizes.
  - **Test:** `python tools/notion_archive.py <URL> --dry-run`.
  - **Commit:** `feat(cli): add --dry-run for safe inspection`

---

### Milestone 3 — Markdown Rendering
- [ ] **Paragraphs & headings**
  - **Goal:** Render `paragraph`, `heading_1/2/3`.
  - **Test:** Simple page renders to temporary MD text.
  - **Commit:** `feat(md): render paragraph and headings`
- [ ] **Lists & to-dos**
  - **Goal:** `bulleted_list_item`, `numbered_list_item`, `to_do` (checked/unchecked).
  - **Test:** Nested lists and subtasks render correctly.
  - **Commit:** `feat(md): render lists and to-do items`
- [ ] **Inline annotations**
  - **Goal:** bold/italic/strikethrough/underline/code + links.
  - **Test:** Create a Notion page using all styles; check MD.
  - **Commit:** `feat(md): support inline annotations and links`
- [ ] **Quote & fenced code**
  - **Goal:** `quote`, `code(language)`.
  - **Test:** Multi-language code fences appear properly.
  - **Commit:** `feat(md): render quote and fenced code blocks`
- [ ] **Toggle & callout (nice-to-have)**
  - **Goal:** `toggle` → `<details>`, `callout` → note block.
  - **Test:** Expand/collapse content preserved.
  - **Commit:** `feat(md): support toggle and callout`

---

### Milestone 4 — Assets (Images / Files)
- [ ] **Download images/files**
  - **Goal:** Save to `assets/<pageId>/...`, link via relative paths.
  - **Test:** Images appear locally; MD references relative paths.
  - **Commit:** `feat(assets): download images/files and link relatively`
- [ ] **Handle URL expiry / retry**
  - **Goal:** Basic retries; graceful fallback on failure.
  - **Test:** Simulate expired URL; ensure no crash.
  - **Commit:** `fix(assets): add basic retry and graceful fallback`

---

### Milestone 5 — File Layout & Idempotency
- [ ] **YAML front-matter**
  - **Goal:** Include `title`, `notion_page`, `last_edited`, `url`.
  - **Test:** FM appears at the top of generated MD.
  - **Commit:** `feat(md): add YAML front-matter`
- [ ] **Output routing**
  - **Goal:** `notes/<year>/<slug>.md` + `assets/<pageId>/...`.
  - **Test:** Year/slug correctly computed from title/edited time.
  - **Commit:** `feat(fs): year/slug path routing`
- [ ] **Change detection (hash)**
  - **Goal:** Skip writing if no content change → clean `git status`.
  - **Test:** Run twice on same page; no diffs on second run.
  - **Commit:** `feat(idempotent): skip write on no content change`
- [ ] **Batch URLs**
  - **Goal:** Accept multiple URLs in one invocation.
  - **Test:** Pass 2–3 URLs at once; all rendered.
  - **Commit:** `feat(cli): accept multiple Notion URLs`

---

### Milestone 6 — UX & Docs
- [ ] **Error messages & logging**
  - **Goal:** Friendly messages for 401/403/404/429; progress logs.
  - **Test:** Exercise each failure mode; messages make sense.
  - **Commit:** `chore(log): improve human-readable errors and logs`
- [ ] **CLI flags**
  - **Goal:** `--out`, `--dry-run`, `--verbose`.
  - **Test:** Verify output redirection and verbosity levels.
  - **Commit:** `feat(cli): add --out/--verbose flags`
- [ ] **Helper scripts (optional)**
  - **Goal:** `.bat` (Windows) / `.command` (macOS) wrappers.
  - **Test:** Double-click runs the tool.
  - **Commit:** `chore: add platform helper scripts`
- [ ] **Documentation**
  - **Goal:** Expand this README (setup/usage/FAQ/limits).
  - **Test:** A new user can set up from README alone.
  - **Commit:** `docs: add setup and usage guide`

---
