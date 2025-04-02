import Model.crud as crud


class ProjetoService:
    @staticmethod
    def listar_projetos(id_user):
        return crud.listar_projetos(id_user)

    @staticmethod
    def obter_projeto(projeto_id):
        return crud.obter_projeto(projeto_id)

    @staticmethod
    def criar_projeto(nome,id_user):
       return crud.salvar_projeto(nome,id_user) 

    @staticmethod
    def deletar_projeto(projeto_id):
        return crud.deletar_projeto(projeto_id)
