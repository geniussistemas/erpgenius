from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired,Length, Email,EqualTo, ValidationError
from erpgenius.models import LoginSite
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados')
    botao_submit_login = SubmitField('Fazer login')

    def validate_email(self, email):
         usuario = LoginSite.query.filter_by(email_usuario=email.data).first()
         if not usuario:
            raise ValidationError('Email não cadastrado')


class FormCadUsuario(FlaskForm):
    nome = StringField('Nome de Usuario', validators=[DataRequired(), Length(6, 50)])
    email = StringField('E-mail ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha', message="As senhas não são iguais")])
    #confirmacao_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_cadusuario = SubmitField('Enviar Dados')

    def validate_email(self, email):
        usuario = LoginSite.query.filter_by(email_usuario=email.data).first()
        if usuario:
            print (usuario)
            raise ValidationError('Email ja cadastrado!. Cadastre-se com outro email.')


class FormCadUsuarioERP(FlaskForm):
    nome = StringField('Nome de Usuario', validators=[DataRequired(), Length(6, 50)])
    email = StringField('E-mail ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo(senha)])
    botao_submit_cadusuario = SubmitField('Enviar Dados')


class FormEditarPerfilERP(FlaskForm):
    nome = StringField('Nome de Usuario', validators=[DataRequired(), Length(6, 50)])
    email = StringField('E-mail ', validators=[DataRequired(), Email()])
    contato = StringField('Contato')
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    cadastro_usuarios = BooleanField('Cadastra/Altera Usuarios ERP')
    cadastro_unidades = BooleanField('Cadastra/Altera Unidades ERP')
    cadastro_tabelas = BooleanField('Cadastra/Altera Tabelas de Preço')
    cadastro_mensalista = BooleanField('Cadastra/Altera Mensalistas')
    emite_relatorio = BooleanField('Gera Relatórios')
    botao_submit_EditarPerfilERP = SubmitField('Enviar Dados')

class FormAlterarSenha(FlaskForm):
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_FormAlteraSenha = SubmitField('Alterar Senha')

class FormCadUnidadeERP(FlaskForm):
    sigla = StringField('Descrição ', validators=[DataRequired(), Length(1, 20)])
    URLUnidade = StringField('Endereço do servidor ', validators=[DataRequired()])
    UsuarioSQl = StringField('Usuario do database', validators=[DataRequired()])
    SenhaSQl = StringField('Senha do database', validators=[DataRequired()])
    botao_submit_cadunidade = SubmitField('Enviar Dados')


