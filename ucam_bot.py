import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Keyboard keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Open the Chrome browser automatically
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # 2. Navigate to the UCAM login page
    driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
    
    # 3. Wait up to 10 seconds for the login fields to appear
    print("Waiting for the UCAM login page to load...")
    wait = WebDriverWait(driver, 10)
    
    # Locate UserID and Password using the correct IDs you found
    username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
    password_field = driver.find_element(By.ID, "logMain_Password")
    
    # 4. Type Student ID
    print("Typing Student ID...")
    username_field.send_keys("0112410092") 
    
    # 5. Type Password and Press ENTER Key immediately
    print("Typing Password and pressing Enter...")
    password_field.send_keys("SaikatUIU1!")
    password_field.send_keys(Keys.ENTER) # It simulates pressing the physical Enter key
    
    # Wait 8 seconds to let the dashboard completely load after logging in
    print("Waiting for dashboard to load...")
    time.sleep(8)
    print("\n[✔] Login successful! Entered the dashboard.")

except Exception as e:
    print("\n[!] An error occurred:")
    print(e)

finally:
    # Close the browser session
    driver.quit()