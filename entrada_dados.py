import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
import pandas as pd
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
            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco de dados!")
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao inserir os dados: {e}")
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
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao consultar o banco de dados: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Função para gerar gráficos de vendas
def generate_sales_graph(data):
    df = pd.DataFrame(data, columns=['Produto', 'Total de Vendas'])
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Produto', y='Total de Vendas', data=df)
    plt.title('Vendas Totais por Produto')
    plt.xticks(rotation=45)
    plt.show()

# Função para carregar e inserir CSV no banco de dados
def load_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        try:
            df = pd.read_csv(filepath)
            messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso.")
            
            # Inserir os dados carregados no banco de dados
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
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco de dados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o CSV: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Função para exibir relatórios de vendas
def show_sales_report():
    query = "SELECT produto, SUM(quantidade) AS total_vendas FROM vendas GROUP BY produto"
    result = query_data_from_mysql(query)

    if result:
        df_vendas_produto = pd.DataFrame(result, columns=['Produto', 'Total de Vendas'])
        print(df_vendas_produto)
        
        # Gerando gráfico
        generate_sales_graph(result)
    else:
        messagebox.showinfo("Resultado", "Nenhuma venda registrada.")

# Função para exibir vendas por intervalo de data
def show_sales_by_date(start_date, end_date):
    query = f"""
    SELECT produto, quantidade, preco, data
    FROM vendas
    WHERE data BETWEEN '{start_date}' AND '{end_date}'
    """
    result = query_data_from_mysql(query)

    if result:
        df_vendas_data = pd.DataFrame(result, columns=['Produto', 'Quantidade', 'Preço', 'Data'])
        print(df_vendas_data)
        
        # Gerando gráfico
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Data', y='Quantidade', data=df_vendas_data, marker='o')
        plt.title('Vendas ao Longo do Tempo')
        plt.xticks(rotation=45)
        plt.show()
    else:
        messagebox.showinfo("Resultado", "Nenhuma venda encontrada para este intervalo de datas.")

# Função para exibir total de vendas
def show_total_sales():
    query = "SELECT SUM(quantidade * preco) AS total_vendas FROM vendas"
    result = query_data_from_mysql(query)

    if result:
        total_vendas = result[0][0]
        messagebox.showinfo("Total de Vendas", f"Total de Vendas Realizadas: R$ {total_vendas:.2f}")
    else:
        messagebox.showerror("Erro", "Erro ao calcular o total de vendas.")

# Função principal da interface Tkinter
def main():
    global start_date_entry, end_date_entry  # Declarando como variáveis globais para acesso em funções

    root = tk.Tk()
    root.title("Sistema de Vendas")

    # Interface para inserir dados manualmente
    def show_insert_data():
        produto = produto_entry.get()
        quantidade = quantidade_entry.get()
        preco = preco_entry.get()
        data = data_entry.get()

        if produto and quantidade and preco and data:
            insert_data_to_mysql(produto, int(quantidade), float(preco), data)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

    # Widgets de entrada manual
    tk.Label(root, text="Produto:").pack()
    produto_entry = tk.Entry(root)
    produto_entry.pack()

    tk.Label(root, text="Quantidade Vendida:").pack()
    quantidade_entry = tk.Entry(root)
    quantidade_entry.pack()

    tk.Label(root, text="Preço Unitário:").pack()
    preco_entry = tk.Entry(root)
    preco_entry.pack()

    tk.Label(root, text="Data da Venda (YYYY-MM-DD):").pack()
    data_entry = tk.Entry(root)
    data_entry.pack()

    insert_button = tk.Button(root, text="Inserir Dados", command=show_insert_data)
    insert_button.pack()

    # Botão para carregar CSV
    load_button = tk.Button(root, text="Carregar Arquivo CSV", command=load_csv)
    load_button.pack()

    # Botões de relatório
    report_button = tk.Button(root, text="Vendas Totais por Produto", command=show_sales_report)
    report_button.pack()

    tk.Label(root, text="Data Inicial (YYYY-MM-DD):").pack()
    start_date_entry = tk.Entry(root)
    start_date_entry.pack()

    tk.Label(root, text="Data Final (YYYY-MM-DD):").pack()
    end_date_entry = tk.Entry(root)
    end_date_entry.pack()

    date_report_button = tk.Button(root, text="Gerar Relatório de Vendas por Data", 
                                   command=lambda: show_sales_by_date(start_date_entry.get(), end_date_entry.get()))
    date_report_button.pack()

    total_sales_button = tk.Button(root, text="Total de Vendas", command=show_total_sales)
    total_sales_button.pack()

    root.mainloop()

# Inicia a aplicação
if __name__ == "__main__":
    main()
