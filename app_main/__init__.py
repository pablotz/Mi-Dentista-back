
# Importamos la clase Flask del módulo flask
import flask
from flask.json import JSONEncoder
from datetime import date
import flask_cors
from app_main.routes.login import login
from .core.model.system_user import system_user
from .connection import db, DB_CONFIG

from .routes import user, login, access_code, services, payment_method, appointment, unabled_date


# Custom datetime field format when using jsonify
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app():
    # Creamos una instancia de Flask
    app = flask.Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    flask_cors.CORS(app)
    cors = flask_cors.CORS(app, resources={
        r"/*": {
            "origins": "*"
        }
    })
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.register_blueprint(user.route)
    app.register_blueprint(login.route)
    app.register_blueprint(access_code.route)
    app.register_blueprint(services.route)
    app.register_blueprint(payment_method.route)
    app.register_blueprint(appointment.route)
    app.register_blueprint(unabled_date.route)

    app.config.from_json(DB_CONFIG)

    db.init_app(app)

    @app.before_first_request
    def create_all():
        db.create_all()

    return app
