import flask
from ..core.controller import access_code as controller
from ..core.decorators import session

route = flask.Blueprint("access_code_route", __name__,
                        url_prefix="/access_code")


@route.route('/create', methods=['POST'])
@session.validate_access([1, 2])
def create(current_user_id):
    try:
        access_code = controller.create_access_code(current_user_id)
        return flask.jsonify({
            "access_code": access_code
        })

    except Exception as e:
        return flask.jsonify({
            "status": "ERROR",
            "message": str(e)
        })
