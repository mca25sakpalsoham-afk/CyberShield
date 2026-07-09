import os

class Config:
    SECRET_KEY = "dev-cybershield-change-me"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:system@localhost:3306/cybershield"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    REPORT_FOLDER = os.path.join(os.path.dirname(__file__), "reports")

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"