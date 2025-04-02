from Controller.Auth2 import AuthService


def autenticar_request(handler):
    auth_header = handler.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
         handler._send_response(400, {"erro": "Token não fornecido"})
         return None

    token = auth_header.split(" ")[1]
    user_id = AuthService.verificar_token(token)  
    
    if not user_id:
        handler._send_response(403, {"erro": "Acesso negado: token inválido ou expirado"})
        return None
    
    return user_id 
