class Veiculo():
    
    def __init__(self, id, marca, modelo, ano, cor, preco_compra, preco_venda, status):
        self.id = id
        self. marca = marca
        self. modelo = modelo
        self.ano = ano
        self.cor = cor
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.status = status

    def get_id(self):
        return self.id

    def to_JSON(self):
        return {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'ano': self.ano,
            'cor': self.cor,
            'preco_compra': self.preco_compra,
            'preco_venda': self.preco_venda,
            'status': self.status
        }