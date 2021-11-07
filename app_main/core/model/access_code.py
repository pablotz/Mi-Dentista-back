from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func


class access_code(db.Model):

    id = db.Column(db.String(8), primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now())
    created_by = db.Column(db.Integer, nullable=False)
