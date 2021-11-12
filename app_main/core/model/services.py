from sqlalchemy.sql.expression import true
from app_main.connection import db
from sqlalchemy.sql import func


class services(db.Model):
    
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    create_by = db.Column(db.String(50), nullable=False)
    create_at = db.Column(db.String(50), nullable=False)
    estatus = db.Column(db.Integer, nullable=False)
    
    
    
