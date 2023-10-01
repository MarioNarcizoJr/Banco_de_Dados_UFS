import psycopg2
from psycopg2 import Error
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="bd-mario-luan.cix7rbgi8hmh.us-east-1.rds.amazonaws.com",
    dbname="bd_marioluan",
    user="mario",
    password="ADMIN123"
)

app = Flask(__name__)


@app.route('/serie_filme', methods=['GET'])
def get_serie_filme():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM sergiflix.serie_filme;")
    serie_filme = cursor.fetchall()
    cursor.close()

    return jsonify(serie_filme)


@app.route(f'/serie_filme/<int:cod_item>', methods=['GET'])
def get_serie_filmeid(cod_item):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.serie_filme WHERE cod_item = {cod_item};")
    serie_filme = cursor.fetchall()
    cursor.close()

    if not serie_filme:
        return jsonify({'erro': 'serie_filme nao encontrado'})

    return jsonify(serie_filme)


@app.route(f'/serie_filme/add', methods=['POST'])
def post_serie_filme():

    serie_filme = request.get_json()
    cod_item = serie_filme['cod_item']

    if serie_filme.get('nome_item') is None or serie_filme.get('cod_categoria') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if not confere_serie_filme(cod_item):
        return jsonify({'erro': 'ja existe serie_filme com esse id'})

    if confere_cat(serie_filme['cod_categoria']):
        return jsonify({'erro': 'nao existe categoria com esse id'})

    cur = conf.cursor()

    sql = f"INSERT INTO sergiflix.serie_filme VALUES ({serie_filme['cod_item']},'{serie_filme['nome_item']}',{serie_filme['preco_venda']},{serie_filme['preco_aluguel']},{serie_filme['cod_categoria']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'serie_filme adicionado com exito'})


def confere_serie_filme(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.serie_filme WHERE cod_item = {pk};")
    serie_filme = cursor.fetchall()
    cursor.close()
    return not serie_filme

def confere_cat(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.categoria WHERE cod_categoria = {pk};")
    categoria = cursor.fetchall()
    cursor.close()
    return not categoria


@app.route('/serie_filme/<int:cod_item>', methods=['PUT'])
def update_serie_filme(cod_item):
    serie_filme = request.get_json()

    if serie_filme.get('nome_item') is None or serie_filme.get('cod_categoria') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_serie_filme(cod_item):
        return jsonify({'erro': 'nao existe serie_filme com esse id'})

    if confere_cat(serie_filme['cod_categoria']):
        return jsonify({'erro': 'nao existe categoria com esse id'})

    cur = conf.cursor()

    sql = f"UPDATE sergiflix.serie_filme SET nome_item = '{serie_filme['nome_item']}', preco_venda = {serie_filme['preco_venda']}," \
          f"preco_aluguel = {serie_filme['preco_aluguel']}, cod_categoria = {serie_filme['cod_categoria']} WHERE cod_item = {cod_item} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'serie_filme editado com exito'})


@app.route('/sergiflix/<int:cod_item>', methods=['DELETE'])
def delete_serie_filme(cod_item):

    if confere_serie_filme(cod_item):
        return jsonify({'erro': 'nao existe serie_filme com esse id'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM sergiflix.serie_filme WHERE cod_item = {cod_item};")
    cursor.close()

    return jsonify({'sucesso': 'serie_filme excluido com exito'})


app.run(host='0.0.0.0', port=5432, debug=True)