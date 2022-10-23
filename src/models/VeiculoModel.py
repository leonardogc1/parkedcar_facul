import logging
from database.db import get_connection
from flask import request
from database.request_handler import request_handler
from models.entities.Veiculo import Veiculo

class VeiculoModel():

    @classmethod
    def get_id(self):
        try:
            connection = get_connection()
            
            with connection.cursor() as cursor:
                sql = '''
                    SELECT v.id
                    FROM veiculos v
                    ORDER BY v.id DESC
                    LIMIT 1;
                '''
                cursor.execute(sql)
                resultone = cursor.fetchall()
                id = resultone[0][0]
                
            connection.close()
            return id
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_estoque(self):
        try:
            request_information = request_handler(request)
            args = request_information.get_args()

            search = '%' + args['search'] + '%' if 'search' in args else '%%'
            connection = get_connection()
            veiculos = []

            with connection.cursor() as cursor:
                sql = '''
                    SELECT v.id, 
                           v.marca, 
                           v.modelo,
                           v.ano,
                           v.cor,
                           v.preco_compra,
                           v.preco_venda,
                           v.status
                           FROM veiculos v
                           WHERE v.status = 'estoque'
                           AND upper(v.modelo) like upper(%s)
                           ORDER BY id;
                '''
                cursor.execute(sql, [search])
                resultset = cursor.fetchall()
                
                for row in resultset:    
                    veiculo = Veiculo(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]), row[7])                    
                    veiculos.append(veiculo.to_JSON())
                    
            connection.close()            
            return veiculos
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)

    @classmethod
    def get_vendas(self):
        try:
            request_information = request_handler(request)
            args = request_information.get_args()

            search = '%' + args['search'] + '%' if 'search' in args else '%%'
            connection = get_connection()
            veiculos = []

            with connection.cursor() as cursor:
                sql = '''
                    SELECT v.id, 
                           v.marca, 
                           v.modelo,
                           v.ano,
                           v.cor,
                           v.preco_compra,
                           v.preco_venda,
                           v.status
                           FROM veiculos v
                           WHERE v.status = 'venda'
                           AND upper(v.modelo) like upper(%s)
                           ORDER BY id;
                '''
                cursor.execute(sql, [search])
                resultset = cursor.fetchall()
                
                for row in resultset:    
                    veiculo = Veiculo(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]), row[7])                    
                    veiculos.append(veiculo.to_JSON())
                    
            connection.close()            
            return veiculos
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)

    @classmethod
    def get_veiculo(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    SELECT v.id, 
                           v.marca, 
                           v.modelo,
                           v.ano,
                           v.cor,
                           v.preco_compra,
                           v.preco_venda,
                           v.status
                           FROM veiculos v
                           WHERE v.id = %s;
                '''
                cursor.execute(sql, [id])
                row = cursor.fetchone()

                resultado = None
                if row != None:
                    veiculo = Veiculo(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]), row[7])
                    resultado = veiculo.to_JSON()

            connection.close()
            return resultado
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)


    @classmethod
    def add_veiculo(self, id, marca, modelo, ano, cor, preco_compra, preco_venda, status):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = '''
                    INSERT INTO veiculos (
                           id, 
                           marca, 
                           modelo,
                           ano,
                           cor,
                           preco_compra,
                           preco_venda,
                           status)
                           VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                           );
                '''
                cursor.execute(sql, [id, marca, modelo, ano, cor,
                    preco_compra, preco_venda, status])
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_veiculo(self, veiculo):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    UPDATE veiculos v
                    SET v.id = %s,
                        v.marca = %s,
                        v.modelo = %s,
                        v.ano = %s,
                        v.cor = %s,
                        v.preco_compra = %s,
                        v.preco_venda = %s,
                        v.status = %s;
                    '''
                cursor.execute(sql, (veiculo.id, veiculo.marca, veiculo.modelo, veiculo.ano, veiculo.cor,
                    veiculo.preco_compra, veiculo.preco_venda, veiculo.status))
                
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def delete_veiculo(self, veiculo):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    DELETE FROM veiculo v
                    WHERE v.id = %s;
                '''
                cursor.execute(sql, (veiculo.id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)