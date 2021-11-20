import flask
from ..core.controller import appointment as controller
from ..core.decorators import session

route = flask.Blueprint("appointment_route", __name__,
                        url_prefix="/appointment")


@route.route('/add', methods=['POST'])
@session.validate_access(0)
def add(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        new_appointment = controller.add(flask.request, current_user_id)

        status = "OK"
        message = "Appointment registered"
        content = new_appointment

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route('/get_valid_hours', methods=['POST'])
@session.validate_access(0)
def get_valid_hours(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        available_hours = controller.get_valid_hours(flask.request)

        status = "OK"
        message = "Appointment registered"
        content = available_hours

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route('/cancel', methods=['POST'])
@session.validate_access(0)
def cancel(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        appointment = controller.cancel(flask.request)

        status = "OK"
        message = "Appointment canceled"
        content = appointment

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route('/get_by_user', methods=['POST'])
@session.validate_access(0)
def get_by_user(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        appointments = controller.get_by_user(current_user_id)

        status = "OK"
        message = "Appointments retrieved"
        content = appointments

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})
