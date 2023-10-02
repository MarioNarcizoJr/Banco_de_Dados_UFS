import psycopg2
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="bd-mario-luan.cix7rbgi8hmh.us-east-1.rds.amazonaws.com",
    dbname="bd_marioluan",
    user="mario",
    password="ADMIN123"
)

app = Flask(__name__)


@app.route('/avaliacoes', methods=['GET'])
def get_avaliacoes():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM sergiflix.avaliacao;")
    avaliacoes = cursor.fetchall()
    cursor.close()

    return jsonify(avaliacoes)


@app.route(f'/avaliacoes/<int:id_telespectador>/<int:cod_item>', methods=['GET'])
def get_avaliacao(id_telespectador, cod_item):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.avaliacao WHERE id_telespectador = {id_telespectador} AND cod_item = {cod_item};")
    avaliacao = cursor.fetchall()
    cursor.close()

    if not avaliacao:
        return jsonify({'erro': 'avaliacao nao encontrada'})

    return jsonify(avaliacao)


@app.route(f'/avaliacoes/add', methods=['POST'])
def add_avaliacao():

    avaliacao = request.get_json()

    if avaliacao.get('cod_item') is None or avaliacao.get('id_telespectador') is None or avaliacao.get('nota') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_item(avaliacao.get('cod_item')) or confere_user(avaliacao.get('id_telespectador')):
        return jsonify({'erro': 'id de jogador ou de jogo não cadastrado'})

    cur = conf.cursor()

    sql = f"INSERT INTO sergiflix.avaliacao VALUES ({avaliacao['nota']},{avaliacao['id_telespectador']},{avaliacao['cod_item']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao adicionada com sucesso'})


def confere_item(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.seriefilme WHERE cod_item = {pk};")
    filme = cursor.fetchall()
    cursor.close()
    return not filme


def confere_user(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.telespectador WHERE id_telespectador = {pk};")
    album = cursor.fetchall()
    cursor.close()
    return not album


def confere_avalia(pk1, pk2):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.avaliacao WHERE id_telespectador = {pk1} AND cod_item = {pk2};")
    album = cursor.fetchall()
    cursor.close()
    return not album


@app.route('/avaliacoes/<int:id_telespectador>/<int:cod_item>', methods=['PUT'])
def update_avaliacao(id_telespectador,cod_item):
    avaliacao = request.get_json()

    if avaliacao.get('nota') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_avalia(id_telespectador, cod_item):
        return jsonify({'erro': 'avaliação não encontrada'})

    cur = conf.cursor()

    sql = f"UPDATE sergiflix.avaliacao SET nota = {avaliacao['nota']}" \
          f" WHERE id_telespectador = {id_telespectador} AND cod_item = {cod_item} ;"

    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao editada com sucesso'})


@app.route('/avaliacoes/<int:id_telespectador>/<int:cod_item>', methods=['DELETE'])
def delete_avaliacao(id_telespectador, cod_item):

    if confere_avalia(id_telespectador, cod_item):
        return jsonify({'erro': 'avaliacao nao encontrada'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM sergiflix.avaliacao WHERE id_telespectador = {id_telespectador} AND cod_item = {cod_item};")
    cursor.close()

    return jsonify({'sucesso': 'avaliacao excluida com sucesso'})


app.run(host='0.0.0.0', port=5432, debug=True)