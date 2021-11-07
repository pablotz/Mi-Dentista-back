from ...core.model.access_code import access_code as model
from ...core.model.system_user import system_user as model_user
from ...connection import db
import datetime
import uuid


def create_access_code(user_id):
    """
    Create a new access code.
    """
    access_code = str(uuid.uuid4())[:8]
    new_code = model(
        id=access_code,
        created_at=datetime.datetime.now(),
        created_by=user_id)

    db.session.add(new_code)
    db.session.commit()
    return access_code


def validate(access_code):
    """
    Validate an access code.
    """
    code = model.query.filter_by(id=access_code).first()
    if code is None:
        raise Exception("Invalid access code.")
    else:
        used = model_user.query.filter_by(access_code=access_code).first()

        if used is None:
            return True
        else:
            raise Exception("Invalid access code.")
