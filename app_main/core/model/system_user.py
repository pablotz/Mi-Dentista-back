from app_main.connection import db


class system_user(db.Model):

    __tablename__ = "system_user"
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_status = db.Column(db.Integer, nullable=False)
    user_role = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
