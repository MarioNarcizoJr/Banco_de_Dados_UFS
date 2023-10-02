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


@app.route('/telespectador', methods=['GET'])
def get_telespectador():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM sergiflix.telespectador;")
    telespectador = cursor.fetchall()
    cursor.close()

    return jsonify(telespectador)


@app.route(f'/telespectador/<int:id_telespectador>', methods=['GET'])
def get_telespectadorid(id_telespectador):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.telespectador WHERE id_telespectador = {id_telespectador};")
    telespectador = cursor.fetchall()
    cursor.close()

    if not telespectador:
        return jsonify({'erro': 'telespectador nao encontrado'})

    return jsonify(telespectador)


@app.route(f'/telespectador/add', methods=['POST'])
def post_telespectador():
    telespectador = request.get_json()
    id_telespectador = telespectador['id_telespectador']

    if telespectador.get('primeiro_nome') is None or telespectador.get('email') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_email(telespectador.get('email')):
        return jsonify({'erro': 'não existe telespectador com esse email'})

    if not confere_telespectador(id_telespectador):
        return jsonify({'erro': 'ja existe telespectador com esse id'})

    cur = conf.cursor()

    sql = f"INSERT INTO sergiflix.telespectador VALUES ({telespectador['id_telespectador']},{telespectador['qtd_itens']},'{telespectador['primeiro_nome']}','{telespectador['email']}');"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'telespectador adicionado com exito'})


def confere_telespectador(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.telespectador WHERE id_telespectador = {pk};")
    telespectador = cursor.fetchall()
    cursor.close()
    return not telespectador


def confere_email(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM sergiflix.telespectador WHERE email = '{pk}';")
    email = cursor.fetchall()
    cursor.close()
    return not email


@app.route('/telespectador/<int:id_telespectador>', methods=['PUT'])
def update_telespectador(id_telespectador):
    telespectador = request.get_json()

    if telespectador.get('email') is None or telespectador.get('primeiro_nome') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_telespectador(id_telespectador):
        return jsonify({'erro': 'nao existe telespectador com esse id'})

    if confere_email(telespectador['email']):
        return jsonify({'erro': 'este email não esta cadastrado'})
    cur = conf.cursor()

    sql = f"UPDATE sergiflix.telespectador SET qtd_itens = '{telespectador['qtd_itens']}', primeiro_nome = '{telespectador['primeiro_nome']}',email = '{telespectador['email']}'" \
          f" WHERE id_telespectador = {id_telespectador} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'telespectador editado com exito'})


@app.route('/telespectador/<int:id_telespectador>', methods=['DELETE'])
def delete_telespectador(id_telespectador):

    if confere_telespectador(id_telespectador):
        return jsonify({'erro': 'nao existe telespectador com esse id'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM sergiflix.telespectador WHERE id_telespectador = {id_telespectador};")
    cursor.close()

    return jsonify({'sucesso': 'telespectador excluido com exito'})


app.run(host='0.0.0.0', port=5432, debug=True)