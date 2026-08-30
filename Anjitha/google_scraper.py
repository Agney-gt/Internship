from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def search_google(query):
    driver=webdriver.Chrome()
    driver.get("https://www.google.com")
    search_box=driver.find_element(By.XPATH,"//textarea[contains(@name,'q')]")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(15)

    results=driver.find_elements(By.XPATH,"//div[contains(@class,'yuRUbf')]")
    data=[]
    for r in results[:10]:
        
        link=r.find_element(By.XPATH,".//a").get_attribute('href')
        title=r.find_element(By.XPATH,".//h3").text
        data.append({"Title":title,"Link":link})
    
    df = pd.DataFrame(data)
    print("\nData in table format:")
    print(df)
    df.to_csv("searchresults.csv")
    print("\n✅ Successfully created 'searchresults.csv'")
    driver.quit()

if __name__=="__main__":
    query=input("Enter your query:")
    search_google(query)
