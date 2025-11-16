import pandas as pd
import psycopg2


class DataBaseConnection:

    ## Valores padrão para criação da conexão com o banco
    def __init__(
        self,
        dbname="mydatabase", 
        user="admin", 
        password="admin", 
        host="localhost", 
        port="5432"
    ):

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    ## Cria a conexão com o banco
    def connection(self):

        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host, 
            port=self.port
        )

    ## Retorna os dados do banco através de uma query SQL no formato pandas dataframe
    def get_data(self, colunas: list = "*", schema: str = "public", tabelas: str = 'Pagina1'):

        if colunas is None:
            colunas = "*"
        
        # Se colunas for lista → converte para string
        if isinstance(colunas, list):
            colunas = ", ".join(colunas)

        conn = self.connection()

        # Query SQL
        query = f'''
            SELECT {colunas} 
            FROM {schema}."{tabelas}";
        '''

        # Carregar no DataFrame
        df = pd.read_sql(query, conn)

        # Encerrar conexão
        conn.close()

        return df

if __name__ == "__main__":

    db = DataBaseConnection()

    df = db.get_data()

    print(df.head())