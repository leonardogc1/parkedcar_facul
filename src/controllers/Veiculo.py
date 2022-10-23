from flask import Blueprint, jsonify, request, make_response
from flask_restx import Resource, Namespace
from flask_jwt import jwt_required
from database.request_handler import request_handler

# Entities
from models.entities.Veiculo import Veiculo
# Models
from models.VeiculoModel import VeiculoModel

##
veiculo_ = Namespace('veiculo', description='Veículo feature set')


@veiculo_.route('/estoque')
class Veiculo(Resource):
    def get(self):
        try:
            veiculos = VeiculoModel.get_estoque()
            return jsonify({'status_message': '',
                            'payload':veiculos})
        except Exception as ex:
            resp = jsonify({'message': str(ex)}), 404
            return resp

@veiculo_.route('/vendas')
class Veiculo(Resource):
    def get(self):
        try:
            veiculos = VeiculoModel.get_vendas()
            return jsonify({'status_message': '',
                            'payload':veiculos})
        except Exception as ex:
            resp = jsonify({'message': str(ex)}), 404
            return resp


@veiculo_.route('/estoque/<id>')
class Veiculo(Resource):
    def get(self, id):
        try:
            veiculo = VeiculoModel.get_veiculo(id)
            if veiculo != None:
                return jsonify({'status_message': '',
                            'payload':veiculo})
            else:
                return jsonify({}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@veiculo_.route('/adiciona-veiculo-estoque')
class Veiculo(Resource):
    def post(self):
        try:
            requestInformation = request_handler(request)   
            args = requestInformation.get_args()
            marca = args['marca'] if 'marca' in args else None            
            modelo = args['modelo'] if 'modelo' in args else None            
            ano = int(args['ano'] if 'ano' in args else None)            
            cor = args['cor'] if 'cor' in args else None
            preco_compra = float(args['preco_compra'] if 'preco_compra' in args else None)           
            preco_venda = float(args['preco_venda'] if 'preco_venda' in args else None)
            status = 'estoque'            
            id = VeiculoModel.get_id() + 1
            affected_rows = VeiculoModel.add_veiculo(id, marca, modelo, ano, cor, preco_compra, preco_venda, status)
            print('oi')

            if affected_rows == 1:
                return jsonify()
            else:
                return jsonify({'message': "Erro ao inserir veículo"}), 500

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@veiculo_.route('/edita-veiculo/<id>')
class Veiculo(Resource):
    def put(self, id):
        try:
            marca = request.json['marca']
            modelo = request.json['modelo']
            ano = int(request.json['ano'])
            cor = request.json['cor']
            preco_compra = float(request.json['preco_compra'])
            preco_venda = float(request.json['preco_venda'])
            status = request.json['status']
            veiculo = Veiculo(id, marca, modelo, ano, cor, preco_compra, preco_venda, status)

            affected_rows = VeiculoModel.update_veiculo(veiculo)

            if affected_rows == 1:
                return jsonify(veiculo.id)
            else:
                return jsonify({'message': "Veículo não atualizado"}), 404

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@veiculo_.route('/delete-veiculo/<id>')
class Veiculo(Resource):
    def delete(self, id):
        try:
            veiculo = VeiculoModel.get_veiculo(id)

            affected_rows = VeiculoModel.delete_veiculo(veiculo)

            if affected_rows == 1:
                return jsonify(veiculo.id)
            else:
                return jsonify({'message': "Veículo não deletado!"}), 404

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500