import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

# 1. Read the Excel sheet data
df = pd.read_excel("backlinks_data.xlsx")
row_data = df.iloc[0] 
target_url = row_data["Website URL Link"]

# Clear, punchy title for the submission
post_title = "Show HN: Y2Map – Convert YouTube videos and PDFs into interactive mind maps"

# 2. Open the browser
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=151)

try:
    # 3. Direct browser straight to the exact working URL you provided
    driver.get("https://news.ycombinator.com/submit")
    
    print("\n👋 MANUAL WORK PHASE:")
    print("1. Create an account quickly (fill in 'Create Account' and click create account).")
    print("2. The site will automatically redirect you to the Title and URL text boxes.")
    print("3. Ensure those text boxes are empty and visible on your screen.")
    
    # Freezes script until your account is ready and you are looking at the form fields
    input("\nOnce you are logged in and looking at the empty form fields, press ENTER here... ")
    
    print("\n[+] Injecting data using JavaScript...")

    # 4. Fill Title field
    title_input = driver.find_element(By.NAME, "title")
    driver.execute_script("arguments[0].value = arguments[1];", title_input, post_title)
    print("[+] Title field populated.")
    time.sleep(0.5)

    # 5. Fill URL field
    url_input = driver.find_element(By.NAME, "url")
    driver.execute_script("arguments[0].value = arguments[1];", url_input, target_url)
    print("[+] URL field populated.")
    time.sleep(1.0)

    # 6. Click the Submit button safely
    print("[+] Submitting to Hacker News...")
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='submit']")
    driver.execute_script("arguments[0].click();", submit_button)

    print("\n🏆 Hacker News Automation Complete! ✅")
    time.sleep(5)

finally:
    driver.quit()
