import os
from main import app, session, redirect, url_for

def recupera_imagem(id):
    for NomeArquivo in os.listdir(app.config['UPLOAD_PATH']):    
        if NomeArquivo.split("-")[0] == str(id):
            return NomeArquivo
    return False

def deletar_arquivo(id):
    arquivo = recupera_imagem(id)
    if not arquivo:
        return False

    path = app.config["UPLOAD_PATH"]
    os.remove(os.path.join(path,arquivo))

def validaLogin():
    StringUser = 'usuario_logado'
    if StringUser not in session or session[StringUser] == None:
        return False
    return True