import json
import cgi
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from Controller.ControllerComponente import ComponentService  
from Controller.ControllerProjetos import ProjetoService 
from Controller.ControllerLowCode import LowCodeService

from Controller.Auth2 import AuthService
from Middleware.Middleware import autenticar_request


UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


class SimpleAPI(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """ Adiciona cabeçalhos CORS corretamente """
        self.send_header("Access-Control-Allow-Origin", "*")  
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        
        
    def _send_response(self, status=200, data=None, location=None):
       
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()  # Chama a função que adiciona os cabeçalhos CORS corretamente
        if location:
            self.send_header("Location", location)
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))

    
    def do_POST(self):
       
        content_type = self.headers.get("Content-Type", "")
        if self.path == "/api/v1/upload" and content_type.startswith("multipart/form-data"):
            return self._handle_file_upload()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
       
        try:
            data = json.loads(post_data.decode("utf-8"))
            if self.path == '/api/v1/registro':
             
                nome = data.get("name")
                email = data.get("email")
                senha = data.get("senha")

                if not email or not senha:
                    return self._send_response(400, {"erro": "Email e senha são obrigatórios"})

                resultado = AuthService.registrar_usuario(nome,email, senha)
                if resultado:
                  login=AuthService.login(email, senha)
                  if login:
                    return self._send_response(201, login, location=f"/api/v1/auth/{resultado}")
                  else:
                    return self._send_response(400, {"erro": "erro de registro"})
            
            elif self.path == "/api/v1/login":
                email = data.get("email")
                senha = data.get("senha")

                if not email or not senha:
                    return self._send_response(400, {"erro": "Email e senha são obrigatórios"})

                resultado = AuthService.login(email, senha)
                if resultado:
                 return self._send_response(200, resultado)
                else:
                    return self._send_response(400, {"erro": "login não realizado"})

            elif self.path == "/api/v1/logout":
                auth_header = self.headers.get("Authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    return self._send_response(400, {"erro": "Token não fornecido"})

                token = auth_header.split(" ")[1]
                resultado = AuthService.logout(token)
                return self._send_response(200, resultado)  
            
            elif self.path == '/api/v1/projetos':
                user_id = autenticar_request(self) 
                if not user_id: 
                      return
                nome = data.get("name")
                id_user = data.get("id_user")
               
                if not nome:
                    return self._send_response(400, {"erro": "Nome é obrigatório"})

                projeto = ProjetoService.criar_projeto(nome, id_user)
                if projeto:
                    response_data = {
                        "mensagem": "Projeto criado com sucesso!",
                        "projeto": projeto
                    }
                    self._send_response(201, response_data, location=f"/api/v1/projetos/{projeto}")
                else:
                    self._send_response(400, {"erro": "Erro ao criar o projeto"})

            elif self.path == '/api/v1/componentes':
                user_id = autenticar_request(self) 
                if not user_id: return
                tipo = data.get("tipo")
                projeto_id = data.get("ProjectID")
                if not tipo or not projeto_id:
                    return self._send_response(400, {"erro": "Tipo e projeto_id são obrigatórios"})
                
                componente = ComponentService.criar_componente(tipo, projeto_id)
                if componente:
                    response_data = {
                        "mensagem": "Componente criado com sucesso!",
                        "componente": componente
                    }
                    self._send_response(201, response_data, location=f"/api/v1/componentes/{componente}")
                else:
                    self._send_response(400, {"erro": "Erro ao criar o componente"})
            
            else:
                self._send_response(404, {"erro": "Rota não encontrada"})

        except json.JSONDecodeError:
            print("Erro ao decodificar JSON:", post_data)  # <-- Log para verificar o JSON inválido
            self._send_response(400, {"erro": "JSON inválido"})
    
    def do_GET(self):
        user_id = autenticar_request(self) 
        if not user_id:
            return
        
        if self.path.startswith('/api/v1/projetos/'):
            projeto_id = self.path.split('/')[-1]
            if projeto_id.isdigit():
              projeto = ProjetoService.listar_projetos(projeto_id)

              if str(projeto[0]['id_user']) == str(user_id):
                 self._send_response(200, projeto)
              else:
                self._send_response(403, {"erro": "Você não tem permissão para acessar este projeto"})

            else:
                 self._send_response(404, {"erro": "Projetos não encontrado"})

 
        elif self.path.startswith('/api/v1/componentes/edit'):
            componete_id = self.path.split('/')[-1]
           
            if componete_id:
                componente = ComponentService.obter_componente(componete_id)
              
                if componente:
          
                 html=LowCodeService.get_render_settings(componente)
        
                 self._send_response(200, {"html":html, "comp":componente})
                else:
                 self._send_response(404, {"erro":"Componete não encontrado"})   
                   
            else:
                self._send_response(400, {"erro": "ID do projeto inválido"})
        
        elif self.path.startswith('/api/v1/perfil'):
            componete_id = self.path.split('/')[-1]
           
            if componete_id:
                componente = AuthService.perfil(componete_id)
                
                self._send_response(200, {"perfil":componente})  
            else:
                self._send_response(400, {"erro": "ID do projeto inválido"})

        elif self.path.startswith("/api/v1/renderComponent"):
            query_components = parse_qs(urlparse(self.path).query)
            id_projeto = self.path.split('/')[-1]
         
            if id_projeto.isdigit():
                id_user=ProjetoService.obter_projeto(id_projeto)
                
                if str(id_user) == str(user_id):
                    component = ComponentService.generate(id_projeto)
                
                    if component:
                            self._send_response(200, component)
                    else:
                            self._send_response(404, {"erro": "Projeto não encontrado"})
                else:
                  self._send_response(403, {"erro": "Você não tem permissão para acessar este projeto"})

         
        elif self.path.startswith("/api/v1/preview"):
            query_components = parse_qs(urlparse(self.path).query)
            id_projeto = self.path.split('/')[-1]
         
            if id_projeto.isdigit():
                component = ComponentService.generatePreview(id_projeto)
               
                if component:
                    self._send_response(200, component)
                else:
                    self._send_response(404, {"erro": "Projeto não encontrado"})
        
        elif self.path.startswith('/api/v1/donwload'):
            projeto_id = self.path.split('/')[-1]
           
            if projeto_id:
                caminho = ComponentService.dawloadProjet(projeto_id)
                print(caminho)
                self._send_response(200, caminho)
            else:
                self._send_response(404, {"erro": "donwload não feito"})     
                           
        else:
            self._send_response(404, {"erro": "Rota não encontrada"})   
    
    def do_PUT(self):
        user_id = autenticar_request(self) 
        if not user_id:
            return
        if self.path.startswith('/api/v1/componentes/update'):
            componente_id = self.path.split('/')[-1]
            
            if not componente_id:
                return self._send_response(400, {"erro": "ID do componente inválido"})
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode("utf-8"))

                atualizado = ComponentService.editar_componente(componente_id, data)
                html=LowCodeService.get_render_settings(data)
                self._send_response(200, {"mensagem": "Componente atualizado com sucesso", "componente": atualizado, "html":html})
               
            except json.JSONDecodeError:
                self._send_response(400, {"erro": "JSON inválido"})
                
        elif self.path.startswith('/api/v1/generateComponentHTML'):
            componente_id = self.path.split('/')[-1]
            
            if not componente_id:
                return self._send_response(400, {"erro": "ID do componente inválido"})
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                componete = json.loads(post_data.decode("utf-8"))

                component = ComponentService.generate_Component_HTML(componete)
                
                self._send_response(200, {"mensagem": "Componente atualizado com sucesso", "comp": component})
               
            except json.JSONDecodeError:
                self._send_response(400, {"erro": "JSON inválido"})
        
        else:
            self._send_response(404, {"erro": "Rota não encontrada"})

    
    def do_DELETE(self):
        user_id = autenticar_request(self) 
        if not user_id:
            return
        if self.path.startswith('/api/v1/projetos/'):
            projeto_id = self.path.split('/')[-1]
            if projeto_id.isdigit():
                sucesso = ProjetoService.deletar_projeto(int(projeto_id))
                if sucesso:
                    self._send_response(204)
                else:
                    self._send_response(404, {"erro": "Projeto não encontrado"})
            else:
                self._send_response(400, {"erro": "ID inválido"})

        elif self.path.startswith('/api/v1/componentes/'):
            componente_id = self.path.split('/')[-1]
            if componente_id:
                sucesso = ComponentService.deletar_componente(componente_id)
                if sucesso:
                    self._send_response(204)
                else:
                    self._send_response(404, {"erro": "Componente não encontrado"})
            else:
                self._send_response(400, {"erro": "ID inválido"})

        else:
            self._send_response(404, {"erro": "Rota não encontrada"})
    
    def _handle_file_upload(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

        if "file" not in form:
            return self._send_response(400, {"erro": "Nenhum arquivo enviado"})

        file_item = form["file"]

        if file_item.filename:
            file_path = os.path.join(UPLOAD_DIR, file_item.filename)

            with open(file_path, "wb") as output_file:
                output_file.write(file_item.file.read())

            return self._send_response(201, {"mensagem": "Upload bem-sucedido!", "filePath": f"uploads/{file_item.filename}"})
        
        return self._send_response(400, {"erro": "Falha ao processar o arquivo"})

    def do_OPTIONS(self):
        """ Responde a requisições OPTIONS para CORS """
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
           
def run_server(port: int = 8000, host: str = "") -> None:
    """Inicia o servidor HTTP na porta especificada."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleAPI)
    print(f"Servidor rodando em http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado")
        httpd.server_close()
        
   
if __name__ == "__main__":
    run_server()