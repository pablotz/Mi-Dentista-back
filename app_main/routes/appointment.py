import flask
from ..core.controller import appointment as controller
from ..core.decorators import session

route = flask.Blueprint("appointment_route", __name__,
                        url_prefix="/appointment")


@route.route('/test', methods=['POST'])
@session.validate_access(0)
def create(current_user_id):
    try:
        # access_code = controller.create_access_code(current_user_id)
        return flask.jsonify({
            "access_code": "access_code"
        })

    except Exception as e:
        return flask.jsonify({
            "status": "ERROR",
            "message": str(e)
        })
