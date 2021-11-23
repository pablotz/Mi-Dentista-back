from re import search
from flask import app
from sqlalchemy.sql.expression import extract, false, true
from ..model.appointment import appointment as model
from ..controller.services import findServices
from ...connection import db
from datetime import datetime, timedelta, date


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


def get_valid_hours(request):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')

    requestJSON = request.json
    request_date = get_or_error(requestJSON, 'date')

    request_service = get_or_error(requestJSON, 'service')
    service = findServices(request_service)

    if service is None:
        raise Exception('Service not found')

    result = db.engine.execute(
        f"""
    SELECT
        a.start_date_time - INTERVAL {service.duration} MINUTE AS start_date_time,
        a.start_date_time + INTERVAL s.duration MINUTE AS end_date_time
    FROM
        appointment AS a
            INNER JOIN
        services AS s ON a.service_id = s.id
    WHERE
        a.status = 1
            AND a.start_date_time <= '{request_date} 23:59:59'
            AND a.start_date_time >='{request_date} 00:00:00'
    ORDER BY a.start_date_time ASC;
                """)

    raw_data = result.fetchall()
    return clear_hours(raw_data, service.duration, request_date)


def clear_hours(raw_data, duration, request_date):
    start_labour_hour = datetime.strptime(
        f'{request_date} 07:00:00', '%Y-%m-%d %H:%M:%S')
    end_labour_hour = datetime.strptime(
        f'{request_date} 20:00:00', '%Y-%m-%d %H:%M:%S') - timedelta(minutes=duration)

    time_lapse = 5
    data = []

    if len(raw_data) == 0:
        # Return all hours
        return divide_into_timelapse([[start_labour_hour, end_labour_hour]], time_lapse)

    last_index = len(raw_data) - 1
    for idx, row in enumerate(raw_data):
        if last_index == 0:
            if row[0] >= start_labour_hour:
                data.append([start_labour_hour, row[0]])
            data.append([row[1], end_labour_hour])
            break
        if idx == 0:
            if row[0] > start_labour_hour:
                diff_s = (row[0] - start_labour_hour).total_seconds()
                diff_m = divmod(diff_s, 60)[0]

                if diff_m > duration:
                    data.append([start_labour_hour, row[0]])

        else:
            end_date_time = raw_data[idx - 1][1]
            start_date_time = row[0]

            diff_s = (start_date_time - end_date_time).total_seconds()
            diff_m = divmod(diff_s, 60)[0]

            if diff_m >= duration:
                data.append([end_date_time, start_date_time])

            if idx == last_index:
                diff_s = (end_labour_hour - row[1]).total_seconds()
                diff_m = divmod(diff_s, 60)[0]

                if diff_m >= duration:
                    data.append([row[1], end_labour_hour])

    return divide_into_timelapse(data, time_lapse)


def divide_into_timelapse(data, duration):
    result = []

    for d in data:
        start = d[0]
        end = d[1]
        while start < end:
            if start < end:
                result.append(start.strftime('%H:%M'))
            start += timedelta(minutes=duration)

    return result


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
            a.status = 1
                AND a.start_date_time <= '{new_datetime}'
                AND a.start_date_time + INTERVAL s.duration MINUTE > '{new_datetime}';
                """)
    row = result.fetchone()

    return row is None


def get_or_error(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")


def cancel(request):
    if not request.json:
        raise Exception(
            'JSON not found. The JSON is necessary to process the request.')

    requestJSON = request.json
    id = get_or_error(requestJSON, 'id')

    appointment = model.query.filter(model.id == id).first()
    if appointment is None:
        raise Exception('Appointment not found')

    if appointment.status != 1:
        raise Exception('Appointment already canceled')

    appointment.status = 0
    db.session.commit()
    return None


def get_by_user(user_id):
    result = model.query.filter(
        model.user_id == user_id, model.status == 1).all()

    data = []
    for row in result:
        dic = row.__dict__
        del dic['_sa_instance_state']
        del dic['user_id']
        dic['service'] = findServices(row.service_id).name
        data.append(dic)

    return data


def get_by_month(request):
    if not request.json:
        raise Exception(
            'JSON not found. The JSON is necessary to process the request.')

    requestJSON = request.json
    month = get_or_error(requestJSON, 'month')
    year = datetime.now().year

    result = model.query.filter(
        extract('month', model.start_date_time) == month).filter(
            extract('year', model.start_date_time) == year).all()

    data = []
    for row in result:
        dic = row.__dict__
        del dic['_sa_instance_state']
        del dic['user_id']
        dic['service'] = findServices(row.service_id).name
        data.append(dic)

    return data


def get_by_period(request):
    if not request.json:
        raise Exception(
            'JSON not found. The JSON is necessary to process the request.')

    requestJSON = request.json
    start_date = get_or_error(requestJSON, 'start_date')
    end_date = get_or_error(requestJSON, 'end_date')

    if start_date > end_date:
        raise Exception('Start date must be less than end date')

    result = model.query.filter(
        model.start_date_time >= start_date,
        model.start_date_time <= f'{end_date} 23:59:59').all()

    data = []
    for row in result:
        dic = row.__dict__
        del dic['_sa_instance_state']
        del dic['user_id']
        dic['service'] = findServices(row.service_id).name
        data.append(dic)

    return data
