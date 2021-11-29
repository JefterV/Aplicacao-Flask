from flask import render_template, request, redirect, session, url_for, flash, send_from_directory
from dao import JogoDao, UsuarioDao
from models import CadastraJogo, CadastraUsuario
import time
from main import app, db
from helpers import recupera_imagem, deletar_arquivo, validaLogin

Jogo_Dao = JogoDao(db)
Usuario_Dao = UsuarioDao(db)

@app.route("/")
def index():
    StringUser = 'usuario_logado'
    lista = Jogo_Dao.listar()
    login = False
    if not validaLogin():
        login = False
    else:
        login = session[StringUser]

    return render_template('lista.html', titulo='Lista de jogos', jogos =lista, login=login)

@app.route("/novo")
def novo():
    StringUser = 'usuario_logado'
    if not validaLogin():
        return redirect(url_for('login', proxima=url_for('novo')))

    return render_template('novo.html', titulo='Novo Jogo')

@app.route("/editar/<int:id>")
def editar(id):
    if not validaLogin():
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    
    jogo = Jogo_Dao.busca_por_id(id)
    CapaJogo = recupera_imagem(id)

    if CapaJogo:
        pass
    else:
        CapaJogo = f'padrao.jpg'
    
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo, CapaJogo = CapaJogo)

@app.route('/deletar/<int:id>')
def deletar(id):
    if not validaLogin():
        return redirect(url_for('login', proxima='/'))

    Jogo_Dao.deletar(id)
    deletar_arquivo(id)
    flash("Jogo removido com sucesso.", "alert alert-success")
    return redirect(url_for('index'))

@app.route("/atualizar", methods=["POST",])
def atualizar():
    if not validaLogin():
        return redirect(url_for('login', proxima='/'))

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    arquivo = request.files['arquivo']
    id = request.form['id']
    timestamp = time.time()

    jogo = CadastraJogo(nome, categoria, console, id)
    jogo = Jogo_Dao.salvar(jogo,session["ID_USER"])

    deletar_arquivo(jogo.id)
    uploadPath = app.config['UPLOAD_PATH']
    arquivo.save(f"{uploadPath}/{str(jogo.id)}-{timestamp}.jpg")
    return redirect(url_for('index'))


@app.route('/criar', methods =["POST",])
def criar():
    if not validaLogin():
        return redirect(url_for('login', proxima='/'))

    nome      = request.form['nome']
    categoria = request.form['categoria']
    console   = request.form['console']

    jogo      = CadastraJogo(nome, categoria, console)
    jogo = Jogo_Dao.salvar(jogo,session["ID_USER"])

    uploadPath = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo = request.files['arquivo']
    if arquivo.filename:
        arquivo.save(f"{uploadPath}/{jogo.id}-{timestamp}.jpg")
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima   = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=["POST",])
def autenticar():
    LoginUser = Usuario_Dao.buscar_por_id(request.form['usuario'])
    UsuarioID     = request.form["usuario"]
    ProximaPagina = request.form['proxima']
    LembreDeMim   = request.form.get('LembreDeMim')
    
    StringUser    = "usuario_logado"
    if LoginUser:
        if LoginUser.senha == request.form['senha']:
            if LembreDeMim == "True":
                session.permanent = True

            session[StringUser] = request.form["usuario"]
            session["ID_USER"] = LoginUser.id

            flash('Olá, ' + request.form["usuario"] + f'! Bem vindo, login efetado com sucesso.', "alert alert-success")
            return redirect(ProximaPagina)
   
    flash(f'Usuario ou senha incorretos.', "alert alert-danger")
    return redirect(url_for("login", proxima=ProximaPagina))

@app.route('/cadastrarUser', methods=["POST","GET"])
def cadastrarUser():
    return render_template('cadastro.html')

@app.route('/validarCadastrarUser', methods=["POST",])
def validarCadastrarUser():
    usuario = request.form['Newusuario']
    senha01 = request.form['senha']
    senha02 = request.form['confirmSenha']
    ConcordoComTermos   = request.form.get('ConcordoComTermos')
    
    if ConcordoComTermos != "True":
        flash('Você não aceitou nossa politica de privacidade.', "alert alert-danger")
        return  redirect(url_for('cadastraUser'))

    if senha01 != senha02:
        flash('As senhas digitadas, são diferentes.', "alert alert-danger")
        return redirect(url_for('cadastraUser'))
        
    buscaUsuario = Usuario_Dao.buscar_por_id(usuario)
    if buscaUsuario != None:
        flash('O usuario digitado não está disponivel.', "alert alert-danger")
        return redirect(url_for('cadastraUser'))
    else:
        if len(usuario) <= 3:
            flash('O usuario digitado não está disponivel.', "alert alert-danger")
            return redirect(url_for('cadastraUser'))
        if len(senha01) <= 7:
            flash('Senha invalida', "alert alert-danger")
            return redirect(url_for('cadastraUser'))

        usuario = CadastraUsuario(None, usuario, senha01)
        novoUsuario = Usuario_Dao.cadastraUsuario(usuario)
        if novoUsuario.id:
            flash('Cadastro concluido com sucesso, faça login.', "alert alert-success")
            return redirect(url_for('login'))
        else:
            flash('O cadastro falhou, tente novamente mais tarde.')
            return redirect(url_for('index'))
    
   

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout concluido.", "alert alert-success")
    return redirect(url_for("index"))

@app.route('/uplouds/<nome_arquivo>')
def imagem(nome_arquivo):
    if not validaLogin():
        return redirect(url_for('login', proxima='/'))
    return send_from_directory('uploads', nome_arquivo)


