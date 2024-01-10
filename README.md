# Todo List API with Falcon

Este é um projeto em Python que utiliza o framework Falcon para criar uma API para gerenciar uma lista de tarefas (Todo List).


## Configuração do banco de dados PostgreSQL

    CREATE DATABASE meubanco;
    
    CREATE TABLE tarefas (
        id SERIAL PRIMARY KEY,
        tarefa TEXT NOT NULL
    );

As informações da linha 12 devem ser alteradas de acordo com as configurações do seu banco.

## Requisitos

python = "^3.11"

falcon = "^3.1.1"

psycopg2 = "^2.9.7"
