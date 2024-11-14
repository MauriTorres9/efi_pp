from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Marca
from schemas import MarcaSchema
from flask_jwt_extended import jwt_required, get_jwt

marca_bp = Blueprint('marcas', __name__)

@marca_bp.route('/marcas', methods=['GET', 'POST'])
@jwt_required()
def marcas():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = MarcaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nueva_marca = Marca(nombre=data.get('nombre'))
            db.session.add(nueva_marca)
            db.session.commit()
            return make_response(MarcaSchema().dump(nueva_marca), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevas marcas"}), 403
    
    marcas = Marca.query.all()
    return MarcaSchema().dump(marcas, many=True)


@marca_bp.route('/marcas/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_marca(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar marcas"}), 403

    marca = Marca.query.get(id)
    if not marca:
        return jsonify({"Mensaje": "Marca no encontrada"}), 404

    db.session.delete(marca)
    db.session.commit()
    return jsonify({"Mensaje": "Marca eliminada con éxito"}), 200
