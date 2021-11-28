from ..model.system_user import system_user as model
from ...connection import db
from werkzeug.security import generate_password_hash
from .access_code import validate as validate_access_code
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def add(request):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')

    requestJSON = request.json
    name = get_or_error(requestJSON, 'name')
    lastName = get_or_error(requestJSON, 'lastName')
    email = get_or_error(requestJSON, 'email')
    phone = get(requestJSON, 'phone')
    password = get_or_error(requestJSON, 'password')
    role = get_or_error(requestJSON, 'role')

    access_code = None
    if(role == "admin"):
        role = 1
    elif(role == "assistant"):
        role = 2
    else:
        role = 0
        access_code = get_or_error(requestJSON, 'access_code')
        validate_access_code(access_code)
    check(email)

    new_user = model(
        user_name=name,
        last_name=lastName,
        email=email,
        user_password=generate_password_hash(password, method='sha256'),
        phone=phone,
        access_code=access_code,
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


def editMe(request, user_id):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')
    print(user_id)
    requestJSON = request.json

    name = get_or_error(requestJSON, 'name')
    lastName = get_or_error(requestJSON, 'lastName')
    email = get_or_error(requestJSON, 'email')
    phone = get(requestJSON, 'phone')

    edit_user = model(
        user_name=name,
        last_name=lastName,
        email=email,
        phone=phone
    )
    try:
        editUser = db.session.query(model).filter(model.id == user_id).first()
        editUser.user_name = edit_user.user_name
        editUser.last_name = edit_user.last_name
        editUser.email = edit_user.email
        editUser.phone = edit_user.phone
        db.session.add(editUser)
        db.session.commit()

        return {'message': 'usuario editado exitosamente'}
    except Exception as es:
        raise Exception('Ocurrio un error', es)


def edit(request):
    if not request.json:
        raise Exception(
            'JSON no encontrado. El JSON es necesario para procesar la petición.')

    requestJSON = request.json
    id = get_or_error(requestJSON, 'id')
    name = get_or_error(requestJSON, 'name')
    lastName = get_or_error(requestJSON, 'lastName')
    email = get_or_error(requestJSON, 'email')
    phone = get(requestJSON, 'phone')
    password = get(requestJSON, 'password')
    #create_by = obtener_validar(requestJSON, 'create_by')

    edit_user = model(
        id=id,
        user_name=name,
        last_name=lastName,
        email=email,
        phone=phone,
    )
    try:
        editUser = db.session.query(model).filter(
            model.id == edit_user.id).first()
        editUser.user_name = edit_user.user_name
        editUser.last_name = edit_user.last_name
        editUser.email = edit_user.email
        editUser.phone = edit_user.phone

        if password is not None:
            editUser.user_password = generate_password_hash(
                password, method='sha256')
        db.session.add(editUser)
        db.session.commit()

        return {'message': 'usuario editado exitosamente'}
    except Exception as es:
        raise Exception('Ocurrio un error', es)


def desactivate(_id, user_id):
    if _id == 0:
        return "El id no puede ser cero"
    desactivateUser = db.session.query(model).filter(model.id == _id).first()
    desactivateUser.user_status = 0
    db.session.add(desactivateUser)
    db.session.commit()
    return True


def activate(_id, user_id):
    if _id == 0:
        return "El id no puede ser cero"
    activateUser = db.session.query(model).filter(model.id == _id).first()
    activateUser.user_status = 1
    db.session.add(activateUser)
    db.session.commit()
    return True


def getUser(user_id):
    return model.query.all()


def findMe(user_id):
    if user_id == 0:
        return model.query.all()
    else:
        return db.session.query(model).filter(model.id == user_id).first()


def get_or_error(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")


def get(json, atributo):
    try:
        return json[atributo]

    except Exception:
        return None


def check(email):
    if(not re.fullmatch(regex, email)):
        raise Exception("Invalid Email")


def buscar_id(id):

    system_user = model.query.filter(model.id == id).first()

    dic = system_user.__dict__
    del dic['_sa_instance_state']
    del dic['user_password']

    return dic
