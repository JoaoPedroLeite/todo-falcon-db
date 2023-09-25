#!/usr/bin/env python
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2

try:
    conn = psycopg2.connect("dbname='meubanco' user='joao' host='localhost' port='5432' password='1234'")
    # conn = psycopg2.connect("dbname='meubanco' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")

# we use a context manager to scope the cursor session
with conn.cursor() as curs:

    try:
        # simple single row system query
        # curs.execute("SELECT version()")

        # # returns a single row as a tuple
        # single_row = curs.fetchone()

        # # use an f-string to print the single tuple returned
        # print(f"{single_row}")

        # simple multi row system query
        # curs.execute("SELECT query, backend_type FROM pg_stat_activity")
        curs.execute("SELECT * FROM usuario;")

        # a default install should include this query and some backend workers
        many_rows = curs.fetchmany(2)

        # use the * unpack operator to print many_rows which is a Python list
        print(*many_rows, sep = "\n")
        # print(many_rows)

    # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)