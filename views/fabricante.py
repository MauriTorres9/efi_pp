from flask import Blueprint, request, jsonify, make_response
from app import db
from models import Fabricante
from schemas import FabricanteSchema
from flask_jwt_extended import jwt_required, get_jwt

fabricante_bp = Blueprint('fabricantes', __name__)

@fabricante_bp.route('/fabricantes', methods=['GET', 'POST'])
@jwt_required()
def fabricantes():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = FabricanteSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_fabricante = Fabricante(
                nombre=data.get('nombre'),  # Cambia "nombre_fabricante" a "nombre"
                pais_id=data.get('pais_id')  # Relación con País
            )
            db.session.add(nuevo_fabricante)
            db.session.commit()
            return make_response(FabricanteSchema().dump(nuevo_fabricante), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear fabricantes"}), 403

    fabricantes = Fabricante.query.all()
    return FabricanteSchema().dump(fabricantes, many=True)

@fabricante_bp.route('/fabricantes/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_fabricante(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar fabricantes"}), 403

    fabricante = Fabricante.query.get(id)
    if not fabricante:
        return jsonify({"Mensaje": "Fabricante no encontrado"}), 404

    db.session.delete(fabricante)
    db.session.commit()
    return jsonify({"Mensaje": "Fabricante eliminado con éxito"}), 200


