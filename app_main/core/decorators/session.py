from functools import wraps
from flask import request, jsonify, current_app
from ..model.system_user import system_user as model
import jwt
import datetime


def validate_access(required_role):
    def inner_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = None

            if 'Token' in request.headers:
                token = request.headers['Token']

            if not token:
                return jsonify({
                    "status": "ERROR",
                    "message": "Token not found."
                })

            try:
                jwt_data = jwt.decode(
                    token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

                expires_at = datetime.datetime.strptime(
                    jwt_data["expires_at"], '%Y-%m-%d %H:%M:%S.%f')

                if datetime.datetime.now() > expires_at:
                    return jsonify({
                        "status": "ERROR",
                        "message": "Token expired."
                    })
                user = model.query.filter_by(
                    id=jwt_data["public_id"], user_status=1).first()
                if not user:
                    return jsonify({
                        "status": "ERROR",
                        "message": "User not found."
                    })

                if user.user_role not in required_role:
                    return jsonify({
                        "status": "ERROR",
                        "message": "Access denied."
                    })
                return f(user.id, *args, **kwargs)

            except Exception as e:
                return jsonify({
                    "status": "ERROR",
                    "message": str(e)
                })
        return wrapped
    return inner_decorator
