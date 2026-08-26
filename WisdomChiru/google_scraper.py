import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

search_query = "Python web scraping tutorial"
url = "https://www.google.com/search?q=" + search_query.replace(" ", "+") + "&hl=en&gl=us"
driver.get(url)
time.sleep(4)

input("If you see a CAPTCHA in the browser window, solve it now, then press Enter here to continue...")

try:
    consent_button = driver.find_element(By.XPATH, "//button[.//div[contains(text(),'Accept all')]]")
    consent_button.click()
    time.sleep(2)
except Exception:
    pass

titles = []
links = []

result_blocks = driver.find_elements(By.CSS_SELECTOR, "div.g")
if not result_blocks:
    result_blocks = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
if not result_blocks:
    result_blocks = driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")

for result in result_blocks:
    try:
        title = result.find_element(By.CSS_SELECTOR, "h3").text
        link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        if title and link:
            titles.append(title)
            links.append(link)
    except Exception:
        pass

if not titles:
    with open("debug_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("No results found. Saved page HTML to debug_page_source.html for inspection.")
else:
    print(f"Found {len(titles)} results.")

time.sleep(3)
driver.quit()

data = pd.DataFrame({"title": titles, "link": links})
print(data)

data.to_csv("google_search_results.csv", index=False)
print("Saved results to google_search_results.csv")
