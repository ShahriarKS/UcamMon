# 🎓 UcamMon

**UcamMon** is a Python-based desktop application that automatically monitors the **United International University (UIU) UCAM Portal** for newly published grades. It runs quietly in the background and instantly notifies you whenever a new grade is detected.

> No more refreshing the UCAM portal multiple times a day.

---

## ✨ Features

- 🔄 **Automatic Grade Monitoring**
  - Checks your UCAM portal every **30 minutes** for new grade updates.

- 🔔 **Instant Notifications**
  - Detects newly published grades and immediately alerts you.
  - Automatically brings the application window to the foreground.

- 📊 **Academic Dashboard**
  - Displays your **Overall CGPA**
  - Shows **Completed Credits**
  - Lists all available course grades

- 🔒 **Secure Local Storage**
  - Login credentials are stored **locally** in an **encrypted JSON configuration file**.
  - No credentials are transmitted to any third-party server.

- 🖥 **Simple Desktop Interface**
  - Built using **Tkinter**.
  - Lightweight and easy to use.

- ⚡ **Resource Efficient**
  - Runs quietly in the background with minimal CPU and memory usage.

---

## 🛠 Built With

- Python 3
- Tkinter
- Selenium
- Chrome WebDriver

---

## 📋 Requirements

Before running the application, ensure you have:

- Python **3.8+**
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Selenium

Install Selenium:

```bash
pip install selenium
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/ShahriarKS/ucammon.git
```

### Go to the project directory

```bash
cd UcamMon
```

### Install dependencies

```bash
pip install selenium
```

### Run the application

```bash
python ucammon.py
```

---

## 🖥 Usage

### 1. Login

Enter your:

- UIU Student ID
- UCAM Password

---

### 2. Start Monitoring

Click **"Switch & Track"**.

The application will:

- Log into UCAM
- Retrieve your academic information
- Start monitoring for new grades

---

### 3. Dashboard

The dashboard displays:

- Overall CGPA
- Completed Credits
- Current Grade Sheet

---

### 4. Notification

Whenever a new grade is published:

- The application refreshes automatically.
- A notification is shown immediately.
- The application window is brought to the foreground.

---

## 🔐 Security

Your privacy is important.

- Credentials are stored **only on your local computer**.
- Data is encrypted before being saved.
- No information is uploaded to external servers.
- **Never share your `ucammon_config.json` file.**

---
## Sample
<p align="center">
  <img src="bot%20img.png" width="700">
</p>

## 📂 Project Structure

```
UcamMon/
│
├── ucammon.py
├── ucammon_config.json
├── assets/
├── README.md
└── requirements.txt
```

---

## ⚠ Disclaimer

UcamMon is an **unofficial project** and is **not affiliated with United International University (UIU)**.

This application is intended solely for personal convenience. Always verify your grades through the official UCAM portal.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome.

Feel free to:

- Fork the repository
- Create a feature branch
- Submit a Pull Request

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.
