from app import ma
from marshmallow import validates, ValidationError
from models import *

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()


class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()


class PaisSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pais

    id = ma.auto_field()
    nombre = ma.auto_field()


class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    id = ma.auto_field()
    nombre = ma.auto_field()


class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria

    id = ma.auto_field()
    nombre = ma.auto_field()


class CaracteristicaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristica

    id = ma.auto_field()
    tipo = ma.auto_field()
    descripcion = ma.auto_field()


class FabricanteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    id = ma.auto_field()
    nombre = ma.auto_field()
    pais_id = ma.auto_field()

    pais = ma.Nested(PaisSchema)



class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo

    id = ma.auto_field()
    nombre_modelo = ma.auto_field()
    fabricante_id = ma.auto_field()

    fabricante = ma.Nested(FabricanteSchema)


class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    id = ma.auto_field()
    nombre = ma.auto_field()
    contacto = ma.auto_field()


class AccesorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio

    id = ma.auto_field()
    tipo = ma.auto_field()
    modelo_id = ma.auto_field()  

    
    modelo = ma.Nested(ModeloSchema) 



class EquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    id = ma.auto_field()
    nombre = ma.auto_field()
    costo = ma.auto_field()
    anio_fabricacion = ma.auto_field()
    modelo_id = ma.auto_field()
    categoria_id = ma.auto_field()
    proveedor_id = ma.auto_field()

    modelo = ma.Nested(ModeloSchema)
    categoria = ma.Nested(CategoriaSchema)
    proveedor = ma.Nested(ProveedorSchema)

    @validates('anio_fabricacion')
    def validate_anio_fabricacion(self, value):
        if int(value) > 2024:
            return ValidationError("El año es superior al actual")


class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stock

    id = ma.auto_field()
    cantidad = ma.auto_field()  
    ubicacion = ma.auto_field()
    equipo_id = ma.auto_field()
    
    equipo = ma.Nested(EquipoSchema)



