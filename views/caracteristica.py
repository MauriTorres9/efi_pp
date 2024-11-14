from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Caracteristica
from schemas import CaracteristicaSchema
from flask_jwt_extended import jwt_required, get_jwt

caracteristica_bp = Blueprint('caracteristicas', __name__)

@caracteristica_bp.route('/caracteristicas', methods=['GET', 'POST'])
@jwt_required()
def caracteristicas():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = CaracteristicaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nueva_caracteristica = Caracteristica(
                tipo=data.get('tipo'),
                descripcion=data.get('descripcion')
            )
            db.session.add(nueva_caracteristica)
            db.session.commit()
            return make_response(CaracteristicaSchema().dump(nueva_caracteristica), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevas características"}), 403
    
    caracteristicas = Caracteristica.query.all()
    return CaracteristicaSchema().dump(caracteristicas, many=True)

@caracteristica_bp.route('/caracteristicas/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_caracteristica(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar características"}), 403

    caracteristica = Caracteristica.query.get(id)
    if not caracteristica:
        return jsonify({"Mensaje": "Característica no encontrada"}), 404

    db.session.delete(caracteristica)
    db.session.commit()
    return jsonify({"Mensaje": "Característica eliminada con éxito"}), 200
