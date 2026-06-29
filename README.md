# UcamMon 🎓

**UcamMon** is an automated Python-based desktop application designed for students of **United International University (UIU)**. This tool monitors the [UCAM portal](https://ucam.uiu.ac.bd/) in the background to track academic grades and notifies you immediately if any new updates are detected.

## 🚀 **Features**

* **Automated Tracking:** Periodically checks your UCAM portal for grade updates every 30 minutes.
* **Real-time Alerts:** Automatically brings the application to the foreground and alerts you the moment a new grade is posted.
* **Secure Storage:** Your credentials are stored locally in an encrypted JSON file on your machine—never sent to any external server.
* **User-Friendly Interface:** Built with `tkinter` for a clean, intuitive dashboard.
* **Lightweight:** Highly optimized to consume minimal system resources while running in the background.

## 🛠 **Prerequisites**

To run this project, you need:
* **Python 3.8+**
* **Google Chrome Browser**
* **Selenium:** Install the required library using pip:

```bash
pip install selenium

🛠 Prerequisites
To run this project, you need:


Bash


pip install selenium
⚙️ Installation & Setup
Clone the repository:

Bash


git clone https://github.com/ShahriarKS/ucam_bot.git
Navigate to the project folder:

Bash


cd UcamMon
Run the application:

Bash


python ucammon.py
🖥 How to Use
Login: Enter your UIU Student ID and Password in the designated fields.

Track: Click on the "Switch & Track" button to start the monitoring process.

Dashboard: The app displays your current Overall CGPA and Completed Credits.

Updates: If a new grade is uploaded, the table refreshes automatically and notifies you.

⚠️ Important Notes
Security: This is a personal tool. Your credentials are only stored locally on your device. Please do not share your ucammon_config.json file.

Disclaimer: This is an unofficial tool. Always verify your results through the official UCAM website.

🤝 Contribution
Contributions are welcome! If you encounter any bugs or have ideas for new features, feel free to open an Issue or submit a Pull Request.

Developed for UIU Students
