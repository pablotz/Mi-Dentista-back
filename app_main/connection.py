from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

db = SQLAlchemy()

DB_CONFIG = "./dbconfig.json"
