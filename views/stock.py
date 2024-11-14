from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Stock
from schemas import StockSchema
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

stock_bp = Blueprint('stocks', __name__)

@stock_bp.route('/stocks', methods=['GET', 'POST'])
@jwt_required()
def stocks():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            errors = StockSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)

            nuevo_stock = Stock(
                cantidad=data.get('cantidad'),
                ubicacion=data.get('ubicacion'),
                equipo_id=data.get('equipo_id'),
            )
            db.session.add(nuevo_stock)
            db.session.commit()
            return make_response(StockSchema().dump(nuevo_stock), 201)
        else:
            return jsonify({"Mensaje": "Solo el administrador puede crear o actualizar stocks"}), 403

    stocks = Stock.query.all()
    return StockSchema().dump(stocks, many=True)

@stock_bp.route('/stocks/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_stock(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para eliminar stocks"}), 403

    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"Mensaje": "Stock no encontrado"}), 404

    db.session.delete(stock)
    db.session.commit()
    return jsonify({"Mensaje": "Stock eliminado con éxito"}), 200
