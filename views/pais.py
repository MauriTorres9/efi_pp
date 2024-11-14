from flask import Blueprint, request, jsonify, make_response
from app import db
from models import Pais
from schemas import PaisSchema
from flask_jwt_extended import jwt_required, get_jwt

pais_bp = Blueprint('paises', __name__)

@pais_bp.route('/paises', methods=['GET', 'POST'])
@jwt_required()
def paises():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = PaisSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_pais = Pais(
                nombre=data.get('nombre')
            )
            db.session.add(nuevo_pais)
            db.session.commit()
            return make_response(PaisSchema().dump(nuevo_pais), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevos países"}), 403

    paises = Pais.query.all()
    return PaisSchema().dump(paises, many=True)


@pais_bp.route('/paises/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_pais(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar países"}), 403

    pais = Pais.query.get(id)
    if not pais:
        return jsonify({"Mensaje": "País no encontrado"}), 404

    db.session.delete(pais)
    db.session.commit()
    return jsonify({"Mensaje": "País eliminado con éxito"}), 200

@pais_bp.route('/paises/<int:id>/edit', methods=['PUT'])
@jwt_required()
def editar_pais(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para editar países"}), 403

    pais = Pais.query.get(id)
    if not pais:
        return jsonify({"Mensaje": "País no encontrado"}), 404

    data = request.get_json()
    errors = PaisSchema().validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    pais.nombre = data.get('nombre', pais.nombre)  # Actualiza solo el nombre si se proporciona
    db.session.commit()

    return jsonify({"Mensaje": "País actualizado con éxito", "pais": PaisSchema().dump(pais)}), 200
