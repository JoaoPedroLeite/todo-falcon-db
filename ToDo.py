from wsgiref.simple_server import make_server

import falcon

import json

import psycopg2

try:
    conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
    # conn = psycopg2.connect("dbname='meubanco' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")


def listar_tarefas(conn):
    # we use a context manager to scope the cursor session
    with conn.cursor() as curs:

        try:
            curs.execute("SELECT * FROM tarefas;")

            # a default install should include this query and some backend workers
            many_rows = curs.fetchmany(3)

            # use the * unpack operator to print many_rows which is a Python list
            # print(*many_rows, sep = "\n")
            print(many_rows)
            print(type(many_rows))
            return many_rows

        # a more robust way of handling errors
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# def adicionar_tarefa(tarefa):
#     lista = ler_arquivo()
#     if tarefa == "":
#         print("É necessario colocar alguma tarefa")
#     else:
#         # import pdb; pdb.set_trace()
#         print(lista)
#         print(type(lista))
#         lista.append(tarefa)
#         txt = open("lista.txt",'w')
#         txt.write("\n".join(lista))
#         txt.close()

# def remover_tarefa(task_id):
#     lista = ler_arquivo()
#     # print (lista)
#     indice = task_id
#     try:
#         del lista[indice-1]
#         print("tarefa removida")
#     except IndexError as error:
#         print(f"Tarefa não encontrada: {error}")
#         return False
#     # print (lista)
#     txt = open("lista.txt",'w')#paremetro w sobrescreve arquivo
#     txt.write("\n".join(lista))
#     txt.close()
#     return True

# def atualizar_tarfa(task_id, tarefa):
#     lista = ler_arquivo()
#     indice = task_id
#     try:
#         alteracao = tarefa
#         if alteracao == "":
#             print("É necessario colocar alguma tarefa")
#         else:
#             lista[indice - 1] = alteracao
#             print("Tarefa Alterada.")
#     except IndexError as erro:
#         print(f"Tarefa não encontrada: {erro}")
    
#     txt = open("lista.txt",'w')#paremetro w sobrescreve arquivo
#     txt.write("\n".join(lista))
#     txt.close()

class ThingsResource:
    def on_get(self, request, response):
        """Handles GET requests"""
        response.status = falcon.HTTP_200 # This is the default status
        # response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        lista = listar_tarefas(conn)
        print(lista)
        print(type(lista))
        # response.body = str(lista)
        # lista_string = listar_tarefas()
        lista_dicionario = {}
        for indice, tarefa in lista:
            lista_dicionario[indice] = tarefa 
        
        # response.media = lista_dicionario


        # response.status = falcon.HTTP_200
        
        # response.content_type = falcon.MEDIA_TEXT

        # lista = listar_tarefas(conn)

        # Crie uma lista de strings formatadas
        # lista_formatada = str(f"{indice}: {tarefa}" for indice, tarefa in lista)
        # dicionario_string = '\n'.join([f'{chave}: "{valor}"' for chave, valor in lista_dicionario.items()])



        # print(dicionario_string)

        # Defina a resposta como a lista formatada
        # response.media = dicionario_string

        #Esse for só deixa o ultimo valor:

        for chave, valor in lista_dicionario.items():
            response.media = (f'Chave: {chave}, Valor: {valor}')
            print(f'Chave: {chave}, Valor: {valor}')

        
    def on_post(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        # response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
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
        # print("teste1")
        # print(task_id)
        # response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override.status
        # print(dir(request))

        body = request.bounded_stream.read()
        dicionario = json.loads(body.decode('utf-8'))
        # print(dicionario)
        # print(type(dicionario))
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

