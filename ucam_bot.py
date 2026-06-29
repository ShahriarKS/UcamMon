import time
import json
import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CONFIG_FILE = "ucam_config.json"
HISTORY_FILE = "grades_history.json"
CHECK_INTERVAL_MINUTES = 30

class UcamMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UIU UCAM Academic Monitor")
        self.root.geometry("650x620")
        self.root.configure(bg="#f4f6f9")
        
        self.remaining_seconds = CHECK_INTERVAL_MINUTES * 60
        self.is_checking = False
        
        # UI Customization
        title_label = tk.Label(root, text="UCAM Academic Dashboard", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f4f6f9")
        title_label.pack(pady=10)
        
        # --- LOGIN CREDENTIALS INPUT AREA ---
        login_frame = tk.LabelFrame(root, text=" UCAM Login Credentials ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#34495e")
        login_frame.pack(padx=20, pady=5, fill="x")
        
        tk.Label(login_frame, text="Student ID:", bg="#f4f6f9", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = tk.Entry(login_frame, width=20, font=("Arial", 10))
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(login_frame, text="UCAM Password:", bg="#f4f6f9", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.pass_entry = tk.Entry(login_frame, width=20, show="*", font=("Arial", 10))
        self.pass_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        self.load_credentials()
        
        # --- STATUS & REPORT AREA ---
        self.status_label = tk.Label(root, text="Bot Status: Ready. Enter credentials and click Start.", font=("Arial", 10, "italic"), fg="#7f8c8d", bg="#f4f6f9")
        self.status_label.pack(pady=5)

        summary_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        summary_frame.pack(pady=10, padx=20, fill="x")
        
        self.cgpa_label = tk.Label(summary_frame, text="Overall CGPA: --", font=("Arial", 13, "bold"), fg="#27ae60", bg="#ffffff")
        self.cgpa_label.pack(side="left", padx=30, pady=12)
        
        self.credit_label = tk.Label(summary_frame, text="Completed Credit: --", font=("Arial", 13, "bold"), fg="#2980b9", bg="#ffffff")
        self.credit_label.pack(side="right", padx=30, pady=12)

        self.update_label = tk.Label(root, text="🔍 Awaiting connection...", font=("Arial", 11, "bold"), fg="#e67e22", bg="#f4f6f9", wraplength=550)
        self.update_label.pack(pady=5)

        # Treeview (Table)
        table_frame = tk.Frame(root)
        table_frame.pack(padx=20, pady=5, fill="both", expand=True)
        
        columns = ("code", "name", "grade_status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        self.tree.heading("code", text="Course Code")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("grade_status", text="Grade / Status")
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("name", width=350, anchor="w")
        self.tree.column("grade_status", width=140, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom Control Area
        control_frame = tk.Frame(root, bg="#f4f6f9")
        control_frame.pack(pady=10, fill="x", padx=20)
        
        self.start_btn = tk.Button(control_frame, text="▶ Start Monitoring", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", bd=0, padx=15, pady=5, command=self.save_and_start)
        self.start_btn.pack(side="left")
        
        self.timer_label = tk.Label(control_frame, text="⏱ Timer: Inactive", font=("Arial", 11, "bold"), fg="#34495e", bg="#f4f6f9")
        self.timer_label.pack(side="right", pady=5)

    def load_credentials(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.id_entry.insert(0, data.get("username", ""))
                    self.pass_entry.insert(0, data.get("password", ""))
            except: pass

    def save_and_start(self):
        u_id = self.id_entry.get().strip()
        u_pass = self.pass_entry.get().strip()
        
        if not u_id or not u_pass:
            messagebox.showerror("Error", "Please fill up both ID and Password fields!")
            return
            
        with open(CONFIG_FILE, "w") as f:
            json.dump({"username": u_id, "password": u_pass}, f)
            
        self.start_btn.config(state="disabled", bg="#bdc3c7", text="🚀 Bot Running")
        
        # Minimize the window instantly after starting so it stays in background
        self.root.iconify()
        
        self.update_countdown()
        self.trigger_background_check()

    def update_ui(self, cgpa, credit, update_text, courses, has_new_update):
        for row in self.tree.get_children(): self.tree.delete(row)
        self.cgpa_label.config(text=f"🎯 Overall CGPA: {cgpa}")
        self.credit_label.config(text=f"🎓 Completed Credit: {credit}")
        self.update_label.config(text=update_text)
        self.update_label.config(fg="#c0392b" if has_new_update else "#e67e22")
        for course in courses: self.tree.insert("", "end", values=(course[0], course[1], course[2]))
        
        # MAGIC LOGIC: If a change is detected, pop up and maximize the window onto the screen!
        if has_new_update:
            self.root.deiconify()  # Restore from minimize
            self.root.state('normal') # Make sure it's windowed normally
            self.root.attributes("-topmost", True)  # Force to front
            self.root.attributes("-topmost", False) # Release restriction so user can minimize again

    def update_countdown(self):
        if not self.is_checking and self.start_btn.cget("state") == "disabled":
            mins, secs = divmod(self.remaining_seconds, 60)
            self.timer_label.config(text=f"⏱ Next Check In: {mins:02d}m {secs:02d}s")
            if self.remaining_seconds <= 0:
                self.trigger_background_check()
            else:
                self.remaining_seconds -= 1
        self.root.after(1000, self.update_countdown)

    def trigger_background_check(self):
        self.is_checking = True
        self.timer_label.config(text="🔄 Checking UCAM...")
        threading.Thread(target=self.run_selenium_bot, daemon=True).start()

    def run_selenium_bot(self):
        u_id = self.id_entry.get().strip()
        u_pass = self.pass_entry.get().strip()
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://ucam.uiu.ac.bd/Security/Login.aspx")
            wait = WebDriverWait(driver, 10)
            
            username_field = wait.until(EC.presence_of_element_located((By.ID, "logMain_UserName")))
            password_field = driver.find_element(By.ID, "logMain_Password")
            
            username_field.send_keys(u_id) 
            password_field.send_keys(u_pass)
            password_field.send_keys(Keys.ENTER)
            
            dashboard_wait = WebDriverWait(driver, 15)
            cgpa_element = dashboard_wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContainer_Status_CGPA")))
            credit_element = driver.find_element(By.ID, "ctl00_MainContainer_Status_CompletedCr")
            
            overall_cgpa = cgpa_element.text.strip()
            completed_credit = credit_element.text.strip()
            
            driver.get("https://ucam.uiu.ac.bd/Student/StudentCourseHistory.aspx?mmi=40545a1642555b514e63")
            time.sleep(4)
            
            rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_MainContainer_gvRegisteredCourse tr.rowCss")
            latest_trimester = 0
            valid_rows_data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 6:
                    tri_code_text = cols[0].text.strip()
                    if tri_code_text.isdigit():
                        tri_code = int(tri_code_text)
                        if tri_code > latest_trimester: latest_trimester = tri_code
                        valid_rows_data.append((tri_code, cols))

            prev_grades = {}
            if os.path.exists(HISTORY_FILE):
                try:
                    with open(HISTORY_FILE, "r") as f: prev_grades = json.load(f)
                except: pass

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
                    ui_courses.append((course_code, course_name, grade if grade else status))
                    
                    if course_code in prev_grades:
                        if prev_grades[course_code] != grade and grade != "":
                            new_updates.append(f"{course_code} ({grade})")
                    elif grade != "":
                        new_updates.append(f"{course_code} ({grade})")

            with open(HISTORY_FILE, "w") as f: json.dump(current_grades, f)

            has_new_update = len(new_updates) > 0
            update_text = f"✨ NEW UPDATE DETECTED: {', '.join(new_updates)}" if has_new_update else "🔍 No new grade updates detected since last check."
            
            # Send results back to UI safely
            self.root.after(0, self.update_ui, overall_cgpa, completed_credit, update_text, ui_courses, has_new_update)
            self.status_label.config(text=f"Bot Status: Idle. Last checked at {datetime.now().strftime('%I:%M:%S %p')}.")

        except Exception as e:
            self.status_label.config(text="Bot Status: Error! Check ID/Password or Internet.")
        finally:
            driver.quit()
            self.remaining_seconds = CHECK_INTERVAL_MINUTES * 60
            self.is_checking = False

if __name__ == "__main__":
    root = tk.Tk()
    app = UcamMonitorApp(root)
    root.mainloop()