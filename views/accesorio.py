from flask import Blueprint, request, jsonify, make_response
from app import db
from models import Accesorio, Modelo
from schemas import AccesorioSchema
from flask_jwt_extended import jwt_required, get_jwt

accesorio_bp = Blueprint('accesorios', __name__)

@accesorio_bp.route('/accesorios', methods=['GET', 'POST'])
@jwt_required()
def accesorios():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = AccesorioSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_accesorio = Accesorio(
                tipo=data.get('tipo'),
                modelo_id=data.get('modelo_id') 
            )
            db.session.add(nuevo_accesorio)
            db.session.commit()
            return make_response(AccesorioSchema().dump(nuevo_accesorio), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear accesorios"}), 403

    accesorios = Accesorio.query.all()
    return AccesorioSchema().dump(accesorios, many=True)


@accesorio_bp.route('/accesorios/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_accesorio(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar accesorios"}), 403

    accesorio = Accesorio.query.get(id)
    if not accesorio:
        return jsonify({"Mensaje": "Accesorio no encontrado"}), 404

    db.session.delete(accesorio)
    db.session.commit()
    return jsonify({"Mensaje": "Accesorio eliminado con éxito"}), 200
