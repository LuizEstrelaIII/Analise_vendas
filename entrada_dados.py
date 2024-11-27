import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns

# Função para inserir dados no MySQL
def insert_data_to_mysql(produto, quantidade, preco, data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vendas_db',  # Nome do banco de dados
            user='root',     # Substitua pelo seu usuário
            password='Luiz@160404'    # Substitua pela sua senha
        )
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO vendas (produto, quantidade, preco, data) 
                              VALUES (%s, %s, %s, %s)"""
            data_tuple = (produto, quantidade, preco, data)
            cursor.execute(insert_query, data_tuple)
            connection.commit()
            st.success("Dados inseridos com sucesso no banco de dados!")
    except Error as e:
        st.error(f"Erro ao inserir os dados: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Função para consultar dados no MySQL
def query_data_from_mysql(query):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vendas_db',
            user='root',     # Substitua pelo seu usuário
            password='Luiz@160404'    # Substitua pela sua senha
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Error as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Interface Streamlit para Entrada de Dados
st.title("Sistema de Entrada de Dados para Análise de Vendas")

st.subheader("Escolha o Método de Entrada de Dados")
input_method = st.radio(
    "Como deseja inserir os dados?",
    ("Entrada Manual", "Upload de Arquivo CSV")
)

if input_method == "Entrada Manual":
    st.subheader("Insira os Dados Manualmente")

    produto = st.text_input("Produto")
    quantidade = st.number_input("Quantidade Vendida", min_value=0, step=1)
    preco = st.number_input("Preço Unitário", min_value=0.0, step=0.01)
    data = st.date_input("Data da Venda")
    
    if st.button("Adicionar Dados"):
        if produto and (quantidade > 0) and (preco > 0):
            # Inserir os dados manualmente no banco de dados
            insert_data_to_mysql(produto, quantidade, preco, data)
            
            novo_dado = {
                "Produto": produto,
                "Quantidade Vendida": quantidade,
                "Preço Unitário": preco,
                "Data da Venda": data
            }
            st.write("Dados Inseridos:")
            st.write(novo_dado)
        else:
            st.warning("Por favor, preencha todos os campos com valores válidos!")

elif input_method == "Upload de Arquivo CSV":
    st.subheader("Carregue um Arquivo CSV")
    uploaded_file = st.file_uploader("Selecione um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dados Carregados com Sucesso:")
        st.dataframe(df)
        
        # Inserir os dados carregados do CSV no banco de dados
        if st.button("Inserir Dados no Banco de Dados"):
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='vendas_db',
                    user='root',
                    password='Luiz@160404'
                )
                if connection.is_connected():
                    cursor = connection.cursor()
                    for i, row in df.iterrows():
                        insert_query = """INSERT INTO vendas (produto, quantidade, preco, data)
                                          VALUES (%s, %s, %s, %s)"""
                        cursor.execute(insert_query, (row['produto'], row['quantidade'], row['preco'], row['data']))
                    connection.commit()
                    st.success("Dados inseridos com sucesso no banco de dados!")
            except Error as e:
                st.error(f"Erro ao inserir os dados no banco: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()


# Interface Streamlit para Relatórios
st.title("Relatórios de Vendas")

# Relatório 1: Vendas Totais por Produto
st.subheader("Vendas Totais por Produto")
query = "SELECT produto, SUM(quantidade) AS total_vendas FROM vendas GROUP BY produto"
result = query_data_from_mysql(query)

if result:
    df_vendas_produto = pd.DataFrame(result, columns=['Produto', 'Total de Vendas'])
    st.write(df_vendas_produto)
    
    # Gerando gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Produto', y='Total de Vendas', data=df_vendas_produto)
    plt.title('Vendas Totais por Produto')
    plt.xticks(rotation=45)
    st.pyplot(plt)
else:
    st.write("Nenhuma venda registrada.")

# Relatório 2: Vendas em Intervalo de Data
st.subheader("Vendas por Intervalo de Data")
start_date = st.date_input("Data Inicial")
end_date = st.date_input("Data Final")

if st.button("Gerar Relatório de Vendas por Data"):
    query = f"""
    SELECT produto, quantidade, preco, data
    FROM vendas
    WHERE data BETWEEN '{start_date}' AND '{end_date}'
    """
    result = query_data_from_mysql(query)
    if result:
        df_vendas_data = pd.DataFrame(result, columns=['Produto', 'Quantidade', 'Preço', 'Data'])
        st.write(df_vendas_data)
        
        # Gerando gráfico
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Data', y='Quantidade', data=df_vendas_data, marker='o')
        plt.title('Vendas ao Longo do Tempo')
        st.pyplot(plt)
    else:
        st.write("Nenhuma venda encontrada para este intervalo de datas.")

# Relatório 3: Total de Vendas
st.subheader("Total de Vendas Realizadas")
query = "SELECT SUM(quantidade * preco) AS total_vendas FROM vendas"
result = query_data_from_mysql(query)

if result:
    total_vendas = result[0][0]
    st.write(f"Total de Vendas Realizadas: R$ {total_vendas:.2f}")
else:
    st.write("Erro ao calcular o total de vendas.")
