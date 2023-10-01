from flask import Flask, jsonify, request 
from flask_restx import Api, Resource, fields

import datetime 

class Pessoa:
    def __init__(self, cpf, nome, data):
        self.cpf = cpf
        self.nome = nome
        self.data = data

    def retorne_dict(self):
        return {'cpf' : self.cpf, 'nome' : self.nome, 'data' : self.data}

app = Flask(__name__)
api = Api(app, version='1.0', title='API - BD parte 1',
    description='API Web Banco de Dados - Alunos: Mário Narcizo e Luan Prata', doc='/doc')

banco_dados = [ Pessoa(07158488977, "Sandra", datetime.date(2015,9,17)) ]

date_model = api.model('Date', {
    'ano': fields.Integer(required=True),
    'mes': fields.Integer(required=True),
    'dia': fields.Integer(required=True)
})

pessoa_model = api.model('Pessoa', {
    'cpf': fields.Integer(required=True),
    'nome': fields.String(required=True),
    'data': fields.Nested(date_model, required=True)
})

us = api.namespace('Cadastro', description='Como Cadastrar e consultar usuários')
  
@us.route('/usuarios/<int:cpf>')
class Usuario(Resource):

    @api.doc(responses={200: 'OK', 404: 'Não encontrado'},
             params = {'cpf' : {'description': 'CPF User', 'example': 123456789}},
             description = 'Consulta o usuário a ser buscado no banco de dados')
    
    def get(self, cpf):
        for usuario in banco_dados:
            if usuario.cpf == cpf:
                return jsonify(usuario.retorne_dict())
        return "Usuário não encontrado", 404

@app.route('/usuarios/<int:cpf>', methods=['GET'])  # type: ignore
def consultar_usuario(cpf):
    for usuario in banco_dados:
        if usuario.cpf == cpf:
            print(usuario)
            return jsonify(usuario.retorne_dict())
    
    return "Usuario não encontrado", 400

@us.route('/usuarios/cadastro')
class CadastroUsuarios(Resource):

    @api.doc(responses={201: 'OK', 400: 'Dado invalido'},
             params = {'cpf' : {'description': 'CPF do usuário a ser cadastrado', 'example': 987654321},
                       'nome' : {'description': 'Nome do usuário a ser cadastrado', 'example': "Mário Narcizo"},
                       'data' : {'description': 'Data de nascimento do usuário', 'example': {'dia' : 1, 'mes' : 1, 'ano' : 2000}}},
             description = 'Cadastra usuário no banco de dados')
    
    @api.expect(pessoa_model)
    def post(self):
        novo_usuario = request.get_json()

        for usuario in banco_dados:
            if usuario.cpf == novo_usuario['cpf']:
                return {'message': 'Já existe um usuário com este CPF no sistema!'}, 400

        data_nasc = (novo_usuario['data'])
        if validaData(data_nasc) == False:
            return {'message': 'Insira uma data valida!'}, 400
        
        data_formatada = datetime.date(data_nasc["ano"], data_nasc["mes"], data_nasc["dia"])

        novo_usuario = Pessoa(novo_usuario['cpf'], novo_usuario['nome'], data_formatada)

        banco_dados.append(novo_usuario)

        return {'message': 'Usuário cadastrado!'},201

@app.route('/usuarios/cadastro', methods=['POST']) 
def cadastrar_usuario():

    novo_usuario = request.get_json()
        
    for usuario in banco_dados:
        if usuario.cpf == novo_usuario['cpf']:
            return 'Ja existe um usuario com este cpf no sistema!'

    data_nasc = (novo_usuario['data'])
    if validaData(data_nasc) == False:
        return {'message': 'Insira uma data valida!'}, 400
    data_formatada = datetime.date(data_nasc["ano"],data_nasc["mes"], data_nasc["dia"])

    novo_usuario = Pessoa(novo_usuario['cpf'], novo_usuario['nome'], data_formatada)
        
    banco_dados.append(novo_usuario)

    saida = []
    for usuario in banco_dados:
        saida.append(usuario.retorne_dict())

    return saida

def validaData(data):
    if data['ano'] <= 0:
        return False
    elif data['mes'] < 1 or data['mes'] > 12:
        return False
    elif data['dia'] < 1 or data['dia'] > 31:
        return False
    
    return True

app.run(host='0.0.0.0', port=5432, debug= True)