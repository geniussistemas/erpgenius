from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import pyodbc

from flask_login import LoginManager
from urllib.parse import quote_plus

app = Flask(__name__)


app.config['SECRET_KEY'] = 'dd997d7de1f0126d366e265aa617938f'

parametros = (
        # Driver que será utilizado na conexão
        'DRIVER={ODBC Driver 13 for SQL Server};'
        # IP ou nome do servidor.
        'SERVER=189.69.195.101\SQLEXPRESS;'
        # Porta
        'PORT=1433;'
        # Banco que será utilizado.
        'DATABASE=ERPGenius;'
        # Nome de usuário.
        'UID=sa;'
        # Senha/Token.
        'PWD=325014')

parametrosgenius = (
        # Driver que será utilizado na conexão
        'DRIVER={ODBC Driver 13 for SQL Server};'
        # IP ou nome do servidor.
        'SERVER=localhost\SQLEXPRESS;'
        # Porta
        'PORT=1433;'
        # Banco que será utilizado.
        'DATABASE=automacao;'
        # Nome de usuário.
        'UID=sa;'
        # Senha/Token.
        'PWD=325014')


url_db = quote_plus(parametros)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=%s' % url_db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql:///?odbc_connect=%s' % url_db

database = SQLAlchemy(app)

sql = """
        EXEc usp_seleciona_tabelas @parametro = ?
        """

#conexao = pyodbc.connect(parametrosgenius)
#print("conexao bem sucedida")

#cursor = conexao.cursor()
#cursor.execute(sql, 'AT')

#tabelas = cursor.fetchall()
#descricao = cursor.description

#print(tabelas)
#print(descricao)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.needs_refresh_message_category = 'alert-info'


from erpgenius import routes



