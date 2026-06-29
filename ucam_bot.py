import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ১. অটোমেটিক ক্রোম ব্রাউজার ওপেন করা
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # ২. UCAM এর লগইন পেজে যাওয়া
    driver.get("https://ucam.uiu.ac.bd")
    time.sleep(3) # পেজ লোড হওয়ার জন্য ৩ সেকেন্ড অপেক্ষা
    
    # ৩. আপনার আইডি, পাসওয়ার্ড বক্স এবং লগইন বাটনের ID বসান
    # (এখানে "id_input_id", "password_input_id", "login_button_id" এর জায়গায় 
    # আপনি UCAM লগইন পেজ ইনস্পেক্ট করে যে আসল ID-গুলো পেয়েছেন, সেগুলো লিখে দিন)
    username_field = driver.find_element(By.ID, "id_input_id") 
    password_field = driver.find_element(By.ID, "password_input_id")
    login_button = driver.find_element(By.ID, "login_button_id")
    
    # ৪. বক্সে আপনার স্টুডেন্ট আইডি ও পাসওয়ার্ড টাইপ করা
    username_field.send_keys("আপনার_স্টুডেন্ট_আইডি") 
    password_field.send_keys("আপনার_পাসওয়ার্ড")
    
    # ৫. লগইন বাটনে ক্লিক করা
    login_button.click()
    
    # লগইন হওয়ার পর ড্যাশবোর্ড লোড হতে ৫ সেকেন্ড সময় দেওয়া হলো
    time.sleep(5)
    print("লগইন সফল হয়েছে এবং ড্যাশবোর্ডে এসেছে!")

except Exception as e:
    print("কোথাও একটা ভুল হয়েছে:", e)

finally:
    # কাজ শেষে ব্রাউজার বন্ধ করা
    driver.quit()