from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func

from app_main.core.model.access_code import access_code


class system_user(db.Model):

    __tablename__ = "system_user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=true)
    user_password = db.Column(db.String(88), nullable=False)
    user_status = db.Column(db.Integer, nullable=False, default=1)
    user_role = db.Column(db.Integer, nullable=False)
    access_code = db.Column(db.String(8), db.ForeignKey(
        access_code.id), nullable=true,)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
