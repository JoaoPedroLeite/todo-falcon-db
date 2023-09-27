from wsgiref.simple_server import make_server

import falcon

import json

import psycopg2

try:
    conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
except:
    print("I am unable to connect to the database")


def listar_tarefas(conn):
    with conn.cursor() as curs:

        try:
            curs.execute("SELECT * FROM tarefas;")
            many_rows = curs.fetchmany(3)
            print(many_rows)
            print(type(many_rows))
            return many_rows
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

class ThingsResource:
    def on_get(self, request, response):
        """Handles GET requests"""
        response.status = falcon.HTTP_200 # This is the default status
        lista = listar_tarefas(conn)
        print(lista)
        print(type(lista))
        lista_dicionario = {}
        for indice, tarefa in lista:
            lista_dicionario[indice] = tarefa 
        
        response.media = lista_dicionario

        
    def on_post(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        lista = ler_arquivo()
        
        body = request.bounded_stream.read()
        dicionario = json.loads(body.decode('utf-8'))
        # print(dicionario)
        # print(type(dicionario))
        response.media = {"mensagem": f"recebido a tarefa {dicionario['data']}"}

        adicionar_tarefa(dicionario['data'])

   

class CowsResource:
    def on_delete(self, request, response, task_id):
        response.status = falcon.HTTP_204
        response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override.status
        print(dir(request))
        print(task_id)
        print(type(task_id))
        # response.text = "ok"
        erro = remover_tarefa(task_id)

        if erro == False:
            response.status = falcon.HTTP_200
            response.text = "Tarefa não encontrada"
    
    def on_patch(self, request, response, task_id):

        response.status = falcon.HTTP_204
        body = request.bounded_stream.read()
        dicionario = json.loads(body.decode('utf-8'))
        response.media = {"mensagem": f"recebido a tarefa {dicionario['data']}"}


        atualizar_tarfa(task_id,dicionario['data'])




app = falcon.App()


things = ThingsResource()
things_cows = CowsResource()


app.add_route('/tarefas/', things)
app.add_route('/tarefas/{task_id:int}', things_cows)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()

