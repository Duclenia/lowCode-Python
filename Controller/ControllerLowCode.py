import json

class LowCodeService:
    
    @staticmethod
    def get_render_settings(component):
        return render_settings(component)
    
    @staticmethod
    def update_component_property(component):
        return 1
    
    
def render_settings(component):
    html = f"""
          <h3>{component['type'].capitalize()}</h3>
          <div class="settings-group">
              <h3>Conteúdo</h3>
              {render_component_content(component)}
          </div>
          <div class="settings-group">
              <h3>Estilos</h3>
              {render_style_settings(component)}
              <button onclick="saveEditedComponent()">Salvar</button>
               <button onclick="cancelEditComponent()">Cancelar</button>

          </div>
      """
    return html

def render_component_content(component):
    component_type = component["type"]
    if component_type == "div-banner":
        return f"""
        {generate_input('Título:', 'content', 'title', 'text', component)}
        {generate_input('Subtítulo:', 'content', 'subtitle', 'text', component)}
        {generate_input('Imagem de Fundo (URL):', 'content', 'src', 'text', component)}
        {generate_input('Ou faça upload de uma imagem:', 'content', 'src', 'file', component)}
        """
    if component_type == "p":
        return f"""
        {generate_input('texto:', 'content', 'title', 'text', component)}
        """  
    
    elif component_type == "card":
        return f"""
        {generate_input('URL da Imagem:', 'content', 'imageCard', 'text', component)}
        {generate_input('Ou faça upload de uma imagem:', 'content', 'imageCard', 'file', component)}
        {generate_input('Título Card:', 'content', 'titleCard', 'text', component)}
        {generate_input('Imagem de Fundo (URL):', 'content', 'backgroundImage', 'text', component)}
        <div class="property-field">
            <label>Conteúdo:</label>
            <textarea rows="2" onchange="updateContentCard('{component['id']}', 'conteudo', this.value)">
                {component['content'].get('conteudo', '')}
            </textarea>
        </div>
        """
    
    elif component_type == "footer":
        return generate_input('Texto do footer:', 'content', 'title', 'text', component)

    elif component_type == "img":
        return f"""
        {generate_input('URL da Imagem:', 'content', 'src', 'text', component)}
        {generate_input('Ou faça upload de uma imagem:', 'content', 'src', 'file', component)}
        {generate_input('Texto Alternativo:', 'content', 'alt', 'text', component)}
        """
    elif component_type == "button":
        return f"""
        {generate_input('Texto:', 'content', 'title', 'text', component)}
        {generate_input('Script:', 'script', 'onclick', 'select', component, ['Nunhum',"alert('Botão clicado!')"])}
          """
    
    elif component_type == "header":
        menu_items = "".join(
            f"""
            <div class="menu-item">
                <input type="text" value="{item['label']}" 
                    onchange="updateComponentProperty('{component['id']}', 'content.items.{index}.label', this.value)" 
                    placeholder="Nome do item">
                <input type="text" value="{item['url']}" 
                    onchange="updateComponentProperty('{component['id']}', 'content.items.{index}.url', this.value)" 
                    placeholder="URL do item">
                <button class="btn btn-danger" onclick="removeMenuItem('{component['id']}', {index})">Remover</button>
            </div>
            """
            for index, item in enumerate(component['content'].get('items', []))
        )

        return f"""
        {generate_input('Logo (URL):', 'content', 'logoUrl', 'text', component)}
        <div class="property-field">
            <label>Itens de Menu:</label>
            {menu_items}
        </div>
        <button class="btn btn-success" onclick="addMenuItem('{component['id']}')">Adicionar Link</button>
        """

def render_style_settings(component):
    component_type = component["type"]
    
    common_styles = f"""
        {generate_input('Padding', 'style', 'padding', 'text', component)}
        {generate_input('Margin (px)', 'style', 'margin', 'text', component)}
        {generate_input('Background', 'style', 'background', 'color', component)}
        {generate_input('Color', 'style', 'color', 'color', component)}
        {generate_input('Fonte', 'style', 'font-size', 'text', component)}
    """
    
    style_options = {
        "header": common_styles + generate_input('Gap', 'style', 'gap', 'text', component),
        "div-banner": common_styles + generate_input('Alinhamento do texto:', 'style', 'text-align', 'select', component, ['center', 'justify', 'left']),
        "card": common_styles + generate_input('Tamanho:', 'style', 'width', 'text', component),
        "video": common_styles + generate_input('Altura', 'style', 'height', 'text', component) + generate_input('Largura', 'style', 'width', 'text', component),
        "img": generate_input('Altura(%)', 'style', 'max-height', 'text', component) + generate_input('Largura (%)', 'style', 'max-width', 'text', component),
        "footer": common_styles + generate_input('Alinhamento do texto:', 'style', 'text-align', 'select', component, ['center', 'justify', 'left']),
        "section": common_styles + generate_input('Altura', 'style', 'height', 'text', component) + generate_input('Largura', 'style', 'width', 'text', component),
        "p": common_styles,
        "button" : common_styles
        }

    return style_options.get(component_type, "")

def generate_input(label, attribute, property, input_type="text", component=None, options=None):
    value = component.get(attribute, {}).get(property, "")
    
    if input_type == "select":
        options_html = "".join(f'<option value="{opt}" {"selected" if value == opt else ""}>{opt}</option>' for opt in options)
        return f"""
        <div class="property-field">
            <label for="{property}">{label}:</label>
            <select id="{property}" onchange="updateComponentProperty('{component['id']}', '{property}', this.value)">
                {options_html}
            </select>
        </div>
        """
    
    elif input_type == "file":
        return f"""
        <div class="property-field">
            <label for="file-upload">{label}</label>
            <input type="file" id="file-upload" accept="image/*" onchange="updateComponentProperty('{component['id']}', 'content.{property}', this.files)">
        </div>
        """

    return f"""
    <div class="property-field">
        <label>{label}:</label>
        <input type="{input_type}" value="{value}" onchange="updateComponentProperty('{component['id']}', '{attribute}.{property}', this.value)">
    </div>
    """

def update_component_property(component, property_path, value):
    keys = property_path.split(".")
    obj = component

    for key in keys[:-1]:
        obj = obj.setdefault(key, {})  

    obj[keys[-1]] = value
    return component 
