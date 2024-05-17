from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from .categoria_model import CategoriaNaoEncontrada, listar_categorias, categoria_por_id, adicionar_categoria, atualizar_categoria, excluir_categoria
categoria = Blueprint('categoria',__name__)

@categoria.route('/categoria', methods=["GET"])
def main():
  return 'Rotas para categoria'

@categoria.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = listar_categorias()
    print(categorias)
    return render_template("categorias.html", categorias=categorias)

@categoria.route('/categorias/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    try:
        categoria = categoria_por_id(id_categoria)
        return render_template('categoria_id.html', categoria=categoria)
    except CategoriaNaoEncontrada:
        return jsonify({'message': 'categoria não encontrado'}), 404

@categoria.route('/categorias/adicionar', methods=['GET'])
def adicionar_categoria_page():
    return render_template('criarCategoria.html')

@categoria.route('/categorias', methods=['POST'])
def create_categoria():
    nome = request.form['nome']
    novo_categoria = {'nome': nome}
    adicionar_categoria(novo_categoria)
    return redirect(url_for('categoria.get_categorias'))

@categoria.route('/categorias/<int:id_categoria>/editar', methods=['GET'])
def editar_categoria_page(id_categoria):
    try:
        categoria = categoria_por_id(id_categoria)
        return render_template('categoria_update.html', categoria=categoria)
    except CategoriaNaoEncontrada:
        return jsonify({'message': 'categoria não encontrado'}), 404

@categoria.route('/categorias/<int:id_categoria>', methods=['PUT'])
def update_categoria(id_categoria):
        print("Dados recebidos no formulário:", request.form)
        try:
            categoria = categoria_por_id(id_categoria)
            nome = request.form['nome']
            categoria['nome'] = nome
            atualizar_categoria(id_categoria, categoria)
            return redirect(url_for('categoria.get_categoria', id_categoria=id_categoria))
        except CategoriaNaoEncontrada:
            return jsonify({'message': 'categoria não encontrado'}), 404
   
@categoria.route('/categorias/<int:id_categoria>', methods=['DELETE'])
def delete_categoria(id_categoria):
        try:
            excluir_categoria(id_categoria)
            return redirect(url_for('categoria.get_categorias'))
        except CategoriaNaoEncontrada:
            return jsonify({'message': 'categoria não encontrado'}), 404
