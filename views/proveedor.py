from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Proveedor, Equipo
from schemas import ProveedorSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

proveedor_bp = Blueprint('proveedores', __name__)

@proveedor_bp.route('/proveedores', methods=['GET', 'POST'])
@jwt_required()
def proveedores():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == "POST":
        if administrador:
            data = request.get_json()
            errors = ProveedorSchema().validate(data)

            if errors:
                return make_response(jsonify(errors), 400)  # Retorna errores con código 400
            
            nuevo_proveedor = Proveedor(
                nombre=data.get('nombre'),
                contacto=data.get('contacto')
            )
            db.session.add(nuevo_proveedor)
            db.session.commit()
            return make_response(ProveedorSchema().dump(nuevo_proveedor), 201)  # Retorna el nuevo proveedor con código 201
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear nuevos proveedores"}), 403

    proveedores = Proveedor.query.all()
    return ProveedorSchema().dump(proveedores, many=True)

@proveedor_bp.route('/proveedores/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_proveedor(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar proveedores"}), 403

    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return jsonify({"Mensaje": "Proveedor no encontrado"}), 404

    # Verificar si el proveedor está siendo utilizado por algún equipo
    equipos_asociados = Equipo.query.filter_by(proveedor_id=id).all()
    if equipos_asociados:
        return jsonify({"Mensaje": "No se puede eliminar el proveedor porque está asociado a uno o más equipos"}), 400

    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"Mensaje": "Proveedor eliminado con éxito"}), 200
