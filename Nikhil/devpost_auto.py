import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
import pandas as pd
import time

# 1. Read the Excel sheet data
df = pd.read_excel("backlinks_data.xlsx")

# Automatically pull the very last available row to prevent index crashes
row_data = df.iloc[-1] 

target_url = str(row_data["Website URL Link"])
tagline = str(row_data["Short Tagline"])
description = str(row_data["Long Description"])

print(f"[+] Loaded data from Excel for product URL: {target_url}")

# 2. Boot Chrome setup
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=151)

try:
    # 3. Direct browser straight to the project setup panel
    driver.get("https://devpost.com")
    
    print("\n👋 MANUAL STEP:")
    print("1. Click the 'No, I'm just adding it to my portfolio' box.")
    print("2. Type 'Y2Map' into the title field, pass the captcha, and click Save.")
    print("3. Wait until you see the big form page with Description and Tagline boxes.")
    
    input("\nOnce you are on the big form page looking at the boxes, press ENTER here... ")
    
    print("\n[+] Injecting data layout fields via JavaScript...")

    # 4. Fill Tagline field (Elevator Pitch)
    tagline_input = driver.find_element(By.XPATH, "//input[contains(@id, 'tagline')]")
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", tagline_input, tagline)
    print("[+] Tagline field populated successfully.")
    time.sleep(0.5)

    # 5. Fill Description TextArea field (About the project)
    desc_textarea = driver.find_element(By.XPATH, "//textarea[contains(@id, 'description')]")
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", desc_textarea, description)
    print("[+] Description field populated successfully.")
    time.sleep(0.5)

    # 6. Fill 'Try it out' link box
    link_input = driver.find_element(By.XPATH, "//input[contains(@id, 'urls_attributes') and @type='url']")
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", link_input, target_url)
    print("[+] Project backlink URL populated successfully.")
    time.sleep(1.0)

    print("\n🏆 Devpost Input Field Automation Complete! ✅")
    print("Review the populated text boxes, add your built-with tags, and click save!")
    time.sleep(10)

except Exception as e:
    print(f"\n[!] Automation error details: {str(e)}")

finally:
    driver.quit()
