from models import CadastraJogo, CadastraUsuario

SQL_DELETA_JOGO = 'delete from JOGOS where ID_JOGO = %s'
SQL_JOGO_POR_ID = 'SELECT ID_JOGO, JOGO, CATEGORIA, CONSOLE from JOGOS where ID_JOGO = %s'
SQL_USUARIO_POR_ID = 'SELECT ID_USER, USUARIO, SENHA from USUARIO where USUARIO = %s'
SQL_ATUALIZA_JOGO = 'UPDATE JOGOS SET JOGO=%s, CATEGORIA=%s, CONSOLE=%s where ID_JOGO = %s'
SQL_BUSCA_JOGOS = 'SELECT ID_JOGO, JOGO, CATEGORIA, CONSOLE from JOGOS'
SQL_CRIA_JOGO = 'INSERT into JOGOS (JOGO, CATEGORIA, CONSOLE, ID_USER) values (%s, %s, %s, %s)'
SQl_NOVO_USUARIO = 'INSERT INTO USUARIO(USUARIO, SENHA) VALUES (%s, %s)'

class JogoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, jogo, idUser):
        cursor = self.__db.connection.cursor()

        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console, idUser))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return CadastraJogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def cadastraUsuario(self, user):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQl_NOVO_USUARIO, (user.nome, user.senha))
        user.id = cursor.lastrowid

        self.__db.connection.commit()
        return user

def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return CadastraJogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return CadastraUsuario(tupla[0], tupla[1], tupla[2])