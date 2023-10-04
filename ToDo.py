from wsgiref.simple_server import make_server

import falcon

import json

import psycopg2

try:
    conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
except ConnectionFailure as error:
    print(f"Erro de conexão: {error}")


def listar_tarefas(conn):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM tarefas;")
        try:
            many_rows = curs.fetchmany(3)
        except (Exception, psycopg2.DatabaseError) as error:
            # print("O erro é:")
            # print(error)
            raise NameError("erro de banco desligado")
        return many_rows

        # except psycopg2.OperationalError as error: 
        #     # Tratamento do erro de conexão
        #     print("Erro de conexão com o banco de dados:", error)
        # return many_rows


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

class ListResource:
    def on_get(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        lista = listar_tarefas(conn)
        lista_dicionario = {}
        for indice, tarefa in lista:
            lista_dicionario[indice] = tarefa 
        
        response.media = lista_dicionario

        
    def on_post(self, request, response):
        response.status = falcon.HTTP_200 # This is the default status
        # response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        lista = ler_arquivo()
        body = request.bounded_stream.read()
        dicionario = json.loads(body.decode('utf-8'))
        response.media = {"mensagem": f"recebido a tarefa {dicionario['data']}"}
        adicionar_tarefa(dicionario['data'])

   

class CreateResource:
    def on_delete(self, request, response, task_id):
        response.status = falcon.HTTP_204
        response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override.status
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
things = ListResource()
things_cows = CreateResource()

app.add_route('/tarefas/', things)
app.add_route('/tarefas/{task_id:int}', things_cows)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()

