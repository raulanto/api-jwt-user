from app import db
from datetime import datetime

# Tabla intermedia para la relación many-to-many entre roles y permisos
role_permissions = db.Table('role_permissions',
                            db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
                            )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary=role_permissions, backref='role')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def check_role(self, role_name):
        return self.role.name == role_name

    def has_permission(self, permission_name):
        return any(p.name == permission_name for p in self.role.permissions) if self.role else False

    def list_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.name if self.role else None,
            "permissions": [perm.name for perm in self.role.permissions] if self.role else []
        }


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


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
