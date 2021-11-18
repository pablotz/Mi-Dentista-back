import flask
from ..core.controller import appointment as controller
from ..core.decorators import session

route = flask.Blueprint("appointment_route", __name__,
                        url_prefix="/appointment")


@route.route('/add', methods=['POST'])
@session.validate_access(1)
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
