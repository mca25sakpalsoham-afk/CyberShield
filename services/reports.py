import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from utils import ist_time

def generate_user_report(user, report_folder, security_score):
    os.makedirs(report_folder, exist_ok=True)
    filename = f"cybershield_report_user_{user.id}.pdf"
    path = os.path.join(report_folder, filename)
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("CyberShield User Progress Report", styles["Title"]),
        Paragraph(
            f"Generated: {ist_time(datetime.utcnow()).strftime('%Y-%m-%d %H:%M IST')}",
            styles["Normal"]
        ),
        Spacer(1, 16),
        Paragraph(f"Name: {user.name}", styles["Heading3"]),
        Paragraph(f"Email: {user.email}", styles["Normal"]),
        Paragraph(f"Security Score: {security_score}", styles["Normal"]),
        Spacer(1, 16),
    ]
    rows = [["Module", "Completed", "Score"]]
    for item in user.progress:
        rows.append([item.module_name, "Yes" if item.completed else "No", str(item.score)])
    if len(rows) == 1:
        rows.append(["No modules completed yet", "-", "-"])
    table = Table(rows, colWidths=[220, 100, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([Paragraph("Completed Modules", styles["Heading2"]), table, Spacer(1, 16)])
    badges = ", ".join(ub.badge.name for ub in user.badges) or "No badges earned yet"
    story.append(Paragraph(f"Badges: {badges}", styles["Normal"]))
    if user.quiz_results:
        latest = user.quiz_results[-1]
        story.append(Paragraph(f"Latest Quiz Performance: {latest.score}/{latest.total_questions} ({latest.percentage:.1f}%)", styles["Normal"]))
    doc.build(story)
    return path

