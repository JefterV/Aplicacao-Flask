class CadastraJogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id      = id
        self.nome    = nome
        self.console = console
        self.categoria = categoria

class CadastraUsuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha