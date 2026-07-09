from models import db
from models.entities import Badge, UserBadge


def award_badge(user, badge_name):
    badge = Badge.query.filter_by(name=badge_name).first()
    if not badge:
        return False
    existing = UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first()
    if existing:
        return False
    db.session.add(UserBadge(user_id=user.id, badge_id=badge.id))
    db.session.commit()
    return True

