from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Categoria
from schemas import CategoriaSchema
from flask_jwt_extended import jwt_required, get_jwt


categoria_bp = Blueprint('categorias', __name__)

@categoria_bp.route('/categorias', methods=['GET', 'POST'])
@jwt_required()
def categorias():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = CategoriaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_categoria = Categoria(
                nombre=data.get('nombre'),
            )
            db.session.add(nuevo_categoria)
            db.session.commit()
            return make_response(CategoriaSchema().dump(nuevo_categoria), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevos categorias"}), 403
    
    categorias = Categoria.query.all()
    return CategoriaSchema().dump(categorias, many=True)

@categoria_bp.route('/categorias/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_categoria(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar categorias"}), 403

    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"Mensaje": "Categoria no encontrado"}), 404

    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"Mensaje": "Categoria eliminado con éxito"}), 200
