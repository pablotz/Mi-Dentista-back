# from typing_extensions import Required
from werkzeug.wrappers import request
from ..model.services import services as model
from ...connection import db
from werkzeug.security import generate_password_hash
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def addServices(request):
    if not request.json:
        raise Exception('JSON no encontrado. El JSON es necesario para procesar la petición.')
    
    requestJSON = request.json
    name = obtener_validar(requestJSON, 'name')
    duration = obtener_validar(requestJSON, 'duration')
    price = obtener_validar(requestJSON, 'price')
    create_by = obtener_validar(requestJSON, 'create_by')
    create_at = obtener_validar(requestJSON, 'create_at')
    
    new_service = model(
            name=name,
            duration=duration,
            price=price,
            create_by=create_by,
            create_at=create_at,
            estatus=1
    )
    
    try:
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Servicio agregado exitosamente'}
    except Exception as es:
            raise Exception('Ocurrio un error')
        
def editServices(request):
    if not request.json:
        raise Exception('JSON no encontrado. El JSON es necesario para procesar la petición.')
    
    requestJSON = request.json
    id = obtener_validar(requestJSON, 'id')
    name = obtener_validar(requestJSON, 'name')
    duration = obtener_validar(requestJSON, 'duration')
    price = obtener_validar(requestJSON, 'price')
    create_by = obtener_validar(requestJSON, 'create_by')
    create_at = obtener_validar(requestJSON, 'create_at')
    
    edit_service = model(
            id=id, 
            name=name,
            duration=duration,
            price=price,
            create_by=create_by,
            create_at=create_at,
            estatus=1
    )
    try:
        editService =  db.session.query(model).filter(model.id == edit_service.id).first()
        editService.name = edit_service.name
        editService.duration = edit_service.duration
        editService.price = edit_service.price
        editService.create_by = edit_service.create_by
        editService.create_at = edit_service.create_at
        db.session.add(editService)
        db.session.commit()
        return {'message': 'Servicio editado exitosamente'}
    except Exception as es:
            raise Exception('Ocurrio un error')
    
    
def getServices():
    return model.query.all()
    

def obtener_validar(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")
    
def findServices(_id):
    if _id == 0:
        return model.query.all()
    else:
        return db.session.query(model).filter(model.id == _id).first()

def desactivateStatus(_id):
    if _id == 0:
        return "El id no puede ser cero"
    desactivateService = db.session.query(model).filter(model.id == _id).first()
    desactivateService.estatus = 0
    db.session.add(desactivateService)
    db.session.commit()
    return True

def activateStatus(_id):
    if _id == 0:
        return "El id no puede ser cero"
    activateServices = db.session.query(model).filter(model.id == _id).first()
    activateServices.estatus = 1
    db.session.add(activateServices)
    db.session.commit()
    return True