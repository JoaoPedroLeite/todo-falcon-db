from wsgiref.simple_server import make_server

import falcon

import json

import psycopg2

try:
    conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
    # conn = psycopg2.connect("dbname='meubanco' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")

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



    # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#-------------------------------------------------------

