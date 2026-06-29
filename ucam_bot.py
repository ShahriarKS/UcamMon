import time
import json
import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HISTORY_FILE = "grades_history.json"
CHECK_INTERVAL_MINUTES = 30

class UcamMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UIU UCAM Academic Monitor")
        self.root.geometry("650x580")
        self.root.configure(bg="#f4f6f9")
        
        # Remaining seconds for countdown tracking
        self.remaining_seconds = CHECK_INTERVAL_MINUTES * 60
        self.is_checking = False
        
        # Style Customization
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Title Label
        title_label = tk.Label(root, text="UCAM Academic Dashboard", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f4f6f9")
        title_label.pack(pady=15)
        
        # Status Bar
        self.status_label = tk.Label(root, text="Bot Status: Initializing...", font=("Arial", 10, "italic"), fg="#7f8c8d", bg="#f4f6f9")
        self.status_label.pack(pady=2)

        # Frame for Summary Card
        summary_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        summary_frame.pack(pady=15, padx=20, fill="x")
        
        self.cgpa_label = tk.Label(summary_frame, text="Overall CGPA: --", font=("Arial", 13, "bold"), fg="#27ae60", bg="#ffffff")
        self.cgpa_label.pack(side="left", padx=30, pady=15)
        
        self.credit_label = tk.Label(summary_frame, text="Completed Credit: --", font=("Arial", 13, "bold"), fg="#2980b9", bg="#ffffff")
        self.credit_label.pack(side="right", padx=30, pady=15)

        # New Update Highlight Box
        self.update_label = tk.Label(root, text="🔍 No new grade updates detected since last check.", font=("Arial", 11, "bold"), fg="#e67e22", bg="#f4f6f9", wraplength=550)
        self.update_label.pack(pady=10)

        # Frame for Treeview (Table)
        table_frame = tk.Frame(root)
        table_frame.pack(padx=20, pady=5, fill="both", expand=True)
        
        columns = ("code", "name", "grade_status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.tree.heading("code", text="Course Code")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("grade_status", text="Grade / Status")
        
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("name", width=350, anchor="w")
        self.tree.column("grade_status", width=140, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for Table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Live Countdown Timer Label at the bottom
        self.timer_label = tk.Label(root, text="⏱ Next Check In: --m --s", font=("Arial", 11, "bold"), fg="#34495e", bg="#f4f6f9")
        self.timer_label.pack(pady=15)
        
        # Start the countdown loop in the UI
        self.update_countdown()
        
        # Trigger the first background check instantly
        self.trigger_background_check()

    def update_ui(self, cgpa, credit, update_text, courses):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        self.cgpa_label.config(text=f"🎯 Overall CGPA: {cgpa}")
        self.credit_label.config(text=f"🎓 Completed Credit: {credit}")
        self.update_label.config(text=update_text)
        
        if "NEW UPDATE" in update_text:
            self.update_label.config(fg="#c0392b")
        else:
            self.update_label.config(fg="#e67e22")

        for course in courses:
            self.tree.insert("", "end", values=(course[0], course[1], course[2]))

    def update_countdown(self):
        if not self.is_checking:
            # Calculate minutes and seconds
            mins, secs = divmod(self.remaining_seconds, 60)
            self.timer_label.config(text=f"⏱ Next Check In: {mins:02d}m {secs:02d}s")
            
            if self.remaining_seconds <= 0:
                self.trigger_background_check()
            else:
                self.remaining_seconds -= 1
                
        # Call this function again after exactly 1 second (1000ms)
        self.root.after(1000, self.update_countdown)

    def trigger_background_check(self):
        self.is_checking = True
        self.timer_label.config(text="🔄 UCAM Check in progress... Please wait.")
        self.status_label.config(text=f"Bot Status: Connecting to UCAM at {datetime.now().strftime('%I:%M:%S %p')}...")
        
        # Run Selenium in a non-blocking background thread
        threading.Thread(target=self.run_selenium_bot, daemon=True).start()

    def run_selenium_bot(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
            wait = WebDriverWait(driver, 10)
            
            username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
            password_field = driver.find_element(By.ID, "logMain_Password")
            
            username_field.send_keys("0112410092") 
            password_field.send_keys("SaikatUIU1!")
            password_field.send_keys(Keys.ENTER)
            
            dashboard_wait = WebDriverWait(driver, 20)
            cgpa_element = dashboard_wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContainer_Status_CGPA")))
            credit_element = driver.find_element(By.ID, "ctl00_MainContainer_Status_CompletedCr")
            
            overall_cgpa = cgpa_element.text.strip()
            completed_credit = credit_element.text.strip()
            
            driver.get("https://ucam.uiu.ac.bd/Student/StudentCourseHistory.aspx?mmi=40545a1642555b514e63")
            time.sleep(5)
            
            rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_MainContainer_gvRegisteredCourse tr.rowCss")
            
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

            prev_grades = {}
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r") as f:
                    prev_grades = json.load(f)

            current_grades = {}
            new_updates = []
            ui_courses = []
            
            for tri_code, cols in valid_rows_data:
                if tri_code == latest_trimester:
                    course_code = cols[1].text.strip()
                    course_name = cols[2].text.strip()
                    grade = cols[4].text.strip()
                    status = cols[5].text.strip()
                    
                    current_grades[course_code] = grade
                    final_grade = grade if grade else status
                    ui_courses.append((course_code, course_name, final_grade))
                    
                    if course_code in prev_grades:
                        if prev_grades[course_code] != grade and grade != "":
                            new_updates.append(f"{course_code} ({grade})")
                    elif grade != "":
                        new_updates.append(f"{course_code} ({grade})")

            with open(HISTORY_FILE, "w") as f:
                json.dump(current_grades, f)

            if new_updates:
                update_text = f"✨ NEW UPDATE DETECTED: {', '.join(new_updates)}"
            else:
                update_text = "🔍 No new grade updates detected since last check."

            # Update UI components via main thread safe method
            self.root.after(0, self.update_ui, overall_cgpa, completed_credit, update_text, ui_courses)
            self.status_label.config(text=f"Bot Status: Idle. Last successful check at {datetime.now().strftime('%I:%M:%S %p')}.")

        except Exception as e:
            self.status_label.config(text=f"Bot Status: Error occurred -> {str(e)[:50]}")
        finally:
            driver.quit()
            # Reset timer back to 30 minutes and resume countdown
            self.remaining_seconds = CHECK_INTERVAL_MINUTES * 60
            self.is_checking = False

if __name__ == "__main__":
    root = tk.Tk()
    app = UcamMonitorApp(root)
    root.mainloop()