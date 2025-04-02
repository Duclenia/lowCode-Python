import Middleware.conexao as conexao
import json

def conectar():
    con = conexao.conectar()
    cursor = con.cursor()
    return con, cursor

def salvar_componente(id, nome, dados_json, id_projeto):
    con, cursor = conectar()
    sql = "INSERT INTO componentes (id, tipo, dados, projeto_id) VALUES (%s, %s, %s, %s)"
    valores = (id, nome, json.dumps(dados_json), id_projeto) 
    cursor.execute(sql, valores)
    con.commit()
    print("Componente salvo com sucesso!")
    cursor.close()
    con.close()
    
def salvar_projeto(nome, id_user):
    con, cursor = conectar()
    sql = "INSERT INTO projetos (nome, id_user) VALUES (%s, %s)"
    valores = (nome, id_user) 
    cursor.execute(sql, valores)
    con.commit()
    project_id = cursor.lastrowid
    print("projeto salvo com sucesso!")
    cursor.close()
    con.close()  
    return project_id
      
def obter_projeto(id_projeto):
    con, cursor = conectar()
    cursor.execute("SELECT id_user, id FROM projetos WHERE id = %s", (id_projeto,))
    projeto = cursor.fetchone()
    cursor.close()
    con.close()
    
    if projeto:
        return projeto[0]  
    else:
        return None
    
def listar_componentes(id_projeto):
    con, cursor = conectar()
    cursor.execute("SELECT dados FROM componentes WHERE projeto_id = %s", (id_projeto,))
    componentes = cursor.fetchall()
    cursor.close()
    con.close()
    if componentes:
        # Transformar a lista de tuplas em uma lista de dicionários
        return [json.loads(dado[0]) for dado in componentes]
    else:
        return []

def atualizar_componente(id_componente, novos_dados):
    con, cursor = conectar()
    sql = "UPDATE componentes SET dados = %s WHERE id = %s"
    valores = (json.dumps(novos_dados), id_componente)
    cursor.execute(sql, valores)
    con.commit()
    print("Componente atualizado com sucesso!")
    cursor.close()
    con.close()

def deletar_componente(id_componente):
    con, cursor = conectar()
    sql = "DELETE FROM componentes WHERE id = %s"
    cursor.execute(sql, (id_componente,))
    con.commit()
    print("Componente deletado com sucesso!")
    cursor.close()
    con.close()
    
def deletar_projeto(id_componente):
    con, cursor = conectar()
    sql = "DELETE FROM projetos WHERE id = %s"
    cursor.execute(sql, (id_componente,))
    con.commit()
    print("projeto deletado com sucesso!")
    cursor.close()
    con.close() 
       
def retornar_componente(id_componente):
    con, cursor = conectar()
    cursor.execute("SELECT id, tipo, dados FROM componentes WHERE id = %s", (id_componente,))
    componente = cursor.fetchone()
    cursor.close()
    con.close()
    
    if componente:
        return json.loads(componente[2])  
    else:
        return None

def retornar_componente_type(type):
    con, cursor = conectar()
    cursor.execute("SELECT id, tipo, dados FROM componentes WHERE tipo = %s", (type))
    componente = cursor.fetchone()
    cursor.close()
    con.close()
    
    if componente:
        return json.loads(componente[2])  
    else:
        return None
        

def listar_contents(nome):

    con, cursor = conectar()
    cursor.execute("SELECT data FROM contents WHERE name = %s", (nome,)) 
    contents = cursor.fetchone()
    cursor.close()
    con.close()
    
    if contents:
       return json.loads(contents[0])
    else:
        return None

def listar_styles(nome):
    con, cursor = conectar()
    cursor.execute("SELECT data FROM styles WHERE name = %s", (nome,))
    style = cursor.fetchone()
    cursor.close()
    con.close()
    
    if style:
        return json.loads(style[0])
    else:
        return None


def listar_projetos(id_user):
    con, cursor = conectar()
    cursor.execute("SELECT id, nome,id_user, created_at FROM projetos WHERE id_user = %s", (id_user,))
    projetos = cursor.fetchall()
    
    cursor.close()
    con.close()

    return [{"id_user": str(dado[2]),"nome": str(dado[1]),"id":str(dado[0]), "created_at": dado[3].strftime('%Y-%m-%d %H:%M:%S')} for dado in projetos] if projetos else []



def listar_script():
    id=1
    con, cursor = conectar()
    cursor.execute("SELECT dados FROM script WHERE id = %s", (id,))
    style = cursor.fetchone()
    cursor.close()
    con.close()
    
    if style:
        return json.loads(style[0])
    else:
        return None