
# Importamos la clase Flask del módulo flask
import flask
import flask_cors
from .core.model.system_user import system_user
from .connection import db, DB_CONFIG

from .routes import user


def create_app():
    # Creamos una instancia de Flask
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    cors = flask_cors.CORS(app, resources={
        r"/*": {
            "origins": "*"
        }
    })
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.register_blueprint(user.route)

    app.config.from_json(DB_CONFIG)

    db.init_app(app)

    @app.before_first_request
    def create_all():
        db.create_all()

    return app
