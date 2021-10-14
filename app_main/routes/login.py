import jwt
import flask
import datetime
from flask.globals import request
from werkzeug.security import check_password_hash
from ..core.model.system_user import system_user as model

route = flask.Blueprint("login_route", __name__)


@route.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return flask.jsonify({
            "status": "ERROR",
            "message": "Unable to read data"
        })
    user_json = request.json
    user = model.query.filter_by(
        email=user_json["email"], user_status=1).first()

    if user and check_password_hash(user.user_password, user_json["user_password"]):
        expires_at = str(datetime.datetime.utcnow() +
                         datetime.timedelta(minutes=30))

        token = jwt.encode({'public_id': user.id, 'expires_at': expires_at},
                           flask.current_app.config['SECRET_KEY'])

        return flask.jsonify({
            "status": True,
            "expires_on": 1800,
            "token": token,
            "user": user.email
        })

    return flask.jsonify({
        "status": "ERROR",
        "message": "Data provided is wrong."
    })
