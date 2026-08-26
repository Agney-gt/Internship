# Google Search Scraper

Selenium scraper that opens Google, collects organic listings, and writes them to a CSV file.

**Loom walkthrough:** [https://www.loom.com/share/ae4ffef8f1ed47cda6f99bd30499a138](https://www.loom.com/share/ae4ffef8f1ed47cda6f99bd30499a138)

The video covers the code and the full workflow: Selenium opens Google search → scrapes listings → generates CSV → CSV is verified.

## Files

- `google_scraper.py` — scraper
- `requirements.txt` — Python dependencies
- `google_search_results.csv` — sample output (`rank`, `title`, `link`, `snippet`)

## Requirements

- Python 3.10+
- Google Chrome
- Packages in `requirements.txt` (`selenium`, `webdriver-manager`)

ChromeDriver is installed automatically via `webdriver-manager`.

## Setup

```bash
cd Darshan_S
pip install -r requirements.txt
```

## Usage

```bash
python google_scraper.py
```

Enter a search query, or press Enter to use the default: `Selenium Python tutorial`.

The script launches Chrome, searches Google, scrapes organic results (`div.tF2Cxc`), and saves them to `google_search_results.csv` in this folder.
