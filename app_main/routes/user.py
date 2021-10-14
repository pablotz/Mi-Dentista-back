import flask
from flask.globals import request
from ..core.controller import system_user as controller

route = flask.Blueprint("user_route", __name__, url_prefix="/user")


@route.route('/add', methods=['POST'])
def add():
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        new_user = controller.add(flask.request)

        status = "OK"
        message = "User registered"
        content = new_user

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})
