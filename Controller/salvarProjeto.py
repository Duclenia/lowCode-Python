import os
import shutil
from pathlib import Path

def save_html_file(projeto, custom_css, generated_html):
    downloads_dir = str(Path.home() / "Downloads")
    

    site_folder = os.path.join(downloads_dir, f"site_gerado_{projeto}")
    css_folder = os.path.join(site_folder, "css")
    js_folder = os.path.join(site_folder, "js")
    uploads_folder = os.path.join(site_folder, "uploads") 

    os.makedirs(css_folder, exist_ok=True)
    os.makedirs(js_folder, exist_ok=True)
    os.makedirs(uploads_folder, exist_ok=True) 

 
    html_file_path = os.path.join(site_folder, "index.html")
    css_file_path = os.path.join(css_folder, "styles.css")

    source_css_folder = "static/css"  
    if os.path.exists(source_css_folder):
        for file_name in os.listdir(source_css_folder):
            src_file = os.path.join(source_css_folder, file_name)
            dest_file = os.path.join(css_folder, file_name)
            shutil.copy2(src_file, dest_file)
            
    with open(css_file_path, "w", encoding="utf-8") as css_file:
        css_file.write("""    
                * { box-sizing: border-box; margin: 0;padding: 0; }

                body { font-family: Arial, sans-serif; }
                """+ custom_css)

  
    bootstrapCDN = """ <link href="css/animate.css" rel="stylesheet">
    <link href="css/all.min.css" rel="stylesheet">
    <link href="css/bootstrap-icons.css" rel="stylesheet">
    <link href="css/bootstrap.min.css" rel="stylesheet">"""

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Gerado</title>
    {bootstrapCDN}
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    {generated_html}
</body>
</html>"""

    # Salvar o arquivo HTML
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    upload_source_folder = "uploads"  
    if os.path.exists(upload_source_folder):
        for file_name in os.listdir(upload_source_folder):
            src_file = os.path.join(upload_source_folder, file_name)
            dest_file = os.path.join(uploads_folder, file_name)
            shutil.copy2(src_file, dest_file)  

    print(f"Arquivos salvos com sucesso em: {site_folder}")
    return site_folder
