import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root2', passwd='root2', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE `jogoteca`;")
conn.commit()

criar_tabelas = '''
CREATE DATABASE JOGOTECA;
USE JOGOTECA;
CREATE TABLE USUARIO(
    ID_USER INT PRIMARY KEY AUTO_INCREMENT, 
    USUARIO VARCHAR(110),
    SENHA VARCHAR(32)
);

CREATE TABLE JOGOS(
    ID_JOGO INT PRIMARY KEY AUTO_INCREMENT, 
    JOGO VARCHAR(130),
    CATEGORIA VARCHAR(130),
    CONSOLE VARCHAR(130),
    ID_USER INT,
    FOREIGN KEY(ID_USER) 
    REFERENCES USUARIO (ID_USER)
);'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO JOGOTECA.USUARIO (USUARIO, SENHA) VALUES (%s, %s)',
      [
            ('Root', 'admin')
      ])

cursor.execute('select * from JOGOTECA.USUARIO')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO JOGOTECA.JOGOS (JOGO, CATEGORIA, CONSOLE, ID_USER) VALUES (%s, %s, %s, %s)',
      [
            ('God of War 4', 'Acao', 'PS4',1),
            ('NBA 2k18', 'Esporte', 'Xbox One',1),
            ('Rayman Legends', 'Indie', 'PS4',1),
            ('Super Mario RPG', 'RPG', 'SNES',1),
            ('Super Mario Kart', 'Corrida', 'SNES',1),
            ('Fire Emblem Echoes', 'Estrategia', '3DS',1),
      ])

cursor.execute('select * from JOGOTECA.JOGOS')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()