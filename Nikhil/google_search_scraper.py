import undetected_chromedriver as uc
# Overwrite the broken class destructor method to prevent the invalid handle popup on close
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import random

# Initialize the modified runtime binary architecture
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

# Boot the driver forcing matching compatibility with your Chrome 151 browser
driver = uc.Chrome(options=options, version_main=151)

try:
    # Direct access path execution
    driver.get("https://google.com")
    time.sleep(random.uniform(3.5, 5.0))  # Settle dynamic telemetry tracking

    # Locate query input
    search_box = driver.find_element(By.NAME, "q")
    
    # Staggered entry cadence matching natural keystroke profiles
    query = "Python Selenium tutorial"
    for char in query:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.18, 0.38))
        
    time.sleep(random.uniform(0.8, 1.4))
    search_box.send_keys(Keys.RETURN)

    # Allow search engine matrix arrays to settle
    time.sleep(random.uniform(5.0, 7.0))

    # Parse structural nodes based on semantic text components
    h3_elements = driver.find_elements(By.CSS_SELECTOR, "h3")
    
    data = []
    for h3 in h3_elements:
        try:
            # Ascend node chain to fetch parent anchor tag references
            parent_link = h3.find_element(By.XPATH, "./ancestor::a")
            
            title = h3.text.strip()
            url = parent_link.get_attribute("href")
            
            # Clean programmatic filtering to drop systemic tracking URLs
            if title and url and "google.com" not in url:
                data.append([title, url])
        except Exception:
            continue

    # Persistence to file architecture
    with open("google_search_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL"])
        writer.writerows(data)

    print(f"Scraped {len(data)} high-quality results.")
    print("CSV file updated successfully!")

finally:
    # Safely close down the browser process manually
    try:
        driver.quit()
    except Exception:
        pass
