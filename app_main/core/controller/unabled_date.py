import datetime
from ...connection import db
from sqlalchemy.sql.expression import true
from ..model.unabled_date import unabled_date as model


def add(request, user_id):
    if not request.json:
        raise Exception('Request is not json')

    request_json = request.json

    date = get_or_error(request_json, 'date')
    validate_is_unique_date(date)

    if type(date) is list:
        for day in date:
            unabled_date = model(date=day, created_by=user_id)
            db.session.add(unabled_date)
    else:
        unabled_date = model(date=date, created_by=user_id)
        db.session.add(unabled_date)

    db.session.add(unabled_date)
    db.session.commit()
    return "Ok"


def get_all():
    # Get all unabled_date sorted by date
    unabled_dates = model.query.order_by(model.date).all()

    dic = [unabled_date.__dict__ for unabled_date in unabled_dates]
    for i in range(len(dic)):
        del dic[i]['_sa_instance_state']
        del dic[i]['created_at']
        del dic[i]['created_by']
    return dic


def delete(date):
    unabled_date = model.query.filter(model.date == date).first()
    db.session.delete(unabled_date)
    db.session.commit()
    return "Ok"


def search(id):
    unabled_date = model.query.filter(model.id == id).first()

    dic = unabled_date.__dict__
    del dic['_sa_instance_state']
    return dic


def is_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except Exception:
        raise Exception(f"{date} is not a valid date")


def validate_is_unique_date(date):
    if type(date) is list:
        for day in date:
            is_date(day)
            if model.query.filter(model.date == day).first():
                raise Exception(f"{day} is already in use")
        return
    is_date(date)
    if model.query.filter(model.date == date).first():
        raise Exception(f"{date} is already in use")


def get_or_error(json, attribute):
    try:
        return json[attribute]

    except Exception:
        raise Exception(f"{attribute} is required")
