from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func

from app_main.core.model.system_user import system_user

class payment_method(db.Model):
    
    __tablename__ = 'payment_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_by = db.Column(db.Integer, db.ForeignKey(system_user.id), nullable=true)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now(), nullable=False)
    estatus = db.Column(db.Integer, nullable=False)