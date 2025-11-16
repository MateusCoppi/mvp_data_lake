import pandas as pd
import psycopg2


def get_data(colunas: list = "*", schema: str = "public", tabelas: str = 'Pagina1'):

    if colunas is None:
        colunas = "*"
    
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="admin",
        password="admin",
        host="localhost", 
        port="5432"
    )

    # Query SQL
    query = f'SELECT {colunas} FROM {schema}."{tabelas}";'

    # Carregar no DataFrame
    df = pd.read_sql(query, conn)

    # Encerrar conexão
    conn.close()

    return df