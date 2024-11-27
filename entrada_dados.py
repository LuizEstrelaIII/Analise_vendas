import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

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
