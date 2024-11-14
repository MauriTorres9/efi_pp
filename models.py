from app import db

class Pais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre


class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre


class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)

    def __str__(self) -> str:
        return f"{self.tipo}: {self.descripcion}"


class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=False)
    
    pais = db.relationship('Pais', backref=db.backref('fabricantes', lazy=True))

    def __str__(self):
        return self.nombre 




class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(100), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)

    fabricante = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))

    def __str__(self) -> str:
        return self.nombre_modelo


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    equipo = db.relationship('Equipo', backref=db.backref('stocks', lazy=True))



class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)

    def __str__(self) -> str:
        return self.nombre


class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('accesorios', lazy=True))

    def __str__(self) -> str:
        return self.tipo



class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    anio_fabricacion = db.Column(db.Integer)

    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('equipos', lazy=True))
    proveedor = db.relationship('Proveedor', backref=db.backref('equipos', lazy=True))

    def __str__(self) -> str:
        return self.nombre


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username
