import undetected_chromedriver as uc
# Patch the shutdown warning bug instantly
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

# 1. Read the Excel sheet data
df = pd.read_excel("backlinks_data.xlsx")

# Grab row 3 data (which is index 1 in Python pandas)
row_data = df.iloc[0] 
target_url = row_data["Website URL Link"]
tagline = row_data["Short Tagline"]

# 2. Open the automated browser
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=151)

try:
    # 3. Open Product Hunt login page
    driver.get("https://producthunt.com")
    
    print("\n👋 MANUAL WORK:")
    print("1. Log in to Product Hunt.")
    print("2. Click '+ Submit', paste the link, and open the page with the Tagline field.")
    
    # Freezes script until you are looking right at the tagline input box
    input("\nOnce you are on the form screen looking at the empty Tagline box, press ENTER here... ")
    
    print("\n[+] Running automation fields...")

    # 4. Automate filling out the Tagline field by looking directly below its text label
    try:
        tagline_input = driver.find_element(By.XPATH, "//*[contains(text(), 'Tagline')]/following::input[1]")
        driver.execute_script("arguments[0].value = arguments[1];", tagline_input, tagline)
        print("[+] Tagline filled successfully!")
    except Exception as e:
        print(f"[!] Could not locate Tagline box using label XPath: {str(e)}")

    # 5. Automate filling out the Link field if needed
    try:
        link_input = driver.find_element(By.XPATH, "//*[contains(text(), 'Link')]/following::input[1] | //input[@type='url']")
        driver.execute_script("arguments[0].value = arguments[1];", link_input, target_url)
        print("[+] Website URL filled successfully!")
    except Exception:
        print("[!] Link field skipped or already filled.")

    print("\n🏆 Product Hunt Automation Complete! Check your browser window to see the filled boxes.")
    time.sleep(10)

finally:
    driver.quit()
