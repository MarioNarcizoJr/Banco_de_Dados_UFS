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


@app.route('/seriefilme', methods=['GET'])
def get_seriefilme():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM sergiflix.seriefilme;")
    seriefilme = cursor.fetchall()
    cursor.close()

    return jsonify(seriefilme)


@app.route(f'/seriefilme/<int:cod_item>', methods=['GET'])
def get_seriefilmeid(cod_item):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.seriefilme WHERE cod_item = {cod_item};")
    seriefilme = cursor.fetchall()
    cursor.close()

    if not seriefilme:
        return jsonify({'erro': 'seriefilme nao encontrado'})

    return jsonify(seriefilme)


@app.route(f'/seriefilme/add', methods=['POST'])
def post_seriefilme():

    seriefilme = request.get_json()
    cod_item = seriefilme['cod_item']

    if seriefilme.get('nome_item') is None or seriefilme.get('cod_item') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if not confere_seriefilme(cod_item):
        return jsonify({'erro': 'ja existe seriefilme com esse id'})


    cur = conf.cursor()

    sql = f"INSERT INTO sergiflix.seriefilme VALUES ({seriefilme['cod_item']},'{seriefilme['nome_item']}',{seriefilme['preco_venda']},{seriefilme['preco_aluguel']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'seriefilme adicionado com exito'})


def confere_seriefilme(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.seriefilme WHERE cod_item = {pk};")
    seriefilme = cursor.fetchall()
    cursor.close()
    return not seriefilme



@app.route('/seriefilme/<int:cod_item>', methods=['PUT'])
def update_seriefilme(cod_item):
    seriefilme = request.get_json()

    if seriefilme.get('nome_item') is None or seriefilme.get('cod_item') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_seriefilme(cod_item):
        return jsonify({'erro': 'nao existe seriefilme com esse id'})

    cur = conf.cursor()

    sql = f"UPDATE sergiflix.seriefilme SET nome_item = '{seriefilme['nome_item']}', preco_venda = {seriefilme['preco_venda']}," \
          f"preco_aluguel = {seriefilme['preco_aluguel']} WHERE cod_item = {cod_item} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'seriefilme editado com exito'})


@app.route('/seriefilme/<int:cod_item>', methods=['DELETE'])
def delete_seriefilme(cod_item):

    if confere_seriefilme(cod_item):
        return jsonify({'erro': 'nao existe seriefilme com esse id'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM sergiflix.seriefilme WHERE cod_item = {cod_item};")
    cursor.close()

    return jsonify({'sucesso': 'seriefilme excluido com exito'})


app.run(host='0.0.0.0', port=5432, debug=True)