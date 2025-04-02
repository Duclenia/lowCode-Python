import hashlib
import time
import base64
import os
import Middleware.conexao as conexao

import json
class AuthService:

    @staticmethod
    def conectar_db():
     con = conexao.conectar()
     cursor = con.cursor(dictionary=True) 
     return con, cursor

    @staticmethod
    def hash_senha(senha):
      
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def gerar_token():
       
        random_bytes = os.urandom(16)  # Gera bytes aleatórios
        timestamp = str(time.time()).encode()  # Adiciona tempo para tornar único
        return base64.b64encode(random_bytes + timestamp).decode()

    @staticmethod
    def registrar_usuario(nome, email, senha):
       
        con, cursor = AuthService.conectar_db()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            con.close()
            return {"erro": "Usuário já existe"}

        senha_hash = AuthService.hash_senha(senha)

        cursor.execute("INSERT INTO users (nome,email, senha) VALUES (%s,%s, %s)", (nome,email, senha_hash))
        con.commit()
        con.close()
        return {"mensagem": "Usuário registrado com sucesso"}

    @staticmethod
    def login(email, senha):
        con, cursor = AuthService.conectar_db()

        if not con.is_connected():  # Verifica se a conexão está ativa
            con, cursor = AuthService.conectar_db()

        cursor.execute("SELECT id, senha FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or AuthService.hash_senha(senha) != user["senha"]:
            con.close()
            return {"erro": "Email ou senha inválidos"}

        # Gera um token
        token = AuthService.gerar_token()

        # Salva a sessão no banco
        cursor.execute("INSERT INTO sessions (user_id, token) VALUES (%s, %s)", (user["id"], token))
        con.commit()
        con.close()

        return {"token": token, "id": user["id"]}

    @staticmethod
    def verificar_token(token):
     
        con, cursor = AuthService.conectar_db()

        cursor.execute("SELECT user_id FROM sessions WHERE token = %s", (token,))
        session = cursor.fetchone()
        con.close()

        return session["user_id"] if session else None
       

    @staticmethod
    def logout(token):
    
        con, cursor = AuthService.conectar_db()
        cursor.execute("DELETE FROM sessions WHERE token = %s", (token,))
        con.commit()
        con.close()
        return {"mensagem": "Logout realizado com sucesso"}

    @staticmethod
    def perfil(id_user):
        
        con, cursor = AuthService.conectar_db()
        cursor.execute("SELECT created_at, user_id FROM sessions WHERE user_id = %s", (id_user,))
        componentes = cursor.fetchall()
        cursor.close()
        con.close()

        if componentes:
           return [{"created_at": dado["created_at"].strftime('%Y-%m-%d %H:%M:%S') if dado["created_at"] else None} for dado in componentes]
        else:
            return []



