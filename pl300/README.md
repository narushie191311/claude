# PL-300 question bank (work in progress)

Scripts that collect PL-300 discussions from ExamTopics and build a question database.

1. `scripts/crawl_index.py OUT_DIR [START] [END]` – walk the public Microsoft discussion listing, collect PL-300 discussion URLs.
2. `scripts/fetch_discussions.py HTML_DIR LINKS.tsv ...` – download each discussion page.
3. `scripts/build_db.py HTML_DIR OUT_DIR [view_page.html ...]` – parse into `pl300.db` (SQLite), CSV, JSON.
