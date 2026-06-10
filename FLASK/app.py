import funcoes
import dados
from flask import Flask, jsonify, request , render_template

app = Flask(__name__)

biblioteca = dados.carregar_do_arquivo()

@app.route('/biblioteca', methods=['GET', 'POST'])
@app.route('/biblioteca/<isbn>', methods=['GET', 'PUT', 'DELETE'])
def exibir_json(isbn=None):
    if request.method == 'GET':
        return render_template('lista.html', biblioteca=biblioteca), 200
    elif request.method == 'POST':
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify('Novo livro inserido'), 201
    elif request.method == 'PUT':
        alteracoes = request.get_json()
        for l in biblioteca:
            if l['isbn'] == isbn:
                for key, value in alteracoes.items():
                    l[key] = value
                dados.salvar_no_arquivo(biblioteca)
            return jsonify('Livro atualizado'), 200
    elif request.method == 'DELETE':
        for l in biblioteca:
            if l['isbn'] == isbn:
                biblioteca.remove(l)
                dados.salvar_no_arquivo(biblioteca) 
                return jsonify('Livro deletado com sucesso')
    return jsonify('Livro não encontrado'), 404

@app.route('/biblioteca/criar', methods=['GET', 'POST'])
def cria_livro():
    if request.method == 'POST':
        novo_livro = {
            'isbn' : request.form.get('isbn'),
            'titulo' : request.form.get('titulo'),
            'autor' : request.form.get('autor'),
            'genero' : request.form.get('genero'),
            'ano_publicacao' : request.form.get('ano_publicacao'),
            'editora' : request.form.get('editora'),
            'paginas' : request.form.get('paginas'),
            'status' : request.form.get('status'),
            'localizacao' : request.form.get('localizacao')
        }
        for l in biblioteca:
            if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro ja cadastrado")
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return redirect('lista.html')
    else:
        return render_template('criar.html')



if __name__ == "__main__":
    app.run(debug=True)