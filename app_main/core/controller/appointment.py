from re import search
from flask import app
from sqlalchemy.sql.expression import false, true
from ..model.appointment import appointment as model
from ..controller.services import findServices
from ...connection import db
from datetime import datetime


def add(request, user_id):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')

    requestJSON = request.json

    start_date_time = datetime.fromisoformat(
        f"{requestJSON['date']} {requestJSON['hour']}")
    if not validate_availability(start_date_time):
        raise Exception('Appointment is not available')
    service_id = get_or_error(requestJSON, 'service')

    new_appointment = model(
        user_id=user_id,
        service_id=service_id,
        start_date_time=start_date_time
    )
    db.session.add(new_appointment)
    db.session.commit()

    return search(new_appointment.id)


def search(id):
    appointment = model.query.filter(model.id == id).first()

    dic = appointment.__dict__
    del dic['_sa_instance_state']
    dic['service'] = findServices(appointment.service_id).name
    return dic


def validate_availability(new_datetime):
    result = db.engine.execute(
        f"""
        SELECT 
            a.start_date_time,
            a.start_date_time + INTERVAL s.duration MINUTE AS end_date_time
        FROM
            appointment AS a
                INNER JOIN
            services AS s ON a.service_id = s.id
        WHERE
            a.start_date_time <= '{new_datetime}'
                AND a.start_date_time + INTERVAL s.duration MINUTE > '{new_datetime}';
                """)
    row = result.fetchone()

    return row is None


def get_or_error(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")
