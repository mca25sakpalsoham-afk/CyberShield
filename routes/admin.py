from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from models import db
from models.entities import (
    CTFChallenge,
    PhishingExample,
    QuizQuestion,
    QuizResult,
    User,
    UserProgress
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@admin_required
def dashboard():
    users = User.query.count()
    questions = QuizQuestion.query.count()
    ctf = CTFChallenge.query.count()
    avg_quiz = db.session.query(func.avg(QuizResult.percentage)).scalar() or 0
    recent_users = User.query.order_by(User.created_at.desc()).limit(8).all()
    return render_template("admin/dashboard.html", users=users, questions=questions, ctf=ctf, avg_quiz=avg_quiz, recent_users=recent_users)


@admin_bp.route("/users")
@admin_required
def users():

    users = User.query.order_by(User.created_at.desc()).all()

    user_stats = []

    for user in users:

        completed_modules = len(
            [p for p in user.progress if p.completed]
        )

        total_modules = 8

        if user.progress:
            lab_score = (
                sum(p.score for p in user.progress)
                / len(user.progress)
            )
        else:
            lab_score = 0

        completion_factor = completed_modules / total_modules

        security_score = round(
            lab_score * completion_factor
        )

        user_stats.append({
            "user": user,
            "completed": completed_modules,
            "total": total_modules,
            "security_score": security_score
        })

    return render_template(
        "admin/users.html",
        user_stats=user_stats
    )

@admin_bp.route("/user/<int:user_id>")
@admin_required
def user_details(user_id):

    user = User.query.get_or_404(user_id)

    completed_modules = len(
        [p for p in user.progress if p.completed]
    )

    total_modules = 8

    if user.progress:
        lab_score = (
            sum(p.score for p in user.progress)
            / len(user.progress)
        )
    else:
        lab_score = 0

    completion_factor = completed_modules / total_modules

    cyber_readiness = round(
        lab_score * completion_factor
    )

    return render_template(
        "admin/user_details.html",
        user=user,
        cyber_readiness=cyber_readiness,
        completed_modules=completed_modules,
        total_modules=total_modules
    )


@admin_bp.route("/quiz", methods=["GET", "POST"])
@admin_required
def quiz_questions():
    if request.method == "POST":
        db.session.add(QuizQuestion(
            question=request.form["question"],
            option_a=request.form["option_a"],
            option_b=request.form["option_b"],
            option_c=request.form["option_c"],
            option_d=request.form["option_d"],
            correct_option=request.form["correct_option"],
            explanation=request.form["explanation"],
        ))
        db.session.commit()
        flash("Quiz question added.", "success")
        return redirect(url_for("admin.quiz_questions"))
    return render_template("admin/quiz.html", questions=QuizQuestion.query.all())


@admin_bp.route("/phishing", methods=["GET", "POST"])
@admin_required
def phishing():
    if request.method == "POST":
        db.session.add(PhishingExample(
            subject=request.form["subject"],
            sender=request.form["sender"],
            body=request.form["body"],
            is_phishing=request.form["is_phishing"] == "true",
            explanation=request.form["explanation"],
        ))
        db.session.commit()
        flash("Phishing example added.", "success")
        return redirect(url_for("admin.phishing"))
    return render_template("admin/phishing.html", examples=PhishingExample.query.all())


@admin_bp.route("/ctf", methods=["GET", "POST"])
@admin_required
def ctf():
    if request.method == "POST":
        db.session.add(CTFChallenge(
            title=request.form["title"],
            description=request.form["description"],
            difficulty=request.form["difficulty"],
            points=int(request.form["points"]),
            flag=request.form["flag"],
        ))
        db.session.commit()
        flash("CTF challenge added.", "success")
        return redirect(url_for("admin.ctf"))
    return render_template("admin/ctf.html", challenges=CTFChallenge.query.all())
