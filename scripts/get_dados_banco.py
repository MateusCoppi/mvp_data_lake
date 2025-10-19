import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="mydatabase",
    user="admin",
    password="admin",
    host="localhost",  # se rodar fora do docker
    port="5432"
)

# Query SQL
query = 'SELECT * FROM public."Pagina1";'  # use aspas duplas se o nome tiver maiúsculas

# Carregar no DataFrame
df = pd.read_sql(query, conn)

# Exibir resultado
print(df.info())

# Encerrar conexão
conn.close()
