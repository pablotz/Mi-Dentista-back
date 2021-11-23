import flask
from flask.globals import request
from ..core.controller import system_user as controller
from ..core.decorators import session

route = flask.Blueprint("user_route", __name__, url_prefix="/user")


@route.route('/add', methods=['POST'])
@session.validate_access([1])
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


@route.route("/get", methods=['GET'])
@session.validate_access([1])
def getAllUsers():
    users = controller.getUser()
    users_json = []
    for user in users:
        users_dictionary = user.__dict__
        del users_dictionary['_sa_instance_state']
        users_json.append(users_dictionary)
    return flask.jsonify(users_json)



@route.route('/edit', methods=['POST'])
@session.validate_access([1])
def edit():
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        edit_user = controller.edit(flask.request)

        status = "OK"
        message = "user Edited"
        content = edit_user

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route("/desactivate", methods=['POST'])
@session.validate_access([1])
def desactivate():
    if "_id" not in request.json:
        return flask.jsonify({
            "estado": "ADVERTENCIA",
            "mensaje": "Ha ocurrido un error"
        })
    if controller.desactivate(request.json["_id"]):
        return flask.jsonify({
            "estado": "OK",
            "mensaje": "El usuario desactivado correctamente"
        })


@route.route("/activate", methods=['POST'])
@session.validate_access([1])
def activate():
    if "_id" not in request.json:
        return flask.jsonify({
            "estado": "ADVERTENCIA",
            "mensaje": "Ha ocurrido un error"
        })
    if controller.activate(request.json["_id"]):
        return flask.jsonify({
            "estado": "OK",
            "mensaje": "El usuario activado correctamente"
        })