import flask
from ..core.controller import unabled_date as controller
from ..core.decorators import session

route = flask.Blueprint("unabled_date_route", __name__,
                        url_prefix="/unabled_date")


@route.route('/add', methods=['POST'])
@session.validate_access([1])
def add(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        new_unabled_date = controller.add(flask.request, current_user_id)

        status = "OK"
        message = "Unabled date registered"
        content = new_unabled_date

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route('get_all', methods=['GET'])
@session.validate_access([1, 0])
def get_all(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        unabled_dates = controller.get_all()

        status = "OK"
        message = "Unabled dates retrieved"
        content = unabled_dates

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route('/delete', methods=['POST'])
@session.validate_access([1])
def delete(current_user_id):
    status = ''
    message = ''
    content = ''
    try:
        date = flask.request.json['date']
        unabled_date = controller.delete(date)

        status = "OK"
        message = "Unabled date deleted"
        content = unabled_date

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})
