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
