import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Senha padrão do XAMPP
        database="lowcode",
        port=3306
    )
    return conexao
