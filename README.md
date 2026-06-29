
```markdown
# UIU UCAM Academic Monitor

An automated Python-based desktop application designed for students of United International University (UIU). This tool monitors the [UCAM portal](https://ucam.uiu.ac.bd/) in the background to track academic grades and notifies the user immediately if any new updates are detected.

## 🚀 Features

* **Automated Tracking:** Periodically checks the UCAM portal for grade updates every 30 minutes.
* **Real-time Alerts:** Automatically brings the application to the foreground and alerts you when a new grade is posted.
* **Privacy First:** Your credentials (Student ID and Password) are stored locally in a JSON file on your computer—never sent to any external server.
* **User-Friendly Interface:** Built with `tkinter` for a clean, intuitive dashboard with features like a password show/hide toggle.
* **Lightweight:** Optimized to consume minimal system resources while running in the background.

## 🛠 Prerequisites

To run this project, you need to have the following installed:

* **Python 3.8+**
* **Google Chrome Browser**
* **Selenium:** Install the required library using pip:

```bash
pip install selenium

```

## ⚙️ Installation & Setup

1. **Clone the repository:**

```bash
git clone [https://github.com/your-username/ucam-academic-monitor.git](https://github.com/your-username/ucam-academic-monitor.git)

```

2. **Navigate to the project folder:**

```bash
cd ucam-academic-monitor

```

3. **Run the application:**

```bash
python ucam_bot.py

```

## 🖥 How to Use

* **Login:** Enter your UIU Student ID and Password in the designated fields.
* **Track:** Click on the **"Switch & Track"** button to start the monitoring process.
* **Dashboard:** The application will display your current Overall CGPA and Completed Credits.
* **Updates:** If a new grade is uploaded, the application will automatically refresh the table and notify you.

## ⚠️ Important Notes

* **Security:** This is a personal tool. Your credentials are only stored on your local machine. Avoid sharing your local `ucam_config.json` file with others.
* **Disclaimer:** This is an unofficial tool. Always verify your results through the official [UCAM website](https://ucam.uiu.ac.bd/).
* **Internet:** A stable internet connection is required for the bot to fetch data from the UCAM server.

## 🤝 Contribution

Contributions are welcome! If you encounter any bugs or have ideas for new features, feel free to open an **Issue** or submit a **Pull Request**.

---

*Developed for UIU Students*


