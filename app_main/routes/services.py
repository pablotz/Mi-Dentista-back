import flask
from flask.globals import request
from flask.json import jsonify
from ..core.controller import services as servicesController

route = flask.Blueprint("services_route", __name__, url_prefix="/services")


@route.route('/add', methods=['POST'])
def add():
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        new_service = servicesController.addServices(flask.request)

        status = "OK"
        message = "Services registered"
        content = new_service

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})




@route.route('/edit', methods=['POST'])
def edit():
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        edit_service = servicesController.editServices(flask.request)

        status = "OK"
        message = "Services registered"
        content = edit_service

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})




@route.route("/get", methods=['GET'])
def getAllServices():
    services  = servicesController.getServices()
    services_json = []
    for service in services:
        services_dictionary = service.__dict__
        del services_dictionary['_sa_instance_state']
        services_json.append(services_dictionary)
    return jsonify(services_json)


@route.route("/find", methods=['GET'])
def findServices():
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
def desactivateServices():
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error, es necesario proporcionar un id de usuario para desactivar"
            })
        if servicesController.desactivateStatus(request.json["_id"]):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El servicio desactivado correctamente"
            })




@route.route("/activate", methods=['POST'])
def activateServices():
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error, es necesario proporcionar un id de usuario para desactivar"
            })
        if servicesController.desactivateStatus(request.json["_id"]):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El servicio activado correctamente"
            })
     