"""Google Search Scraper using Selenium.

Opens Google, performs a search, scrapes organic result listings,
and writes the data to a CSV file.
"""

import csv
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

GOOGLE_URL = "https://www.google.com"
DEFAULT_QUERY = "Selenium Python tutorial"
OUTPUT_FILE = "google_search_results.csv"
CSV_COLUMNS = ("rank", "title", "link", "snippet")


def create_driver(headless: bool = False) -> webdriver.Chrome:
    """Create and return a configured Chrome WebDriver instance."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def perform_search(driver: webdriver.Chrome, query: str) -> None:
    """Navigate to Google and submit the search query."""
    driver.get(GOOGLE_URL)

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#search"))
    )


def extract_results(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Extract organic search result title, link, and snippet from the page."""
    results: list[dict[str, str]] = []
    result_blocks = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

    for index, block in enumerate(result_blocks, start=1):
        try:
            title = block.find_element(By.TAG_NAME, "h3").text.strip()
            link = block.find_element(By.TAG_NAME, "a").get_attribute("href") or ""
        except NoSuchElementException:
            continue

        if not title or not link:
            continue

        snippet = ""
        try:
            snippet = block.find_element(By.CSS_SELECTOR, "div.VwiC3b").text.strip()
        except NoSuchElementException:
            pass

        results.append(
            {
                "rank": str(index),
                "title": title,
                "link": link,
                "snippet": snippet,
            }
        )

    return results


def save_to_csv(results: list[dict[str, str]], output_path: Path) -> None:
    """Write scraped results to a CSV file."""
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(results)


def scrape_google(query: str, output_path: Path | None = None) -> list[dict[str, str]]:
    """Run the full scrape workflow and return extracted results."""
    output_path = output_path or Path(__file__).resolve().parent / OUTPUT_FILE
    driver = create_driver()

    try:
        print(f"Searching Google for: {query!r}")
        perform_search(driver, query)
        results = extract_results(driver)

        if not results:
            print("No results found. Google may have changed its layout or blocked the request.")
            return []

        save_to_csv(results, output_path)
        print(f"Saved {len(results)} results to {output_path}")
        return results
    finally:
        driver.quit()


def main() -> None:
    query = input("Enter a Google search query (press Enter for default): ").strip()
    if not query:
        query = DEFAULT_QUERY

    try:
        results = scrape_google(query)
    except TimeoutException:
        print("Timed out waiting for Google to load. Check your internet connection and try again.")
        sys.exit(1)
    except WebDriverException as error:
        print(f"Scraping failed: {error}")
        sys.exit(1)

    if results:
        print("\nPreview:")
        for row in results[:5]:
            print(f"{row['rank']}. {row['title']}")
            print(f"   {row['link']}")


if __name__ == "__main__":
    main()
