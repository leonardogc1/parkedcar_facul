from database.db import get_connection
from models.entities.Funcionario import Funcionario
from database.request_handler import request_handler
from flask import request
import logging

class FuncionarioModel():

    @classmethod
    def get_id(self):
        try:
            connection = get_connection()
            
            with connection.cursor() as cursor:
                sql = '''
                    SELECT f.id
                    FROM funcionarios f
                    ORDER BY f.id DESC
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
    def get_funcionarios(self):
        try:
            request_information = request_handler(request)
            args = request_information.get_args()

            search = '%' + args['search'] + '%' if 'search' in args else '%%'
            connection = get_connection()
            funcionarios = []

            with connection.cursor() as cursor:
                sql = '''
                    SELECT f.id, 
                           f.nome, 
                           f.registro,
                           f.salario,
                           f.funcao,
                           f.senha,
                           f.usuario
                           FROM funcionarios f
                           ORDER BY nome
                           WHERE upper(f.nome) like upper(%s);
                '''
                cursor.execute(sql, [search])
                resultset = cursor.fetchall()

                for row in resultset:
                    funcionario = Funcionario(row[0], row[1], row[2], float(row[3]), row[4], row[5], row[6])
                    funcionarios.append(funcionario.to_JSON())

            connection.close()
            return funcionarios
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)


    @classmethod
    def get_funcionario(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    SELECT f.id, 
                           f.nome, 
                           f.registro,
                           f.salario,
                           f.funcao,
                           f.senha,
                           f.usuario
                           FROM funcionarios f
                           WHERE f.id = %s
                '''
                cursor.execute(sql, (id))
                row = cursor.fetchone()

                funcionario = None
                if row != None:
                    funcionario = Funcionario(row[0], row[1], row[2], float(row[3]), row[4], row[5], row[6])
                    funcionario = funcionario.to_JSON()

            connection.close()
            return funcionario
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def add_funcionario(self, id, nome, registro, salario, funcao, senha, usuario):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = '''
                    INSERT INTO funcionarios (
                           id, 
                           nome, 
                           registro,
                           salario,
                           funcao,
                           senha,
                           usuario)
                    VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        );
                    '''              
                cursor.execute(sql, [id, nome, registro,
                    salario, funcao, senha, usuario])
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_funcionario(self, funcionario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    UPDATE funcionarios f
                    SET f.id = %s,
                        f.nome = %s,
                        f.registro = %s,
                        f.salario = %s,
                        f.funcao = %s,
                        f.senha = %s,
                        f.usuario = %s
                    '''
                cursor.execute(sql, (funcionario.id, funcionario.nome, funcionario.registro,
                    funcionario.salario, funcionario.funcao, funcionario.senha, funcionario.usuario))
                
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def delete_funcionario(self, funcionario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    DELETE FROM funcionarios f
                    WHERE f.id = %s
                '''
                cursor.execute(sql, (funcionario.id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_login(self, usuario, senha):
        try:
            usuario = "'" + usuario + "'"
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = '''
                        SELECT  f.id,
                                f.nome,
                                f.registro,
                                f.salario,
                                f.funcao,
                                f.senha,
                                f.usuario
                        FROM funcionarios f
                        WHERE f.usuario = {}
                '''.format(usuario)                     
                
                cursor.execute(sql)
                row = cursor.fetchone()
                

                funcionario = None
                if row != None:
                    funcionario = Funcionario(row[0], row[1], row[2], float(row[3]), row[4], row[5], row[6])
                    
                    if funcionario.login(senha):
                        funcionario = funcionario.to_JSON()
                    else:
                        funcionario = None      
            connection.close()
            return funcionario
        except Exception as ex:
            raise Exception(ex)