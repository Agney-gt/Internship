import tempfile
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

profile = tempfile.mkdtemp()

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + profile)

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
time.sleep(3)

search = driver.find_element(By.XPATH, "//textarea[@name='q']")
search.send_keys("current affairs today India")
search.send_keys(Keys.ENTER)

# Pause for CAPTCHA
input("Solve CAPTCHA if it appears, then press ENTER here...")

data = []

while len(data) < 50:

    results = driver.find_elements(
        By.XPATH,
        "//div[@class='MjjYud']//h3"
    )

    for result in results:
        if len(data) >= 50:
            break

        try:
            title = result.text

            link = result.find_element(
                By.XPATH,
                "./ancestor::a"
            ).get_attribute("href")

            data.append([title, link])

            print("Saved:", title)

        except:
            continue

    if len(data) >= 50:
        break

    try:
        next_button = driver.find_element(
            By.XPATH,
            "//a[@id='pnnext']"
        )

        next_button.click()
        time.sleep(4)

    except:
        print("No more pages available")
        break

with open(
    "current_affairs.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(["Title", "Link"])

    writer.writerows(data)

print("Total results saved:", len(data))
print("Data saved in current_affairs.csv")

driver.quit()