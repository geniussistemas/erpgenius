from erpgenius import database, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_usuario(id_usuario):
    return LoginSite.query.get(int(id_usuario))


class LoginSite (database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    login_usuario = database.Column(database.String, nullable=False)
    senha_usuario = database.Column(database.String, nullable=False)
    status_usuario = database.Column(database.String, nullable=False)
    acessos_usuario = database.Column(database.String, nullable=False)
    foto_usuario = database.Column(database.String, nullable=False, default='default.jpg')
    email_usuario = database.Column(database.String, nullable=False)
    contato_usuario = database.Column(database.String, nullable=True)
   # data_criacao = database.Column(database.datetime, nullable=False, default=datetime.utcnow())

class Unidades_ERP(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    SiglaUnidade = database.Column(database.String, nullable=False)
    URLUnidade = database.Column(database.String, nullable=False)
    UsuarioSQL = database.Column(database.String, nullable=False)
    SenhaSql = database.Column(database.String, nullable=False)






