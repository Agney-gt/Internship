from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def google_search(query):
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com/search?q=selenium&sca_esv=f84ae5225a953008&rlz=1C1CHBF_enIN1090IN1090&sxsrf=AE3TifMASEPVUh2aJoceROB3OYICVlz9yg%3A1763285703662&ei=x5oZadiRKJmt4-EP9MLt4QU&ved=0ahUKEwiYkYSQr_aQAxWZ1jgGHXRhO1wQ4dUDCBE&uact=5&oq=selenium&gs_lp=Egxnd3Mtd2l6LXNlcnAiCHNlbGVuaXVtMg0QABiABBixAxhDGIoFMg4QABiABBiRAhixAxiKBTIOEAAYgAQYkQIYsQMYigUyDhAAGIAEGJECGLEDGIoFMg4QABiABBiRAhixAxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixA0joC1AAWK8KcAB4AZABAJgB7gKgAcQMqgEHMC43LjAuMbgBA8gBAPgBAZgCCKACsQ3CAgoQIxiABBgnGIoFwgILEAAYgAQYkQIYigXCAgsQABiABBixAxiDAcICDhAAGIAEGLEDGIMBGIoFwgIFEAAYgATCAgoQLhiABBgnGIoFwgIEECMYJ8ICDRAAGIAEGLEDGBQYhwLCAhcQLhiABBiKBRiXBRjcBBjeBBjfBNgBAcICCBAuGIAEGLEDwgINEC4YgAQYsQMYQxiKBZgDALoGBggBEAEYFJIHBzAuNS4yLjGgB55WsgcHMC41LjIuMbgHsQ3CBwUyLTMuNcgHVg&sclient=gws-wiz-serp")
    time.sleep(1)

    box = driver.find_element(By.NAME, "q")
    box.send_keys(query)
    box.send_keys(Keys.RETURN)

    time.sleep(2)
    print("Page Title:", driver.title)

    driver.quit()

google_search("selenium python tutorial")
