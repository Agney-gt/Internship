import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

search_query = "Python web scraping tutorial"
url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")
driver.get(url)
time.sleep(2)

search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

titles = []
links = []

for result in search_results:
    try:
        title = result.find_element(By.CSS_SELECTOR, "h3").text
        link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        if title and link:
            titles.append(title)
            links.append(link)
    except:
        pass

driver.quit()

data = pd.DataFrame({"title": titles, "link": links})
print(data)

data.to_csv("google_search_results.csv", index=False)
print("Saved results to google_search_results.csv")
