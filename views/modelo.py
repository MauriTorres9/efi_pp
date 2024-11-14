from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Modelo
from schemas import ModeloSchema
from flask_jwt_extended import jwt_required, get_jwt


modelo_bp = Blueprint('modelos', __name__)

@modelo_bp.route('/modelos', methods=['GET', 'POST'])
@jwt_required()
def modelos():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = ModeloSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_modelo = Modelo(
                nombre_modelo=data.get('nombre_modelo'),
                fabricante_id=data.get('fabricante_id')
            )
            db.session.add(nuevo_modelo)
            db.session.commit()
            return make_response(ModeloSchema().dump(nuevo_modelo), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevos modelos"}), 403
    
    modelos = Modelo.query.all()
    return ModeloSchema().dump(modelos, many=True)

@modelo_bp.route('/modelos/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_modelo(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar modelos"}), 403

    modelo = Modelo.query.get(id)
    if not modelo:
        return jsonify({"Mensaje": "Modelo no encontrado"}), 404

    db.session.delete(modelo)
    db.session.commit()
    return jsonify({"Mensaje": "Modelo eliminado con éxito"}), 200
