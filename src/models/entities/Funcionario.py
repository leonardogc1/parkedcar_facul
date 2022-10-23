class Funcionario():
    
    def __init__(self, id, nome, registro, salario, funcao, senha, usuario):
        self.id = id
        self.nome = nome
        self.registro = registro
        self.salario = salario
        self.funcao = funcao
        self.senha = senha
        self.usuario = usuario

    def login(self, password_entrada):
        if(password_entrada == self.senha):
            return True
        return False
    
    def to_JSON(self):
       return {
            'id': self.id,
            'nome': self.nome,
            'registro': self.registro,
            'salario': self.salario,
            'funcao': self.funcao,
            'senha': self.senha,
            'usuario': self.usuario
       }