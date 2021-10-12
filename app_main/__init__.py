
# Importamos la clase Flask del módulo flask
import flask
import flask_cors


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
    # app.register_blueprint(usuario_route)
    # app.register_blueprint(rol_usuario_route)
    # app.register_blueprint(inicio_sesion_route)
    # app.register_blueprint(venta_route)
    # app.register_blueprint(producto_route)
    # app.register_blueprint(ingrediente_route)

    # app.config.from_json(DB_CONFIGURACION)

    # db.init_app(app)

    # @app.before_first_request
    # def create_all():
    # db.create_all()

    return app
