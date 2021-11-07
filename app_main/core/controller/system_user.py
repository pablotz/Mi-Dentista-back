from ..model.system_user import system_user as model
from ...connection import db
from werkzeug.security import generate_password_hash
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def add(request):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')

    requestJSON = request.json
    name = obtener_validar(requestJSON, 'name')
    lastName = obtener_validar(requestJSON, 'lastName')
    email = obtener_validar(requestJSON, 'email')
    password = obtener_validar(requestJSON, 'password')
    role = obtener_validar(requestJSON, 'role')

    if(role == "admin"):
        role = 1
    else:
        role = 0
    check(email)

    new_user = model(
        user_name=name,
        last_name=lastName,
        email=email,
        user_password=generate_password_hash(password, method='sha256'),
        user_role=role)
    db.session.add(new_user)

    try:
        db.session.commit()
    except Exception as e:
        if str(e).__contains__('Duplicate entry'):
            raise Exception('Email is unavailable.')
        else:
            raise Exception(
                'Hubo un error interno. Por favor consultelo con un técnico.')
    return buscar_id(new_user.id)


def obtener_validar(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")


def check(email):
    if(not re.fullmatch(regex, email)):
        raise Exception("Invalid Email")


def buscar_id(id):

    system_user = model.query.filter(model.id == id).first()

    dic = system_user.__dict__
    del dic['_sa_instance_state']
    del dic['user_password']

    return dic
