import mysql.connector

def test_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vendas_db',  # Nome do banco de dados
            user='root',     # Substitua pelo seu usuário
            password='Luiz@160404'    # Substitua pela sua senha
        )
        
        if connection.is_connected():
            print("Conexão ao MySQL estabelecida com sucesso!")
            db_info = connection.get_server_info()
            print(f"Versão do servidor MySQL: {db_info}")
            
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexão encerrada com sucesso.")

# Teste a função
test_mysql_connection()
