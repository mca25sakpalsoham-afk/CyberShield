from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from datetime import datetime, timedelta

def ist_now():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("student", "admin"), default="student", nullable=False)
    created_at = db.Column(db.DateTime, default=ist_now)

    progress = db.relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_results = db.relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")
    ctf_submissions = db.relationship("CTFSubmission", back_populates="user", cascade="all, delete-orphan")
    badges = db.relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    activity_logs = db.relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_name = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=ist_now, onupdate=ist_now)

    user = db.relationship("User", back_populates="progress")


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=ist_now)


class QuizResult(db.Model):
    __tablename__ = "quiz_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=ist_now)

    user = db.relationship("User", back_populates="quiz_results")


class PhishingExample(db.Model):
    __tablename__ = "phishing_examples"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_phishing = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.Text, nullable=False)


class CTFChallenge(db.Model):
    __tablename__ = "ctf_challenges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum("Easy", "Medium", "Hard"), default="Easy", nullable=False)
    points = db.Column(db.Integer, default=50)
    flag = db.Column(db.String(160), nullable=False)

    submissions = db.relationship("CTFSubmission", back_populates="challenge", cascade="all, delete-orphan")


class CTFSubmission(db.Model):
    __tablename__ = "ctf_submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("ctf_challenges.id"), nullable=False)
    submitted_flag = db.Column(db.String(160), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=ist_now)

    user = db.relationship("User", back_populates="ctf_submissions")
    challenge = db.relationship("CTFChallenge", back_populates="submissions")


class Badge(db.Model):
    __tablename__ = "badges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(80), default="shield-check")

    users = db.relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")


class UserBadge(db.Model):
    __tablename__ = "user_badges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey("badges.id"), nullable=False)
    awarded_at = db.Column(db.DateTime, default=ist_now)

    user = db.relationship("User", back_populates="badges")
    badge = db.relationship("Badge", back_populates="users")
    __table_args__ = (db.UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),)


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(180), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=ist_now)

    user = db.relationship("User", back_populates="activity_logs")

