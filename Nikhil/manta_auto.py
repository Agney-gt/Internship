import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# 1. Read the Excel sheet data safely
df = pd.read_excel("backlinks_data.xlsx")
row_data = df.iloc[-1] 

target_url = str(row_data["Website URL Link"])
tagline = str(row_data["Short Tagline"])
description = str(row_data["Long Description"])

# 2. Boot Chrome setup
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=151)
wait = WebDriverWait(driver, 15)

try:
    # 3. Open Manta's setup page
    driver.get("https://manta.com")
    
    print("\n👋 MANUAL STEP:")
    print("1. Log in to your verified account on the Chrome window.")
    print("2. Advance until you see the empty business details creation form fields.")
    
    input("\nOnce you are on the form screen looking at the empty fields, press ENTER here... ")
    
    print("\n[+] Context Shift: Looking for isolated iframe windows...")
    
    # Locate all iframes on the current workspace layout page
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    
    # If Manta loaded the form inside a layout frame context, switch inside it dynamically
    if len(iframes) > 0:
        print(f"[+] Found {len(iframes)} active iframes. Switching context to the primary form workspace...")
        driver.switch_to.frame(iframes[0])
    
    print("[+] Injecting Manta structural data fields...")
    
    # 4. Company Name Field Injection using highly resilient fallback selectors
    name_input = wait.until(EC.presence_of_element_located((
        By.XPATH, "//input[@id='name' or @name='name' or contains(@autocomplete, 'organization')]"
    )))
    driver.execute_script("arguments[0].value = 'Y2Map'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", name_input)
    print("[+] Company name injected successfully.")
    
    # 5. Address Placeholders Injection (Bypasses US Validation Scripts)
    street_input = driver.find_element(By.XPATH, "//input[contains(@id, 'street') or contains(@autocomplete, 'street-address')]")
    driver.execute_script("arguments[0].value = '123 Main Street'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", street_input)
    
    city_input = driver.find_element(By.XPATH, "//input[contains(@id, 'city') or contains(@autocomplete, 'address-level2')]")
    driver.execute_script("arguments[0].value = 'New York'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", city_input)
    
    zip_input = driver.find_element(By.XPATH, "//input[contains(@id, 'zip') or contains(@autocomplete, 'postal-code')]")
    driver.execute_script("arguments[0].value = '10001'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", zip_input)
    print("[+] Region-bypass address matrix injected successfully.")
    
    # 6. Check public display suppression toggle safely
    try:
        hide_checkbox = driver.find_element(By.XPATH, "//input[contains(@id, 'hide') or @type='checkbox']")
        if not hide_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", hide_checkbox)
            print("[+] Public address suppression privacy checked.")
    except Exception:
        pass
        
    print("\n🏆 Manta Input Field Automation Complete! ✅")
    print("Add your service area manually, click 'Add my company', and take your final success screenshot!")
    time.sleep(10)

except Exception as e:
    print(f"\n[!] Automation error details: {str(e)}")

finally:
    driver.quit()
