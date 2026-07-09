from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .entities import (  # noqa: E402,F401
    ActivityLog,
    Badge,
    CTFChallenge,
    CTFSubmission,
    PhishingExample,
    QuizQuestion,
    QuizResult,
    User,
    UserBadge,
    UserProgress,
)

