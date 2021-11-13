import flask
from flask.globals import request
from flask.json import jsonify
from ..core.controller import payment_method as PaymentMethodController

route = flask.Blueprint("paymentmethod_route", __name__, url_prefix="/payment_method")

@route.route('/add', methods=['POST'])
def add():
    # return controller.add(flask.request)
    status = ''
    message = ''
    content = ''
    try:
        new_service = PaymentMethodController.addPaymentMethod(flask.request)

        status = "OK"
        message = "Payment Method registered"
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
        edit_service = PaymentMethodController.editPayMethod(flask.request)
        status = "OK"
        message = "Payment method edited"
        content = edit_service

    except Exception as error:
        status = "ERROR"
        message = str(error)
        content = None

    return flask.jsonify({"status": status, "message": message, "content": content})


@route.route("/get", methods=['GET'])
def getAllPaymentMethods():
    payment_methods  = PaymentMethodController.getPayMethod()
    payment_methods_json = []
    for payment_method in payment_methods:
        services_dictionary = payment_method.__dict__
        del services_dictionary['_sa_instance_state']
        payment_methods_json.append(services_dictionary)
    return jsonify(payment_methods_json)


@route.route("/find", methods=['GET'])
def FindPaymentMethod():
    estado = "OK"
    mensaje = "Información consultada correctamente"
    try:
        print(request.json)
        print("_id" not in request.json)
        
        if "_id" not in request.json or request.json["_id"] == 0:
            
            payment_methods = PaymentMethodController.findPayMethod(0)
            if len(payment_methods)>0:
                services_json = []
                for payment_method in payment_methods:
                    payment_method_dictionary = payment_method.__dict__
                    del payment_method_dictionary['_sa_instance_state']
                    services_json.append(payment_method_dictionary)
                return jsonify(services_json)
        else:
            payment_method = PaymentMethodController.findPayMethod(request.json["_id"])
            if payment_method is None:
                    return jsonify({
                        "estado" : "ADVERTENCIA",
                        "mensaje": "No se encontro un payment_method con el id especificado"
                    })
            payment_method_dictionary = payment_method.__dict__
            del payment_method_dictionary['_sa_instance_state']
            return jsonify(payment_method_dictionary)

    except Exception as e:
        estado = "ERROR"
        mensaje = "Ha ocurrido un error! Por favor verificalo con un administrador"
        return jsonify({
            "estado"  : estado,
            "mensaje" : mensaje,
            "excepcion": str(e)
        })

@route.route("/desactivate", methods=['POST'])
def desactivatePaymentMethod():
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error"
            })
        if PaymentMethodController.desactivateStatus(request.json["_id"]):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El Metodo de pago a sido desactivado correctamente"
            })




@route.route("/activate", methods=['POST'])
def activatePaymentMethod():
        if "_id" not in request.json:
            return jsonify({
                "estado" : "ADVERTENCIA",
                "mensaje": "Ha ocurrido un error"
            })
        if PaymentMethodController.activateStatus(request.json["_id"]):
            return jsonify({
                "estado" : "OK",
                "mensaje": "El Metodo de pago a sido activado correctamente"
            })
