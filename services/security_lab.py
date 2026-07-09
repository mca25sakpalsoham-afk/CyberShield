import hashlib
import os
import re

from werkzeug.utils import secure_filename

COMMON_PASSWORDS = {
    "password",
    "123456",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
}


def human_duration(seconds):
    if seconds < 60:
        return f"{seconds:.1f} seconds"

    minutes = seconds / 60

    if minutes < 60:
        return f"{minutes:.1f} minutes"

    hours = minutes / 60

    if hours < 24:
        return f"{hours:.1f} hours"

    days = hours / 24

    if days < 365:
        return f"{days:.1f} days"

    years = days / 365

    return f"{years:.1f} years"


def password_report(password):
    length = len(password)

    classes = sum(
        [
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"\d", password)),
            bool(re.search(r"[^A-Za-z0-9]", password)),
        ]
    )

    score = min(100, length * 6 + classes * 12)

    weaknesses = []

    if length < 12:
        weaknesses.append("Use at least 12 characters.")

    if password.lower() in COMMON_PASSWORDS:
        score = min(score, 20)
        weaknesses.append("Common dictionary password detected.")

    if not re.search(r"[^A-Za-z0-9]", password):
        weaknesses.append("Add special characters.")

    if not weaknesses:
        weaknesses.append("Strong password.")

    charset = max(classes, 1) * 26
    guesses = charset ** max(length, 1)
    brute_seconds = guesses / 1_000_000_000
    
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    entropy = round(length * 4.7, 1)

    return {
        "score": score,
        "weaknesses": weaknesses,
        
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "entropy": entropy,
        
        "dictionary_status": (
            "High Risk"
            if score < 35
            else "Medium Risk"
            if score < 70
            else "Low Risk"
        ),
        "classification": (
            "Strong"
            if score >= 80
            else "Moderate"
            if score >= 60
            else "Weak"
        ),
        "brute_force_duration": human_duration(brute_seconds),
    }


def simulated_sql_login(username, password):

    payload = f"{username} {password}".lower()

    attack_type = None

    patterns = {
        "Authentication Bypass": [
            "' or '1'='1",
            '" or "1"="1',
            "' or 1=1",
            "or 1=1--",
            "admin'--",
            "'--",
            "' or ''='",
            "admin' or 'x'='x",
            "' or true--"
        ],

        "UNION-based Injection": [
            "union select",
            "' union"
        ]
    }

    bypass = False

    for attack, signatures in patterns.items():

        if any(sig in payload for sig in signatures):

            bypass = True
            attack_type = attack
            break

    return {
        "vulnerable_result":
            "Login Bypassed"
            if bypass
            else
            "Login Rejected",

        "secure_result":
            "Blocked by Parameterized Query",

        "bypass": bypass,

        "attack_type":
            attack_type if attack_type else "No Attack",

        "risk":
            "CRITICAL" if bypass else "LOW",

        "explanation":
            (
                "The vulnerable query accepted a malicious SQL payload. "
                "Parameterized queries treat input as data and prevent injection."
            )
            if bypass
            else
            "No SQL Injection pattern detected."
    }


def sanitize_xss(value):

    attack_type = "No Attack"
    severity = "LOW"
    risk_score = 5

    payload = value.lower()

    if "<script" in payload:
        attack_type = "Reflected XSS"
        severity = "HIGH"
        risk_score = 95

    elif "onerror=" in payload:
        attack_type = "Event Handler XSS"
        severity = "HIGH"
        risk_score = 90

    elif "<svg" in payload:
        attack_type = "SVG XSS"
        severity = "HIGH"
        risk_score = 85

    elif "onload=" in payload:
        attack_type = "DOM/Event XSS"
        severity = "HIGH"
        risk_score = 80

    elif "javascript:" in payload:
        attack_type = "Script URL XSS"
        severity = "HIGH"
        risk_score = 88

    sanitized = (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
    
    explanation = "No attack detected."

    if attack_type == "Reflected XSS":
        explanation = "Script tags inject executable JavaScript into a web page."

    elif attack_type == "Event Handler XSS":
        explanation = "JavaScript executes when a browser event such as an image error occurs."

    elif attack_type == "SVG XSS":
        explanation = "SVG elements can contain executable JavaScript."

    elif attack_type == "DOM/Event XSS":
        explanation = "The payload executes through browser DOM events."

    elif attack_type == "Script URL XSS":
        explanation = "JavaScript URLs can execute code when rendered."

    return {
    "original": value,
    "sanitized": sanitized,
    "attack_type": attack_type,
    "severity": severity,
    "risk_score": risk_score,
    "explanation": explanation,
    "owasp": "A03:2021 Injection",
    "cwe": "CWE-79"
}

def simulated_scan(ip_address):
    profiles = [
        {
            "ports": [
                (22, "SSH", "Open"),
                (80, "HTTP", "Open"),
                (443, "HTTPS", "Open"),
            ],
            "risk": "Medium",
        },
        {
            "ports": [
                (21, "FTP", "Open"),
                (3306, "MySQL", "Open"),
                (8080, "Proxy", "Open"),
            ],
            "risk": "High",
        },
        {
            "ports": [
                (53, "DNS", "Open"),
                (443, "HTTPS", "Open"),
            ],
            "risk": "Low",
        },
    ]

    idx = sum(ord(c) for c in ip_address) % len(profiles)

    return profiles[idx]


def analyze_upload(file_storage, upload_folder):
    print("UPLOAD_FOLDER =", upload_folder)

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(
        file_storage.filename or "uploaded.bin"
    )

    print("FILENAME =", filename)

    path = os.path.abspath(
        os.path.join(upload_folder, filename)
    )

    print("SAVE PATH =", path)

    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass

    file_storage.save(path)

    md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    size = 0

    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            size += len(chunk)
            md5.update(chunk)
            sha256.update(chunk)

    ext = os.path.splitext(filename)[1].lower()

    risky_ext = {
        ".exe",
        ".dll",
        ".bat",
        ".cmd",
        ".scr",
        ".js",
        ".vbs",
        ".ps1",
    }

    if ext in risky_ext:
        risk = "High"
    elif size > 2 * 1024 * 1024:
        risk = "Medium"
    else:
        risk = "Low"

    risk_score = 20

    if risk == "High":
        risk_score = 85
    elif risk == "Medium":
        risk_score = 60
    else:
        risk_score = 25

    if ext in {".exe", ".dll"}:
        malware_type = "Trojan"
    elif ext in {".js", ".vbs"}:
        malware_type = "Script Malware"
    elif ext in {".bat", ".cmd", ".ps1"}:
        malware_type = "Potential Backdoor"
    else:
        malware_type = "Unknown"

    ioc = []

    if ext in risky_ext:
        ioc.append("Executable or Script File")

    if size > 2 * 1024 * 1024:
        ioc.append("Large File Size")

    if filename.count(".") > 1:
        ioc.append("Multiple File Extensions")

    if ext == ".bat":
        mitre = [
            "T1059 - Command and Scripting Interpreter"
        ]

    elif ext == ".exe":
        mitre = [
            "T1105 - Ingress Tool Transfer",
            "T1071 - Application Layer Protocol"
        ]

    elif ext == ".ps1":
        mitre = [
            "T1059.001 - PowerShell",
            "T1082 - System Information Discovery"
        ]

    elif ext == ".js":
        mitre = [
            "T1059.007 - JavaScript",
            "T1071 - Application Layer Protocol"
        ]

    else:
        mitre = [
            "T1082 - System Information Discovery"
        ]

    recommendations = [
        "Do not execute the file",
        "Scan with antivirus software",
        "Upload to sandbox environment",
        "Monitor network activity",
        "Verify file source"
    ]
    
    size_kb = round(size / 1024, 2)

    return {
        "filename": filename,
        "md5": md5.hexdigest(),
        "sha256": sha256.hexdigest(),
        "extension": ext,
        "size": size,
        "size_kb": size_kb,
        "risk": risk,

        "risk_score": risk_score,
        "malware_type": malware_type,
        "ioc": ioc,
        "mitre": mitre,
        "recommendations": recommendations
    }