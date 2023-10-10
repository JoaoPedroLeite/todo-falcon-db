from wsgiref.simple_server import make_server

import falcon

import json

import psycopg2

def get_db_conn():
    print("Conectando ao banco de dados...")
    try:
        conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
    except psycopg2.OperationalError as error:
        raise psycopg2.OperationalError(error)
    print("Conectado!")
    return conn


def listar_tarefas(conn):
    with conn.cursor() as curs:
        try:
            curs.execute("SELECT * FROM tarefas;")
            many_rows = curs.fetchall()
        except psycopg2.IntegrityError as integrity_error:
            print("Erro de integridade do banco de dados:", integrity_error)
            raise integrity_error
        except psycopg2.ProgrammingError as programming_error:
            print("Erro de programação SQL:", programming_error)
            raise programming_error
        except psycopg2.OperationalError as operational_error:
            print("Erro operacional:", operational_error)
            raise operational_error
        return many_rows


def adicionar_tarefa(conn, dados):
    with conn.cursor() as curs:
        try:
            insert_query = "INSERT INTO tarefas (id, tarefa) VALUES (%s, %s)"
            dados = (dados["id"], dados["tarefa"])
            curs.execute(insert_query, dados)
            conn.commit()
        except psycopg2.IntegrityError as integrity_error:
            print("Erro de integridade do banco de dados:", integrity_error)
            raise integrity_error
        except psycopg2.ProgrammingError as programming_error:
            print("Erro de programação SQL:", programming_error)
            raise programming_error
        except psycopg2.OperationalError as operational_error:
            print("Erro operacional:", operational_error)
            raise operational_error


class ListResource:
    def __init__(self, conn):
        self.conn = conn

    def on_get(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        lista = listar_tarefas(self.conn)
        lista_dicionario = {}
        for indice, tarefa in lista:
            lista_dicionario[indice] = tarefa 
        
        response.media = lista_dicionario
    
    def on_post(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        body = request.bounded_stream.read()
        dados_dicionario = json.loads(body.decode('utf-8'))
        adicionar_tarefa(self.conn, dados_dicionario)
        response.media = {"mensagem": "recebido a tarefa"}


def main():
    conn = get_db_conn()
    app = falcon.App()
    things = ListResource(conn)
    app.add_route('/tarefas/', things)
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        # Serve until process is killed
        httpd.serve_forever()

if __name__ == '__main__':
    main()
