from flask import Blueprint, current_app, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from models import db
from models.entities import ActivityLog, Badge, CTFChallenge, CTFSubmission, PhishingExample, QuizQuestion, QuizResult, UserProgress
from services.achievements import award_badge
from services.reports import generate_user_report
from services.security_lab import analyze_upload, password_report, sanitize_xss, simulated_scan, simulated_sql_login
from models.entities import UserProgress

main_bp = Blueprint("main", __name__)


MODULES = ["Password Lab", "Phishing Lab", "SQL Injection Lab", "XSS Lab", "Network Scanner", "Malware Analysis", "Quiz Arena", "CTF"]


def mark_progress(module, score=100):
    progress = UserProgress.query.filter_by(user_id=current_user.id, module_name=module).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id, module_name=module)
    progress.completed = True
    progress.score = max(progress.score or 0, score)
    db.session.add(progress)
    db.session.add(ActivityLog(user_id=current_user.id, action=f"Completed {module}", details=f"Score {score}"))
    db.session.commit()


def dashboard_metrics(user):
    completed = sum(1 for item in user.progress if item.completed)
    quiz_score = user.quiz_results[-1].percentage if user.quiz_results else 0
    badge_count = len(user.badges)
    security_score = int(min(100, completed * 9 + quiz_score * 0.25 + badge_count * 5))
    return completed, quiz_score, badge_count, security_score


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard") if current_user.is_authenticated else url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    completed, quiz_score, badge_count, security_score = dashboard_metrics(current_user)

    module_scores = {
        "Password Lab": 0,
        "Phishing Lab": 0,
        "SQL Injection Lab": 0,
        "XSS Lab": 0,
        "Network Scanner": 0,
        "Malware Analysis": 0,
        "CTF": 0
    }

    for item in current_user.progress:
        module_scores[item.module_name] = item.score

    radar_data = [
        module_scores["Password Lab"],
        module_scores["Phishing Lab"],
        module_scores["SQL Injection Lab"],
        module_scores["XSS Lab"],
        module_scores["Network Scanner"],
        module_scores["Malware Analysis"],
        module_scores["CTF"]
    ]

    return render_template(
        "dashboard.html",
        modules=MODULES,
        module_scores=module_scores,
        radar_data=radar_data,
        completed=completed,
        quiz_score=quiz_score,
        badge_count=badge_count,
        security_score=security_score
    )

@main_bp.route("/labs/password", methods=["GET", "POST"])
@login_required
def password_lab():
    report = None
    if request.method == "POST":
        report = password_report(request.form.get("password", ""))
        mark_progress("Password Lab", report["score"])
        if report["score"] >= 75:
            award_badge(current_user, "Password Security Expert")
    return render_template("labs/password.html", report=report)


@main_bp.route("/labs/phishing", methods=["GET", "POST"])
@login_required
def phishing_lab():
    examples = PhishingExample.query.all()
    result = None
    if request.method == "POST":
        score = 0
        feedback = []
        for item in examples:
            answer = request.form.get(f"email_{item.id}") == "phishing"
            correct = answer == item.is_phishing
            score += int(correct)
            feedback.append({"subject": item.subject, "correct": correct, "explanation": item.explanation})
        percent = int((score / max(len(examples), 1)) * 100)
        mark_progress("Phishing Lab", percent)
        if percent >= 80:
            award_badge(current_user, "Phishing Hunter")
        result = {"score": score, "total": len(examples), "percent": percent, "feedback": feedback}
    return render_template("labs/phishing.html", examples=examples, result=result)


@main_bp.route("/labs/sql-injection", methods=["GET", "POST"])
@login_required
def sql_lab():
    result = None
    if request.method == "POST":
        result = simulated_sql_login(request.form.get("username", ""), request.form.get("password", ""))
        mark_progress("SQL Injection Lab", 100 if result["bypass"] else 70)
        if result["bypass"]:
            award_badge(current_user, "SQL Injection Master")
    return render_template("labs/sql.html", result=result)


@main_bp.route("/labs/xss", methods=["GET", "POST"])
@login_required
def xss_lab():

    result = None

    if request.method == "POST":

        payload = request.form.get("payload", "")

        result = sanitize_xss(payload)

        mark_progress("XSS Lab", 100)

    return render_template(
        "labs/xss.html",
        result=result
    )


@main_bp.route("/labs/network-scanner", methods=["GET", "POST"])
@login_required
def scanner_lab():
    scan = None
    ip_address = ""

    if request.method == "POST":
        ip_address = request.form.get("ip_address", "")
        scan = simulated_scan(ip_address)
        critical_count = sum(
            1 for v in scan["vulnerabilities"]
            if v["severity"] == "Critical"
        )

        high_count = sum(
            1 for v in scan["vulnerabilities"]
            if v["severity"] == "High"
        )

        medium_count = sum(
            1 for v in scan["vulnerabilities"]
            if v["severity"] == "Medium"
        )

        low_count = sum(
            1 for v in scan["vulnerabilities"]
            if v["severity"] == "Low"
        )

        scan["risk_breakdown"] = {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count
        }
        mark_progress("Network Scanner", 100)

    return render_template(
        "labs/scanner.html",
        scan=scan,
        ip_address=ip_address
    )
import random

import random

def simulated_scan(ip):

    last_octet = int(ip.split(".")[-1])
    
    profiles = [

        {
            "risk_level": "HIGH",
            "security_score": 42,

            "open_ports": [
                {"port": 21, "service": "FTP", "status": "Open", "severity": "Critical"},
                {"port": 3306, "service": "MySQL", "status": "Open", "severity": "High"},
                {"port": 8080, "service": "Proxy", "status": "Open", "severity": "Medium"},
            ],

            "vulnerabilities": [
                {"severity": "Critical", "name": "Anonymous FTP Access", "cve": "CVE-2023-1234"},
                {"severity": "High", "name": "Exposed MySQL Service", "cve": "CVE-2022-5678"},
                {"severity": "Medium", "name": "Open Proxy Service", "cve": "CVE-2021-9999"},
            ],

            "recommendations": [
                "Disable anonymous FTP access",
                "Restrict MySQL to localhost",
                "Close unnecessary ports",
                "Enable firewall filtering",
                "Perform regular patch management"
            ]
        },

        {
            "risk_level": "MEDIUM",
            "security_score": 68,

            "open_ports": [
                {"port": 80, "service": "HTTP", "status": "Open", "severity": "Medium"},
                {"port": 443, "service": "HTTPS", "status": "Open", "severity": "Low"},
                {"port": 22, "service": "SSH", "status": "Open", "severity": "Medium"},
            ],

            "vulnerabilities": [
                {"severity": "Medium", "name": "Directory Listing Enabled", "cve": "CVE-2022-5671"},
                {"severity": "Low", "name": "Weak TLS Configuration", "cve": "CVE-2021-1234"},
            ],

            "recommendations": [
                "Disable directory browsing",
                "Upgrade TLS configuration",
                "Restrict SSH access"
            ]
        },

        {
            "risk_level": "LOW",
            "security_score": 91,

            "open_ports": [
                {"port": 443, "service": "HTTPS", "status": "Open", "severity": "Low"},
            ],

            "vulnerabilities": [
                {"severity": "Low", "name": "Minor Information Disclosure", "cve": "CVE-2020-1111"},
            ],

            "recommendations": [
                "Continue routine patching",
                "Review security logs regularly"
            ]
        }

    ]

    selector = last_octet % 3

    print("SELECTOR =", selector)

    if selector == 0:
        profile = profiles[0]      

    elif selector == 1:
        profile = profiles[1]      

    else:
        profile = profiles[2]                

    profile["target"] = ip

    return profile


@main_bp.route("/labs/malware-analysis", methods=["GET", "POST"])
@login_required
def malware_lab():
    analysis = None
    if request.method == "POST" and "sample" in request.files:
        analysis = analyze_upload(request.files["sample"], current_app.config["UPLOAD_FOLDER"])
        mark_progress("Malware Analysis", 100 if analysis["risk"] != "High" else 65)
    return render_template("labs/malware.html", analysis=analysis)


@main_bp.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    questions = QuizQuestion.query.all()
    result = None
    if request.method == "POST":
        score = 0
        feedback = []
        for q in questions:
            answer = request.form.get(f"q_{q.id}")
            correct = answer == q.correct_option
            score += int(correct)
            feedback.append({"question": q.question, "correct": correct, "explanation": q.explanation})
        percentage = (score / max(len(questions), 1)) * 100
        db.session.add(QuizResult(user_id=current_user.id, score=score, total_questions=len(questions), percentage=percentage))
        db.session.commit()
        mark_progress("Quiz Arena", int(percentage))
        if percentage >= 80:
            award_badge(current_user, "Cyber Defender")
        result = {"score": score, "total": len(questions), "percentage": percentage, "feedback": feedback}
    return render_template("quiz.html", questions=questions, result=result)


@main_bp.route("/ctf", methods=["GET", "POST"])
@login_required
def ctf():
    challenges = CTFChallenge.query.all()
    message = None
    if request.method == "POST":
        challenge = CTFChallenge.query.get_or_404(int(request.form["challenge_id"]))
        flag = request.form.get("flag", "").strip()
        correct = flag == challenge.flag
        db.session.add(CTFSubmission(user_id=current_user.id, challenge_id=challenge.id, submitted_flag=flag, is_correct=correct))
        db.session.commit()
        message = "Correct flag submitted." if correct else "Flag rejected. Review the challenge hint and try again."
        if correct:
            mark_progress("CTF", challenge.points)
            award_badge(current_user, "CTF Champion")
    solved = {s.challenge_id for s in current_user.ctf_submissions if s.is_correct}
    return render_template("ctf.html", challenges=challenges, solved=solved, message=message)


@main_bp.route("/profile")
@login_required
def profile():
    completed, quiz_score, badge_count, security_score = dashboard_metrics(current_user)
    return render_template("profile.html", completed=completed, quiz_score=quiz_score, badge_count=badge_count, security_score=security_score)


@main_bp.route("/report")
@login_required
def report():
    _, _, _, security_score = dashboard_metrics(current_user)
    path = generate_user_report(current_user, current_app.config["REPORT_FOLDER"], security_score)
    return send_file(path, as_attachment=True)

