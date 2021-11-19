
from ..model.payment_method import payment_method as model
from ...connection import db

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def obtener_validar(json, atributo):
    try:
        return json[atributo]

    except Exception:
        raise Exception(f"Formato incorrecto en {atributo}")
    

def addPaymentMethod(request, user_id):
    if not request.json:
        raise Exception('JSON no encontrado. El JSON es necesario para procesar la petición.')
    
    requestJSON = request.json
    name = obtener_validar(requestJSON, 'name')
    # create_by = obtener_validar(requestJSON, 'create_by')
    
    new_service = model(
            name=name,
            create_by=user_id,
            estatus=1
    )
    
    try:
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Metodo de pago agregado exitosamente'}
    
    except Exception as es:
            raise Exception('Ocurrio un error')
        
def editPayMethod(request, user_id):
    if not request.json:
        raise Exception('JSON no encontrado. El JSON es necesario para procesar la petición.')
    
    requestJSON = request.json
    id = obtener_validar(requestJSON, 'id')
    name = obtener_validar(requestJSON, 'name')
    # create_by = obtener_validar(requestJSON, 'create_by')
    
    edit_PayMethod = model(
            id=id, 
            name=name,
            create_by=user_id,
            estatus=1
    )
    try:
        editPayMethod =  db.session.query(model).filter(model.id == edit_PayMethod.id).first()
        editPayMethod.name = edit_PayMethod.name
        editPayMethod.create_by = edit_PayMethod.create_by
        db.session.add(editPayMethod)
        db.session.commit()
        return {'message': 'El metodo de pago editado exitosamente'}
    except Exception as es:
            raise Exception('Ocurrio un error')
    
def getPayMethod():
    return model.query.all()

def findPayMethod(_id):
    if _id == 0:
        return model.query.all()
    else:
        return db.session.query(model).filter(model.id == _id).first()
    

def desactivateStatus(_id, user_id):
    if _id == 0:
        return "El id no puede ser cero"
    desactivatePayMethod = db.session.query(model).filter(model.id == _id).first()
    desactivatePayMethod.estatus = 0
    desactivatePayMethod.create_by = user_id
    db.session.add(desactivatePayMethod)
    db.session.commit()
    return True

def activateStatus(_id, user_id):
    if _id == 0:
        return "El id no puede ser cero"
    activatePayMethod = db.session.query(model).filter(model.id == _id).first()
    activatePayMethod.estatus = 1
    activatePayMethod.create_by = user_id
    db.session.add(activatePayMethod)
    db.session.commit()
    return True
    