# 🛡️ CyberShield – Cybersecurity Learning & Investigation Platform

CyberShield is a Flask-based web application developed to help students learn cybersecurity concepts while providing tools for basic cyber investigations. The platform combines interactive learning modules, security analysis tools, quizzes, Capture The Flag (CTF) challenges, and an admin dashboard into a single application.

---

## 📌 Features

###  User Authentication
- Secure Login & Registration
- User Profile
- Activity History

###  Dashboard
- Interactive dashboard
- Cybersecurity statistics
- User progress tracking
- Achievement badges

###  Password Security Checker
- Password strength analysis
- Security recommendations
- Common password detection

###  Phishing Detection
- Analyze suspicious URLs
- Detect phishing indicators
- Security awareness tips

###  SQL Injection Detector
- Analyze SQL Injection payloads
- Explain attack behavior
- Defensive recommendations

###  XSS Detection
- Detect Cross Site Scripting payloads
- Security validation
- Learning examples

###  Network Scanner
- Scan target IP addresses
- Display open ports
- Basic network reconnaissance

###  Malware Analysis
- Upload suspicious files
- File hash generation
- Basic malware indicator detection
- MITRE ATT&CK mapping

###  Capture The Flag (CTF)
- Beginner-friendly cybersecurity challenges
- Hands-on learning experience
- Score tracking

###  Cybersecurity Quiz
- Multiple-choice questions
- Instant score calculation
- Learning assessment

###  PDF Report Generation
- Generate investigation reports
- Downloadable PDF reports
- Summary of analysis

###  Admin Panel
- User management
- Analytics dashboard
- Platform monitoring

---

#  Technologies Used

## Backend
- Python
- Flask
- SQLAlchemy
- ReportLab

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js

## Database
- MySQL

---

#  Project Structure

```
CyberShield/
│
├── app.py
├── config.py
├── models.py
├── routes/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── uploads/
├── reports/
├── database/
└── requirements.txt
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/CyberShield.git
```

## Move into project

```bash
cd CyberShield
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Database

Create a MySQL database and import the SQL schema.

Update your database credentials inside `config.py`.

## Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

Add screenshots of:

- Login Page
- Dashboard
- Password Checker
- Malware Analysis
- SQL Injection Module
- Admin Dashboard
- Quiz Module
- PDF Report

---

# 📚 Educational Modules

- Password Security
- Phishing Awareness
- SQL Injection
- Cross Site Scripting (XSS)
- Malware Basics
- Network Scanning
- Capture The Flag (CTF)
- Cybersecurity Quiz

---

# 🔒 Security Features

- User Authentication
- Secure Session Management
- Password Validation
- File Upload Validation
- PDF Investigation Reports
- MITRE ATT&CK Technique Mapping
- Activity Tracking

---

#  Future Improvements

- AI-based Threat Detection
- VirusTotal API Integration
- Real-time Network Monitoring
- SIEM Dashboard
- Email Alert System
- Dark Web Monitoring
- Machine Learning Malware Detection

---

#  Author

**Soham Sakpal**

MCA Student | Cybersecurity Enthusiast

GitHub: https://github.com/mca25sakpalsoham-afk

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
