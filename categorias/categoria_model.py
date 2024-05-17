from config import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable = False)

    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}

class CategoriaNaoEncontrada(Exception):
    pass

def categoria_por_id(id_categoria):
    categoria = Categoria.query.get(id_categoria)
    if not categoria:
        raise CategoriaNaoEncontrada
    return categoria.to_dict()

def listar_categorias():
    categorias = Categoria.query.all()
    return [categoria.to_dict() for categoria in categorias]

def adicionar_categoria(categoria_data):
    novo_categoria = Categoria(nome=categoria_data['nome'])
    db.session.add(novo_categoria)
    db.session.commit()

def atualizar_categoria(id_categoria, novos_dados):
    categoria = Categoria.query.get(id_categoria)
    if not categoria:
        raise CategoriaNaoEncontrada
    categoria.nome = novos_dados['nome']
    db.session.commit()

def excluir_categoria(id_categoria):
    categoria = Categoria.query.get(id_categoria)
    if not categoria:
        raise CategoriaNaoEncontrada
    db.session.delete(categoria)
    db.session.commit()
