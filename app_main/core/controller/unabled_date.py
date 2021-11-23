import datetime
from ..model.unabled_date import unabled_date as model


def add(request, user_id):
    if not request.json:
        raise Exception('Request is not json')

    request_json = request.json

    date = get_or_error(request_json, 'date')

    repetitive = get(request_json, 'repetitive')

    if repetitive:
        # Must be a weekday
        validate_weekday(date)

    all_day = get(request_json, 'all_day')
    if not all_day:
        # Must have a start and end hour
        start_hour = get_or_error(request_json, 'start_hour')
        start_hour = datetime.datetime.strptime(start_hour, '%H:%M').time()
        end_hour = get_or_error(request_json, 'end_hour')
        end_hour = datetime.datetime.strptime(end_hour, '%H:%M').time()
        print(start_hour, end_hour)

    return get_all()


def get_all():
    return model.query.all()


def validate_weekday(weekday):
    week_list = ['monday', 'tuesday', 'wednesday',
                 'thursday', 'friday', 'saturday', 'sunday']
    if type(weekday) is list:
        for day in weekday:
            if day.lower() not in week_list:
                raise Exception(f"{day} is not a valid weekday")
        return
    if weekday.lower() not in week_list:
        raise Exception(f"{weekday} is not a valid weekday")


def get(json, attribute):
    try:
        return json[attribute]

    except Exception:
        return None


def get_or_error(json, attribute):
    try:
        return json[attribute]

    except Exception:
        raise Exception(f"{attribute} is required")
