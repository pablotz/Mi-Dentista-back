import flask

route = flask.Blueprint("user_route", __name__, url_prefix="/user")


@route.route('/add', methods=['POST'])
def add():
    return flask.jsonify({
        "estado": "holaaaaa"
    })
