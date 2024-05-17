from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from categorias.categoria_model import listar_categorias, CategoriaNaoEncontrada, categoria_por_id
from sorvetes.sorvetes_model import (
    SorveteNaoEncontrado, adicionar_sorvete, listar_sorvetes_por_categoria, atualizar_sorvete, excluir_sorvete, listar_sorvetes, sorvete_por_id
)

sorvete = Blueprint('sorvete', __name__)

@sorvete.route('/sorvetes', methods=['GET'])
def get_sorvetes():
    sorvetes = listar_sorvetes()
    return render_template("sorvetes.html", sorvetes=sorvetes)

@sorvete.route('/sorvetes/adicionar', methods=['GET', 'POST'])
def adicionar_sorvetes():
    categorias = listar_categorias()
    if request.method == 'POST':
        categoria_nome = request.form['categoria_nome']
        sabor = request.form['sabor']
        preco = float(request.form['preco'])
        qtd = int(request.form['qtd'])
        novo_sorvete = {'categoria_nome': categoria_nome, 'sabor': sabor, 'preco': preco, 'qtd': qtd}
        adicionar_sorvete(novo_sorvete)
        return redirect(url_for('sorvete.get_sorvetes'))
    return render_template('criarSorvete.html', categorias=categorias)

@sorvete.route('/sorvetes/<int:id_sorvete>', methods=['GET'])
def get_sorvete(id_sorvete):
    try:
        sorvete = sorvete_por_id(id_sorvete)
        return render_template('sorvete_id.html', sorvete=sorvete)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não encontrado'}), 404

@sorvete.route('/sorvetes/<int:id_sorvete>/editar', methods=['GET', 'POST'])
def editar_sorvete(id_sorvete):
    try:
        sorvete = sorvete_por_id(id_sorvete)
        categorias = listar_categorias()
        if request.method == 'POST':
            sorvete_data = {
                'categoria_id': request.form['categoria_id'],
                'sabor': request.form['sabor'],
                'preco': float(request.form['preco']),
                'qtd': int(request.form['qtd'])
            }
            atualizar_sorvete(id_sorvete, sorvete_data)
            return redirect(url_for('sorvete.get_sorvete', id_sorvete=id_sorvete))
        return render_template('sorvete_update.html', sorvete=sorvete, categorias=categorias)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não encontrado'}), 404
    except CategoriaNaoEncontrada:
        return jsonify({'message': 'Categoria não encontrada'}), 404

@sorvete.route('/sorvetes/<int:id_sorvete>', methods=['DELETE'])
def delete_sorvete(id_sorvete):
    try:
        excluir_sorvete(id_sorvete)
        return jsonify({'message': 'Sorvete excluído com sucesso'}), 200
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não encontrado'}), 404
    
@sorvete.route('/sorvetes/categoria/<int:categoria_id>', methods=['GET'])
def get_sorvetes_por_categoria(categoria_id):
    categoria = categoria_por_id(categoria_id)
    if not categoria:
        return jsonify({'message': 'Categoria não encontrada'}), 404
    sorvetes = listar_sorvetes_por_categoria(categoria_id)
    return render_template('sorvetes_por_categoria.html', sorvetes=sorvetes, categoria=categoria)

