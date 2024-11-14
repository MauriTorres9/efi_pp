from .auth_view import auth_bp
from .accesorio import accesorio_bp
from .caracteristica import caracteristica_bp
from .categoria import categoria_bp
from .equipo import equipo_bp
from .fabricante import fabricante_bp
from .marca import marca_bp
from .modelo import modelo_bp
from .pais import pais_bp
from .proveedor import proveedor_bp
from .stock import stock_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(accesorio_bp)
    app.register_blueprint(caracteristica_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(equipo_bp)
    app.register_blueprint(fabricante_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(pais_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(stock_bp)