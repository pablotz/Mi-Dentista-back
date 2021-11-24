from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func

from app_main.core.model.system_user import system_user


class unabled_date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey(system_user.id))
