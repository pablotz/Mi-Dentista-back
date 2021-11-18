from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func

from app_main.core.model.access_code import access_code
from app_main.core.model.services import services
from app_main.core.model.system_user import system_user


class appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_date_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        system_user.id), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        services.id), nullable=False)
