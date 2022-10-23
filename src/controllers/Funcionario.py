from flask import Blueprint, jsonify, request
from flask_restx import Resource, Namespace
from database.request_handler import request_handler

# Entities
from models.entities.Funcionario import Funcionario
# Models
from models.FuncionarioModel import FuncionarioModel

##
funcionario_ = Namespace('funcionario', description='Funcionário feature set')


@funcionario_.route('/colaboradores')
class Funcionario(Resource):
    def get(self):
        try:
            funcionarios = FuncionarioModel.get_funcionarios()
            return jsonify({'status_message': '',
                            'payload':funcionarios})
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@funcionario_.route('/colaboradores/<id>')
class Funcionario(Resource):
    def get(self, id):
        try:
            funcionario = FuncionarioModel.get_funcionario(id)
            if funcionario != None:
                return jsonify({'status_message': '',
                            'payload':funcionario})
            else:
                return jsonify({}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@funcionario_.route('/adiciona-colaborador')
class Funcionario(Resource):
    def post(self):
        try:
            requestInformation = request_handler(request)
            args = requestInformation.get_args()

            nome = args['nome'] if 'nome' in args else None
            registro = args['registro'] if 'registro' in args else None
            salario = float(args['salario' if 'salario' in args else None])
            funcao = args['funcao'] if 'funcao' in args else None
            usuario = args['usuario'] if 'usuario' in args else None
            senha = args['senha'] if 'senha' in args else None
            id = FuncionarioModel.get_id() + 1

            affected_rows = FuncionarioModel.add_funcionario(id, nome, registro, salario, funcao, senha, usuario)

            if affected_rows == 1:
                return jsonify()
            else:
                return jsonify({'message': "Erro ao adicionar Funcionário"}), 500

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@funcionario_.route('/edita-colaborador/<id>')
class Funcionario(Resource):
    def put(self, id):
        try:
            nome = request.json['nome']
            registro = request.json['registro']
            salario = float(request.json['salario'])
            funcao = request.json['funcao']
            usuario = request.json['usuario']
            senha = request.json['senha']
            funcionario = Funcionario(id, nome, registro, salario, funcao, senha, usuario)

            affected_rows = FuncionarioModel.update_funcionario(funcionario)

            if affected_rows == 1:
                return jsonify(funcionario.id)
            else:
                return jsonify({'message': "Funcionário não atualizado"}), 404

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@funcionario_.route('/delete-funcionario/<id>')
class Funcionario(Resource):
    def delete(self, id):
        try:
            funcionario = FuncionarioModel.get_funcionario(id)

            affected_rows = FuncionarioModel.delete_funcionario(funcionario)

            if affected_rows == 1:
                return jsonify(funcionario.id)
            else:
                return jsonify({'message': "Funcionário não deletado!"}), 404

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

@funcionario_.route('/auth/<usuario>/<senha>')
class Funcionario(Resource):
    def get(self, usuario, senha):
        try:
            funcionario = FuncionarioModel.get_login(usuario, senha)
            if funcionario != None:
                return jsonify({'status_message': '',
                            'payload':funcionario})
            else:
                return jsonify({'message': 'login não encontrado'}), 500 
        except Exception as ex:
            return jsonify({'status_message': str(ex)})