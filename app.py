import os

from flask import Flask
from flask_login import LoginManager

from config import Config, LocalConfig
from models import db
from models.entities import Badge, CTFChallenge, PhishingExample, QuizQuestion, User
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.main import main_bp
from quiz_data import QUIZ_QUESTIONS
from phishing_data import PHISHING_EXAMPLES

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("DATABASE =", app.config["SQLALCHEMY_DATABASE_URI"])
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    with app.app_context():
        db.create_all()
        seed_data()
    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def seed_data():
    badges = [
        ("SQL Injection Master", "Understands SQL injection risk and parameterized defenses.", "database-zap"),
        ("Phishing Hunter", "Identifies phishing indicators with high accuracy.", "mail-warning"),
        ("Password Security Expert", "Builds strong passwords and recognizes weak patterns.", "key-round"),
        ("Cyber Defender", "Performs strongly in the cybersecurity quiz arena.", "shield-check"),
        ("CTF Champion", "Solves beginner capture-the-flag challenges.", "flag"),
    ]
    for name, description, icon in badges:
        if not Badge.query.filter_by(name=name).first():
            db.session.add(Badge(name=name, description=description, icon=icon))
    if not User.query.filter_by(email="admin@gmail.com").first():
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            role="admin"
        )

        admin.set_password("admin@123")
        db.session.add(admin)
    if QuizQuestion.query.count() == 0:
        for q in QUIZ_QUESTIONS:
            db.session.add(
                QuizQuestion(
                    question=q["question"],
                    option_a=q["option_a"],
                    option_b=q["option_b"],
                    option_c=q["option_c"],
                    option_d=q["option_d"],
                    correct_option=q["correct_option"],
                    explanation=q["explanation"]
                )
            )

    if PhishingExample.query.count() == 0:

        for p in PHISHING_EXAMPLES:

            db.session.add(
                PhishingExample(
                    subject=p["subject"],
                    sender=p["sender"],
                    body=p["body"],
                    is_phishing=p["is_phishing"],
                    explanation=p["explanation"]
                )
            )
        
    if CTFChallenge.query.count() == 0:
        db.session.add_all([
            CTFChallenge(title="Robots Recon", description="A training site exposes a comment saying the flag is CYBER{robots_are_clues}. Submit it.", difficulty="Easy", points=50, flag="CYBER{robots_are_clues}"),
            CTFChallenge(title="Hash Spotter", description="Identify the MD5 hash length: the flag is CYBER{md5_has_32_hex_chars}.", difficulty="Easy", points=60, flag="CYBER{md5_has_32_hex_chars}"),
            CTFChallenge(title="Header Hunter", description="Security headers matter. Submit CYBER{x_content_type_options}.", difficulty="Medium", points=90, flag="CYBER{x_content_type_options}"),
        ])
    db.session.commit()


app = create_app()

from utils import ist_time

app.jinja_env.globals.update(ist_time=ist_time)


if __name__ == "__main__":
    app.run(debug=True)

