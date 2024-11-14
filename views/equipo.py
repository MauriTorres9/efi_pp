from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Equipo, Marca, Categoria, Proveedor
from schemas import EquipoSchema, MarcaSchema, CategoriaSchema, ProveedorSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

equipo_bp = Blueprint('equipos', __name__)


@equipo_bp.route('/equipos', methods=['GET', 'POST'])
@jwt_required()
def equipos():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == "POST":
        if administrador:
            data = request.get_json()  # Solo el administrador puede crear un equipo
            errors = EquipoSchema().validate(data)

            if errors:
                return make_response(jsonify(errors), 400)  # Retorna errores con código 400
            
            nuevo_equipo = Equipo(
                nombre=data.get('nombre'),
                costo=data.get('costo'),
                anio_fabricacion=data.get('anio_fabricacion'),
                modelo_id=data.get('modelo_id'),
                categoria_id=data.get('categoria_id'),
                proveedor_id=data.get('proveedor_id')
            )
            db.session.add(nuevo_equipo)
            db.session.commit()
            return make_response(EquipoSchema().dump(nuevo_equipo), 201)  # Retorna el nuevo equipo con código 201
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevos equipos"}), 403

    equipos = Equipo.query.all()
    return EquipoSchema().dump(equipos, many=True)

@equipo_bp.route('/equipos/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_equipo(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para eliminar equipos"}), 403

    equipo = Equipo.query.get(id)
    if not equipo:
        return jsonify({"Mensaje": "Equipo no encontrado"}), 404

    db.session.delete(equipo)
    db.session.commit()
    return jsonify({"Mensaje": "Equipo eliminado con éxito"}), 200
