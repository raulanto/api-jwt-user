from app import db
from datetime import datetime

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def check_role(self, role_name):
        return self.role.name == role_name

class SesionUsuario(db.Model):
    __tablename__ = "sesion_usuario"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    usuario = db.relationship("User", backref="sesiones")
    fecha_hora_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_hora_salida = db.Column(db.DateTime, nullable=True)
    token_jti = db.Column(db.String(36), unique=True, nullable=False)

    def lis_json(self):
        return {
            "id": self.id,
            "usuario": self.usuario.nombre,
            "fecha_hora_entrada": self.fecha_hora_entrada,
            "fecha_hora_salida": self.fecha_hora_salida,
        }