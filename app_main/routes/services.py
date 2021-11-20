import flask
from flask.globals import request
from flask.json import jsonify
from ..core.controller import services as servicesController
from ..core.decorators import session
import datetime

route = flask.Blueprint("services_route", __name__, url_prefix="/services")


@route.route('/add', methods=['POST'])
@session.validate_access(1)
def add(current_user_id):
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        new_service = servicesController.addServices(flask.request, current_user_id)

        status = "OK"
        message = "Services registered"
        content = new_service

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})




@route.route('/edit', methods=['POST'])
@session.validate_access(1)
def edit(current_user_id):
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        edit_service = servicesController.editServices(flask.request, current_user_id)

        status = "OK"
        message = "Services Edited"
        content = edit_service

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})




@route.route("/get", methods=['GET'])
@session.validate_access(1)
def getAllServices(current_user_id):
    #controlador con su json 
    services  = servicesController.getServices()
    services_json = []
    for service in services:
        id = service.id
        format = servicesController.minutesConvert(id)
        formats_json = []
        if format is None:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "No se encontro un service con el id especificado"
                })
        else:
            format = servicesController.minutesConvert(id)
            formats_json = []
            if format is None:
                    return jsonify({
                        "estado" : "ADVERTENCIA",
                        "mensaje": "No se encontro un service con el id especificado"
                    })
            minutos = format.duration
            if minutos <= 59:
                hrs = minutos/60
                second = hrs*3600
                min = str(datetime.timedelta(seconds = second))
                xd = min[0:4]    
                formats_json.append({
                    'duration': xd,
                    'format': 'min.'
                })
            else:
                hrs = minutos/60
                second = hrs*3600
                horas = str(datetime.timedelta(seconds = second))
                xd = horas[0:4]
                formats_json.append({
                    'duration' : xd,
                    'format': 'hrs.'
                })
        services_dictionary = service.__dict__
        del services_dictionary['_sa_instance_state']
        services_dictionary['systemformat'] = formats_json
        services_json.append(services_dictionary)
    return jsonify(services_json)


@route.route("/find", methods=['GET'])
@session.validate_access(1)
def findServices(current_user_id):
    estado = "OK"
    mensaje = "Información consultada correctamente"
    try:
        print(request.json)
        print("_id" not in request.json)
        
        if "_id" not in request.json or request.json["_id"] == 0:
            print("test")
            services = servicesController.findServices(0)
            if len(services)>0:
                services_json = []
                for service in services:
                    service_dictionary = service.__dict__
                    del service_dictionary['_sa_instance_state']
                    services_json.append(service_dictionary)
                return jsonify(services_json)
        else:
            service = servicesController.findServices(request.json["_id"])
            if service is None:
                    return jsonify({
                        "estado" : "ADVERTENCIA",
                        "mensaje": "No se encontro un service con el id especificado"
                    })
            service_dictionary = service.__dict__
            del service_dictionary['_sa_instance_state']
            return jsonify(service_dictionary)

    except Exception as e:
        estado = "ERROR"
        mensaje = "Ha ocurrido un error! Por favor verificalo con un administrador"
        return jsonify({
            "estado"  : estado,
            "mensaje" : mensaje,
            "excepcion": str(e)
        })



@route.route("/desactivate", methods=['POST'])
@session.validate_access(1)
def desactivateServices(current_user_id):
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error"
            })
        if servicesController.desactivateStatus(request.json["_id"],current_user_id ):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El servicio desactivado correctamente"
            })




@route.route("/activate", methods=['POST'])
@session.validate_access(1)
def activateServices(current_user_id):
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error"
            })
        if servicesController.activateStatus(request.json["_id"], current_user_id):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El servicio activado correctamente"
            })
    

@route.route("/test2", methods=['GET'])
def newxd():
    estado = "OK"
    mensaje = "Información consultada correctamente"
    try:
        print(request.json)
        print("_id" not in request.json)
        
        if "_id" not in request.json or request.json["_id"] == 0:
            print("test")
        else:
            format = servicesController.minutesConvert(request.json["_id"])
            formats_json = []
            if format is None:
                    return jsonify({
                        "estado" : "ADVERTENCIA",
                        "mensaje": "No se encontro un service con el id especificado"
                    })
            minutos = format.duration
            if minutos <= 59:
                hrs = minutos/60
                second = hrs*3600
                min = str(datetime.timedelta(seconds = second))
                xd = min[0:4]    
                formats_json.append({
                    'duration': xd,
                    'format': 'min.'
                })
            else:
                hrs = minutos/60
                second = hrs*3600
                horas = str(datetime.timedelta(seconds = second))
                xd = horas[0:4]
                formats_json.append({
                    'duration' : xd,
                    'format': 'hrs.'
                })
            return jsonify(formats_json)
        
    except Exception as e:
        estado = "ERROR"
        mensaje = "Ha ocurrido un error! Por favor verificalo con un administrador"
        return jsonify({
            "estado"  : estado,
            "mensaje" : mensaje,
            "excepcion": str(e)
        })