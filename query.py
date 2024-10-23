#conexão com banco de dados e enviar os dados para o dash

#pip install mysql-connector-python

#conexão

import pandas as pd
import mysql.connector


def conexao(query):
    conn = mysql.connector.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        password = "adm123",
        db = "bd_carro"
    )

    dataframe = pd.read_sql(query, conn)

    conn.close()

    return dataframe