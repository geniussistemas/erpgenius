from flask import Flask, render_template, url_for, flash,redirect, request
from erpgenius.forms import FormLogin, FormCadUsuario, FormEditarPerfilERP, FormAlterarSenha, FormCadUnidadeERP
from erpgenius import app, database
from flask_login import login_user, logout_user, current_user, login_required
from erpgenius.models import LoginSite, Unidades_ERP


@app.route('/', methods=['GET', 'POST'])
def login():
    logout_user()
    form_login = FormLogin()

    if (form_login.validate_on_submit())and ('botao_submit_login' in request.form):
        usuario = LoginSite.query.filter_by(email_usuario=form_login.email.data).first()
        if usuario:
           senha= usuario.senha_usuario
           if senha != form_login.senha.data:
               flash(f'Senha inválida!', 'alert-danger')
               return render_template('login.html', form_login=form_login)
           if usuario.status_usuario == 'AP':
               flash(f'Usuario aguardando aprovação do Administrador!', 'alert-danger')
               return render_template('login.html', form_login=form_login)
           login_user(usuario, remember=form_login.lembrar_dados.data)
           flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
           par_next = request.args.get('next')
           if par_next:
               return redirect(par_next)
           else:
               return redirect(url_for('principal', tipo_usuario=usuario.acessos_usuario))
        else:
           flash(f'Falha no login, email ou senha invalidos!', 'alert-danger')
    return render_template('login.html', form_login=form_login)




@app.route('/principal')
@login_required
def principal():
    foto_perfil = url_for('static', filename='fotos/{}'.format(current_user.foto_usuario))
    print (foto_perfil)

    tipo_usuario= current_user.status_usuario
    lista_usuarios = LoginSite.query.all()
    lista_unidades = Unidades_ERP.query.all()

    for usuario in lista_usuarios:
       if usuario.status_usuario == 'AP':
         flash(f'Usuario do email {usuario.email_usuario} aguardando aprovação', 'alert-danger')

    return render_template('principal.html', foto_perfil=foto_perfil, tipo_usuario=tipo_usuario, lista_usuarios=lista_usuarios, lista_unidades=lista_unidades)

def atualizar_cursos(FormEditarPerfilERP):
    lista_cursos = []
    for campo in FormEditarPerfilERP:
        if 'cadastro_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/cadusuarioserp/<id_usuario>',methods=['GET', 'POST'])
@login_required
def cadusuarioserp(id_usuario):
    formEditarPerfilERP = FormEditarPerfilERP()
    usuario = LoginSite.query.filter_by(id=id_usuario).first()
    formEditarPerfilERP.nome.data = usuario.login_usuario
    formEditarPerfilERP.email.data = usuario.email_usuario
    formEditarPerfilERP.contato.data = usuario.contato_usuario
    if formEditarPerfilERP.validate_on_submit():
        usuario.email_usuario = formEditarPerfilERP.email.data
        usuario.login_usuario = formEditarPerfilERP.nome.data
        usuario.contato_usuario = formEditarPerfilERP.contato.data
        usuario.acessos_usuario = atualizar_cursos(formEditarPerfilERP)
        usuario.status_usuario = 'AT'
        database.session.commit()
        flash(f'Usuario {usuario.login_usuario} atualizado com Sucesso', 'alert-success')
        return redirect(url_for('editarusuarioerp'))
    elif request.method == "GET":
        if usuario.acessos_usuario:
             if 'Cadastra/Altera Usuarios ERP' in usuario.acessos_usuario:
                 formEditarPerfilERP.cadastro_usuarios.data = True
             if 'Cadastra/Altera Unidades ERP' in usuario.acessos_usuario:
                 formEditarPerfilERP.cadastro_unidades.data = True
             if 'Cadastra/Altera Tabelas ' in usuario.acessos_usuario:
                 formEditarPerfilERP.cadastro_tabelas.data = True
             if 'Cadastra/Altera Tabelas' in usuario.acessos_usuario:
                 formEditarPerfilERP.cadastro_mensalista.data = True
             if 'Power BI Impressionador' in usuario.acessos_usuario:
                 formEditarPerfilERP.emite_relatorio.data = True

    return render_template('cadusuarioserp.html', formEditarPerfilERP=formEditarPerfilERP)

@app.route('/editarunidadeerp')
@login_required
def editarunidadeerp():
    lista_unidades = Unidades_ERP.query.all()
    return render_template('editarunidadeerp.html', lista_unidades=lista_unidades)

@app.route('/cadunidadeerp',methods=['GET', 'POST'])
@login_required
def cadunidadeerp():
    formCadUnidadeERP=FormCadUnidadeERP()

    if (formCadUnidadeERP.validate_on_submit()) and ('botao_submit_cadunidade' in request.form):
            unidade = Unidades_ERP(SiglaUnidade=formCadUnidadeERP.sigla.data, URLUnidade=formCadUnidadeERP.URLUnidade.data, UsuarioSQL=formCadUnidadeERP.UsuarioSQl.data, SenhaSql=formCadUnidadeERP.SenhaSQl.data)
            database.session.add(unidade)
            database.session.commit()
            flash('Cadastro enviado com sucesso', 'alert-success')
            return redirect(url_for('editarunidadeerp'))
    return render_template('cadunidadeerp.html', formCadUnidadeERP=formCadUnidadeERP, altera=0)



@app.route('/cadusuario')
def cadusuario():
    return render_template('cadusuario.html', foto_perfil=foto_perfil)



@app.route('/editarusuarioerp', methods=['GET', 'POST'])
@login_required
def editarusuarioerp():
    #foto_perfil = url_for('static', filename='fotos/{}'.format(current_user.foto_usuario))
    #print (foto_perfil)
    lista_usuarios = LoginSite.query.all()
    return render_template('editarusuarioerp.html', lista_usuarios=lista_usuarios)

@app.route('/cadastrologin', methods=['GET', 'POST'])
def cadastrologin():
    form_CadUsuario = FormCadUsuario()
    if (form_CadUsuario.validate_on_submit()) and ('botao_submit_cadusuario' in request.form):
            usuario = LoginSite(login_usuario=form_CadUsuario.nome.data, email_usuario=form_CadUsuario.email.data, senha_usuario=form_CadUsuario.senha.data, acessos_usuario='AD', status_usuario='AP')
            database.session.add(usuario)
            database.session.commit()
            flash('Cadastro enviado com sucesso, aguarde confirmação para acesso.', 'alert-success')
            return redirect(url_for('login'))
    return render_template('cadastrologin.html', form_CadUsuario=form_CadUsuario)

@app.route('/alterasenha/<id_usuario>',methods=['GET', 'POST'])
def alterasenha(id_usuario):
    formAlterarSenha = FormAlterarSenha()
    usuario = LoginSite.query.filter_by(id=id_usuario).first()
    print(usuario.login_usuario, id_usuario)
    if formAlterarSenha.validate_on_submit():
        nome_usuario = usuario.login_usuario
        usuario.senha_usuario = formAlterarSenha.senha.data
        database.session.commit()
        flash(f'Senha Alterada com sucesso para o usuario {nome_usuario}.', 'alert-success')
        return redirect(url_for('editarusuarioerp'))
    return render_template('alterarsenha.html', formAlterarSenha=formAlterarSenha)


@app.route('/inativausuario/<id_usuario>',methods=['GET', 'POST'])
def invativausuario(id_usuario):
    formAlterarSenha = FormAlterarSenha()
    usuario = LoginSite.query.filter_by(id=id_usuario).first()
    print(usuario.login_usuario, id_usuario)
    if formAlterarSenha.validate_on_submit():
        nome_usuario = usuario.login_usuario
        usuario.senha_usuario = formAlterarSenha.senha.data
        database.session.commit()
        flash(f'Senha Alterada com sucesso para o usuario {nome_usuario}.', 'alert-success')
        return redirect(url_for('editarusuarioerp'))
    return render_template('alterarsenha.html', formAlterarSenha=formAlterarSenha)

@app.route('/alteracadastrounidade/<id_unidade>', methods=['GET', 'POST'])
def alteracadastrounidade(id_unidade):
    formCadUnidadeERP = FormCadUnidadeERP()
    unidade = Unidades_ERP.query.filter_by(id=id_unidade).first()
    formCadUnidadeERP.sigla.data = unidade.SiglaUnidade
    formCadUnidadeERP.URLUnidade.data = unidade.URLUnidade
    formCadUnidadeERP.UsuarioSQl.data = unidade.UsuarioSQL
    formCadUnidadeERP.SenhaSQl.data = unidade.SenhaSql
    return render_template('cadunidadeerp.html', formCadUnidadeERP=formCadUnidadeERP, altera=1)