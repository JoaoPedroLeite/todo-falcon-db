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
        insert_query ="INSERT INTO tarefas (tarefa) VALUES (%s);"
        dados = (dados["tarefa"],)
        print(dados)

        try:
            curs.execute(insert_query, dados)
        except (psycopg2.IntegrityError, psycopg2.ProgrammingError, psycopg2.OperationalError) as erro:
            raise psycopg2.DatabaseError(erro)
        conn.commit()


def remover_tarefa(conn, task_id):
    with conn.cursor() as curs:
        insert_query ="DELETE FROM tarefas WHERE id = %s"
        indice = task_id

        try:
            curs.execute(insert_query, (str(indice),))
        except (psycopg2.IntegrityError, psycopg2.ProgrammingError, psycopg2.OperationalError) as erro:
            raise psycopg2.DatabaseError(erro)
        conn.commit()


def atualizar_tarfa(conn, task_id, tarefa):
    insert_query ="UPDATE tarefas SET tarefa = %s WHERE id = %s"
    indice = task_id
    dados = (tarefa["tarefa"], str(indice))

    with conn.cursor() as curs:
        try:
            curs.execute(insert_query, dados)
        except (psycopg2.IntegrityError, psycopg2.ProgrammingError, psycopg2.OperationalError) as erro:
            raise psycopg2.DatabaseError(erro)
        conn.commit()



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
        body = request.bounded_stream.read()
        print(f"{body = }")
        print(f"{body.decode('utf-8') = }")
        nova_tarefa = json.loads(body.decode('utf-8'))
        adicionar_tarefa(self.conn, nova_tarefa)
        response.media = {"mensagem": f"recebido a tarefa: {nova_tarefa['tarefa']}"}


class OtherResource:
    def __init__(self, conn):
        self.conn = conn

    def on_delete(self, request, response, task_id):
        response.status = falcon.HTTP_204
        response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override.status
        remover_tarefa(self.conn, task_id)
    
    def on_patch(self, request, response, task_id):
        body = request.bounded_stream.read()
        nova_tarefa = json.loads(body.decode('utf-8'))
        atualizar_tarfa(self.conn, task_id, nova_tarefa)
        response.media = {"mensagem": f"tarefa alterada para: {nova_tarefa['tarefa']}"}


def main():
    conn = get_db_conn()
    app = falcon.App(cors_enable = True)
    things = ListResource(conn)
    app.add_route('/tarefas/', things)

    things_other = OtherResource(conn)
    app.add_route('/tarefas/{task_id:int}', things_other)

    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        # Serve until process is killed
        httpd.serve_forever()

if __name__ == '__main__':
    main()
