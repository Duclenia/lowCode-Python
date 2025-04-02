import Model.crud as crud
import time
from typing import List, Dict
import Controller.salvarProjeto as salvarComponent


css_storage = {"custom_css": ""}
js_storage = {"custom_js": ""}

class ComponentService:
    
    @staticmethod
    def listar_componente_projeto(projeto_id):
       return crud.listar_componentes(projeto_id)
   
    @staticmethod
    def obter_componente(componente_id):
       return crud.retornar_componente(componente_id)
    
    @staticmethod
    def criar_componente(component_type, projeto_id):
        component=createComponent(component_type)
        if component :
          return crud.salvar_componente(component["id"], component_type, component,projeto_id)
        else:
          return None
    
    @staticmethod
    def deletar_componente(componente_id):
        return crud.deletar_componente(componente_id)
    
    @staticmethod
    def generate_Component_HTML(componete):
        return render_component(componete)
    
    @staticmethod
    def editar_componente(id, componente):
        return crud.atualizar_componente(id, componente)

    @staticmethod
    def generate(projeto_id):
      return  generate_inner_html(crud.listar_componentes(projeto_id))
    
    @staticmethod
    def generatePreview(projeto_id):
      return  generate_preview(crud.listar_componentes(projeto_id))
    @staticmethod
    def dawloadProjet(projeto_id):
      return  dawload_projets(projeto_id,crud.listar_componentes(projeto_id))


def listarContent(nome):
    return crud.listar_contents(nome)
  
def listarStyle(nome):
    return crud.listar_styles(nome)

def listarScript():
    return crud.listar_script()


def createComponent(type):            
            component_content = listarContent(type)
            component_style = listarStyle(type)
            component_id = f"component-{int(time.time() * 1000)}"
            return {
                    "id": component_id,
                    "type": type,
                    "content":component_content or {},
                    "style":  component_style or {},
                    "script": {},
                    "children": []
                }
            
            
def selected_component_function(component):
   
    component_type=component.get("type")
    
    match component_type:
        case "header":
            return content_header(component)
        case "div-banner":
            return content_banner(component)
        case "img":
            return content_image(component)
        case "p":
            return content_paragraph(component)
        case "card":
            return content_card(component)
        case "button":
            return content_button(component)
        case "video":
            return content_video(component)
        case _:
            return ""


def content_banner(component):
    """Gera HTML para um banner."""
    content = component.get("content", {})
    style = component.get("style", {})

    background = (
        f"background-image: url('{content.get('src')}'); background-size: cover; background-position: center;"
        if content.get("src")
        else f"background: {style.get('background', 'transparent')};"
    )

    return f"""
    <div style="{background}; padding:60px 20px;">
        <h1 style="color:{style.get('color', 'black')}">{content.get('title', '')}</h1>
        <p>{content.get('subtitle', '')}</p>
    </div>
    """


def content_header(component):
    """Gera HTML para um cabeçalho."""
    content = component.get("content", {})

    logo = (
        f'<img src="{content.get("logoUrl")}" alt="Logo" style="height: 40px;">'
        if content.get("logoUrl")
        else "<span>.</span>"
    )

    items_html = "".join(
        f'<li><a href="{item.get("url")}" style="color: inherit; text-decoration: none;" target="_blank">'
        f'{item.get("label")}</a></li>'
        for item in content.get("items", [])
    )

    return f"""
        {logo}
        <ul style="display: flex; list-style: none; margin: 0; padding: 0; gap: 20px;">
            {items_html}
        </ul>
    """


def content_image(component):
    """Gera HTML para uma imagem."""
    content = component.get("content", {})
    style = component.get("style", "")
   
    return f'src="{content.get("src", "")}" alt="{content.get("alt", "")}"'


def content_paragraph(component):
   content = component.get("content", {})
   return f'{content.get("title", "")}'


def content_card(component):
    """Gera HTML para um card."""
    content = component.get("content", {})

    image_html = (
        f'<img src="{content.get("src")}" alt="Avatar" class="card-img">'
        if content.get("src")
        else "<span>No Image</span>"
    )

    return f"""
    <div class="card">
        {image_html}
        <div class="card-content">
            <h3 class="card-title">{content.get("titleCard", "")}</h3>
            <p class="card-description">{content.get("conteudo", "")}</p>
        </div>
    </div>
    """


def content_button(component):
    content = component.get("content", {})
    return f'{content.get("title", "")}'


def content_video(component):
    """Gera HTML para um vídeo."""
    content = component.get("content", {})

    return f' src="{content.get("src", "")}" controls="{content.get("controls", "false")}"'



def object_to_style(style_dict: Dict[str, str]) -> str:
    """Converte um dicionário de estilos para uma string CSS."""
    return "; ".join(f"{key}: {value}" for key, value in style_dict.items())


def render_component(component: Dict) -> str:
    
    style_string = object_to_style(component.get("style", {}))
    component_id = component.get("id")
    component_type = component.get("type")
    component_script = component.get("script")
    children = component.get("children", [])

    content_component =  selected_component_function(component)

    children_html = "\n".join([ render_component(child) for child in children])

    dropzone = (
        f'<div class="dropzone" data-parent="{component_id}" '
        f'ondrop="dropWidget(event)" ondragover="allowDrop(event)"></div>'
        if component_type not in ["p", "img"] else ""
    )

    contents = ""

    if component_type == "video":
        contents = f'<{component_type} {content_component} style="{style_string}"></{component_type}>'

    elif component_type == "img":
        contents = f'<{component_type} {content_component} style="{style_string}">'

    elif component_type == "button":
        contents = f'<{component_type} class="btn btn-primary" onclick="{component_script.get("onclick")}" style="{style_string}">{content_component}</{component_type}>'

    else:
        contents = f'<{component_type} style="{style_string}">{content_component}{children_html}</{component_type}> {dropzone}'
 
    return f"""
    <div class="component" data-id="{component_id}">
        <div class="main">
            {contents}
        </div>
        <div class="component-controls">
            <button class="control-btn" onclick="editComponent('{component_id}')">Editar</button>
            <button class="control-btn delete-btn" onclick="deleteComponent('{component_id}')">Deletar</button>
        </div>
    </div>
    """


def generate_inner_html(components: List[Dict]) -> str:
    if not components:
        return "<p>Crie aqui os teus componentes</p>"

    rendered_components = "\n".join([render_component(comp) for comp in components])
    return f"{rendered_components} <div class='dropzone'></div>"



def render_component_preview(component):
  
    style_string = object_to_style(component.get("style", {}))
    component_type = component.get("type")
    component_script = component.get("script")
    children = component.get("children", [])
    script = f""" onclick="alert('Botão clicado!')" """

    content_component =  selected_component_function(component)
    children_html = "\n".join([ render_component_preview(child) for child in children])

    css_storage["custom_css"]  += f".{component_type} {{ {style_string} }}\n"
    
    if component_type == "video":
        return f'<{component_type} class="{component_type}" {content_component}></{component_type}>'

    elif component_type == "img":
        return f'<{component_type} class="{component_type}" {content_component}>'

    elif component_type == "button":
        contents = f'<{component_type} class="btn btn-primary" onclick="{component_script.get("onclick")}" style="{style_string}">{content_component}</{component_type}>'

    else:
        return f'<{component_type} class="{component_type}">{content_component}{children_html}</{component_type}>'

def generate_preview(components: List[Dict]) -> str:
  
    generated_html = "\n".join([render_component_preview(comp) for comp in components])
    
    export_panel_html = f"""
        <h2>Código Gerado</h2>
        <style>{css_storage["custom_css"] }</style>
        <body><div class='main'>{generated_html}</div></body>
    """
    return export_panel_html

def dawload_projets(projeto_id,components: List[Dict]) -> str:
    
    generated_html = "\n".join([render_component_preview(comp) for comp in components])
    
    return salvarComponent.save_html_file(projeto_id,css_storage["custom_css"],generated_html)
   




