import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Initialize Chrome browser in automated mode
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # 2. Navigate to the UCAM login page
    driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
    
    # 3. Wait for the login fields to load completely
    print("Loading UCAM login page...")
    wait = WebDriverWait(driver, 10)
    
    username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
    password_field = driver.find_element(By.ID, "logMain_Password")
    
    # 4. Type the login credentials
    print("Typing credentials...")
    username_field.send_keys("0112410092") 
    password_field.send_keys("SaikatUIU1!")
    
    # 5. Simulate pressing the physical 'Enter' key to login
    password_field.send_keys(Keys.ENTER)
    
    # 6. Wait for the dashboard to load completely
    print("Login triggered. Loading Dashboard...")
    dashboard_wait = WebDriverWait(driver, 20)
    
    # Fetch Overall CGPA and Completed Credit from the Dashboard
    cgpa_element = dashboard_wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContainer_Status_CGPA")))
    credit_element = driver.find_element(By.ID, "ctl00_MainContainer_Status_CompletedCr")
    
    overall_cgpa = cgpa_element.text.strip()
    completed_credit = credit_element.text.strip()
    print("[✔] Dashboard data fetched successfully!")
    
    # 7. Directly navigate to the Student Course History URL
    print("Navigating to the Course History page...")
    course_history_url = "https://ucam.uiu.ac.bd/Student/StudentCourseHistory.aspx?mmi=40545a1642555b514e63"
    driver.get(course_history_url)
    
    # 8. Wait for the course table to render properly
    time.sleep(5)
    print("Fetching course details...")
    
    # 9. Locate all rows inside the registered course grid
    rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_MainContainer_gvRegisteredCourse tr.rowCss")
    
    # Find the maximum/latest trimester code dynamically
    latest_trimester = 0
    valid_rows_data = []
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 6:
            tri_code_text = cols[0].text.strip()
            if tri_code_text.isdigit():
                tri_code = int(tri_code_text)
                if tri_code > latest_trimester:
                    latest_trimester = tri_code
                valid_rows_data.append((tri_code, cols))

    # 10. PRINT THE FINAL COMBINED ACADEMIC REPORT
    print("\n==============================================")
    print("         UCAM ACADEMIC SUMMARY REPORT         ")
    print("==============================================")
    print(f" 🎯 Overall CGPA      : {overall_cgpa}")
    print(f" 🎓 Completed Credit : {completed_credit}")
    print("----------------------------------------------")
    print(f" 📅 Results for Latest Trimester: {latest_trimester}")
    print("----------------------------------------------")
    
    found_any = False
    for tri_code, cols in valid_rows_data:
        if tri_code == latest_trimester:
            course_code = cols[1].text.strip()
            course_name = cols[2].text.strip()
            grade = cols[4].text.strip()
            status = cols[5].text.strip()
            
            # If the grade cell is empty, fallback to display the course status
            final_grade = grade if grade else status
            
            print(f" 📖 {course_code} - {course_name} | Grade/Status: {final_grade}")
            found_any = True
            
    if not found_any:
        print(" No courses found for the latest trimester.")
                
    print("==============================================\n")

except Exception as e:
    print("\n[!] An unexpected error occurred:")
    print(e)

finally:
    # 11. Close the automated browser session completely
    driver.quit()