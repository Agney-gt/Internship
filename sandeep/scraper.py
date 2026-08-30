from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def google_scrape(query):
    driver = webdriver.Chrome()    
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        for index, result in enumerate(results[:10]):
            print(f"{index + 1}. {result.text}")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    google_scrape("python internships for beginners")
