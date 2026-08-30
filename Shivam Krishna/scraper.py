from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_google_search(query="Selenium WebDriver"):
    """
    Scrapes Google search results for a given query.
    """
    # Set up the driver (using Chrome in this example)
    # NOTE: You need to download the correct ChromeDriver from https://sites.google.com/chromium.org/driver/
    # and either place it in your system PATH or specify its path explicitly.
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

    try:
        # Navigate to Google
        driver.get("https://www.google.com")

        # Find the search box, enter the query, and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        # Optional: Add a small delay to ensure all content is loaded
        time.sleep(2)

        # Find all the search result elements
        # This selector might change; inspect the Google page to update it if needed.
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")

        scraped_data = []

        for result in results:
            try:
                # Extract the title (link text)
                title_element = result.find_element(By.CSS_SELECTOR, "h3")
                title = title_element.text

                # Extract the URL (href attribute)
                link_element = result.find_element(By.CSS_SELECTOR, "a")
                url = link_element.get_attribute("href")

                # Extract the snippet/description
                snippet_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                snippet = snippet_element.text

                # Only add if we have a title and URL
                if title and url:
                    scraped_data.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })

            except Exception as e:
                # If an error occurs on a single result, skip it and continue
                print(f"Error extracting one result: {e}")
                continue

        # Print the results to the console
        for i, data in enumerate(scraped_data, 1):
            print(f"Result {i}:")
            print(f"  Title: {data['title']}")
            print(f"  URL: {data['url']}")
            print(f"  Snippet: {data['snippet']}\n")

        # (Optional) Save results to a CSV file
        with open('google_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'url', 'snippet']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(scraped_data)

        print(f"Successfully scraped {len(scraped_data)} results.")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    finally:
        # Always close the browser
        driver.quit()

if __name__ == "__main__":
    # You can change the search query here
    scrape_google_search("Python Selenium Web Scraping")