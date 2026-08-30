import undetected_chromedriver as uc
# Overwrite the broken class destructor method to prevent the invalid handle popup on close
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

# 1. Read the Excel data cleanly
df = pd.read_excel("backlinks_data.xlsx")
row_data = df.iloc[0]
target_url = row_data["Website URL Link"]
tagline = row_data["Short Tagline"]
description = row_data["Long Description"]

# 2. Boot browser configuration setup
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=151)

try:
    # 3. GO STRAIGHT TO THE METADATA EDIT URL (Bypasses homepage confusion)
    driver.get("https://sourceforge.net")
    
    print("\n👋 MANUAL PHASE:")
    print("1. Since you are already logged in on your main browser, your session might be empty here.")
    print("2. Log in quickly if prompted.")
    print("3. Click 'Metadata' on the left sidebar menu if it doesn't open automatically.")
    print("\n👉 CRITICAL STEP:")
    
        # Halts script until you are explicitly looking at the text fields
    input("Once you are on the Metadata page looking at the input fields, press ENTER here... ")
    
    print("\n[+] Injecting data using JavaScript execution matrices...")

    try:
        # Locate the core fields using flexible attribute identifiers
        homepage_input = driver.find_element(By.XPATH, "//input[contains(@name, 'homepage') or contains(@id, 'homepage')]")
        summary_input = driver.find_element(By.XPATH, "//input[contains(@name, 'summary') or contains(@id, 'summary')]")
        desc_textarea = driver.find_element(By.XPATH, "//textarea[contains(@name, 'description') or contains(@id, 'description')]")
        
        # Force fill the inputs via JavaScript to bypass ElementNotInteractable restrictions
        driver.execute_script("arguments[0].value = arguments[1];", homepage_input, target_url)
        print("[+] Homepage field populated successfully.")
        time.sleep(0.5)

        driver.execute_script("arguments[0].value = arguments[1];", summary_input, tagline)
        print("[+] Short Summary field populated successfully.")
        time.sleep(0.5)

        driver.execute_script("arguments[0].value = arguments[1];", desc_textarea, description)
        print("[+] Full Description field populated successfully.")
        time.sleep(1.0)

        # Locate and click Save button safely using Javascript execution
        print("[+] Submitting form data...")
        save_button = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Save')] | //button[contains(text(), 'Save')]")
        driver.execute_script("arguments[0].click();", save_button)
        
        print("\n🏆 SourceForge Automation Completed Successfully! ✅")
        time.sleep(5)

    except Exception as e:
        print(f"\n[!] Error during form handling: {str(e)}")
        print("Please check if you are actively looking at the correct Metadata form inputs.")

finally:
    driver.quit()
