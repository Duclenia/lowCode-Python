let selectedComponent = null;

const params = new URLSearchParams(window.location.search);
let projetoID = params.get('id');


function dragWidget(event, type) {
    event.dataTransfer.setData('text/plain', type);
    event.dataTransfer.effectAllowed = 'move';
}

function allowDrop(event) {
    event.preventDefault();
    const dropzone = findClosestDropzone(event.target);
    if (dropzone) dropzone.classList.add('active');
}

function findClosestDropzone(element) {
    if (!element) return null;
    if (element.classList.contains('dropzone')) return element;
    if (element.id === 'preview') return element;
    return findClosestDropzone(element.parentElement);
}

async function dropWidget(event) {
    event.preventDefault();
    const type = event.dataTransfer.getData('text/plain');
    if (!type) return;

    const dropzone = findClosestDropzone(event.target);
    if (!dropzone) return;

    const component = createComponet(type);
    if (!component) return;

    document.querySelectorAll('.dropzone').forEach(zone => zone.classList.remove('active'));

    selectedComponent = component;
}

async function fetchComponents() {

    try {
        const response = await fetch(`${API_URL}/renderComponent/${projetoID}`, {
            headers: {
                "Authorization": `Bearer ${getToken()}`
            }
        });
        const data = await response.json();
        document.getElementById("preview").innerHTML = data;

    } catch (error) {
        console.error("Erro ao buscar componentes:", error);
        return [];
    }
}

function renderSettings(html) {
    const settings = document.getElementById('settings');
    settings.innerHTML = html;
}

async function updateComponentProperty(componentId, propertyPath, value) {

   
    if (!selectedComponent) return;

    if(propertyPath=="onclick"){
        selectedComponent.script = {
            onclick: value 
        };
    
    }else{

    if (value instanceof FileList && value.length > 0) {
        value = await uploadFile();
    }
    let keys = propertyPath.split(".");
    let obj = selectedComponent;

    for (let i = 0; i < keys.length - 1; i++) {
        obj = obj[keys[i]];
        if (!obj) return;
    }
    keys
    obj[keys[keys.length - 1]] = value;
    }
    const updatedHTML = await generateComponentHTML(selectedComponent);
    document.querySelector(`[data-id="${selectedComponent.id}"]`).innerHTML =updatedHTML;
}

async function uploadFile() {
    const fileInput = document.getElementById("file-upload");
    if (!fileInput.files.length) {
        alert("Selecione um arquivo!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${getToken()}`
        },
        body: formData
    });

    const result = await response.json();
    console.log("Resultado:", result.filePath);
    return result.filePath;   
}

async function addMenuItem(componentId) {
    
    if (selectedComponent) {
        selectedComponent.content.items.push({ label: '', url: '' });
       saveEditedComponent();
    }
}
async function removeMenuItem(componentId, index) {
    if (selectedComponent) {
        selectedComponent.content.items.splice(index, 1); 
       
        saveEditedComponent();
    }
}
async function addScript(componentId, propertyPath, value) {
    if (selectedComponent) {
        
       selectedComponent.script={propertyPath : `"${propertyPath}"`};
        saveEditedComponent();
    }
}
function createComponet(type) {
    fetch(`${API_URL}/componentes`, {
        method: "POST",
        headers: {"Authorization": `Bearer ${getToken()}`, "Content-Type": "application/json" },
        body: JSON.stringify({ "tipo": type, "ProjectID": projetoID })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Componente criado:", data);
            fetchComponents();
        })
        .catch(error => console.error("Erro ao criar componente:", error));
}

async function editComponent(componentId) {
    try {
        const response = await fetch(`${API_URL}/componentes/edit/${componentId}`,{headers: { "Authorization": `Bearer ${getToken()}`}});
        const res = await response.json();

        selectedComponent = res.comp;
        renderSettings(res.html);

    } catch (res) {
        console.error("Erro ao buscar projetos:", res);
        alert("Erro ao carregar projetos.");
    }
}

async function generateComponentHTML(componente) {
    try {
        const response = await fetch(`${API_URL}/generateComponentHTML/${componente.id}`, {
            method: 'PUT',
            headers: {"Authorization": `Bearer ${getToken()}`, "Content-Type": "application/json" },
            body: JSON.stringify(componente)
        });

        if (!response.ok) {
            throw new Error("Erro ao atualizar componente");
        }
        const data = await response.json();
        return data.comp; 
    } catch (error) {
        alert("Erro ao carregar projetos.");
        return null;
    }
}

async function saveEditedComponent() {

    if (!selectedComponent) return;

    const response = await fetch(`${API_URL}/componentes/update/${selectedComponent.id}`, {
        method: 'PUT',
        headers: { "Authorization": `Bearer ${getToken()}`,"Content-Type": "application/json" },
        body: JSON.stringify(selectedComponent)
    });

    const data = await response.json();
    alert("Projeto atualizado com sucesso!");
            fetchComponents();
            renderSettings(data.html);
            selectedComponent = null;
       }

async function cancelEditComponent() {
   
    if (!selectedComponent) return;
   
      window.location.reload();
      selectedComponent = null;
}

function deleteComponent(componentId) {
    fetch(`${API_URL}/componentes/${componentId}`, {
        method: 'DELETE',
        headers: {
            "Authorization": `Bearer ${getToken()}`
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log("Componente eliminado:", data);
            fetchComponents();
        })
        .catch(error => console.error("Erro ao eliminar componente:", error));
}

async function saveProject() {
    try {
        const response = await fetch(`${API_URL}/donwload/${projetoID}`,
            { headers: {
            "Authorization": `Bearer ${getToken()}`
        }});
        const res = await response.json();
        alert("Projeto salvo com sucesso, em:", res);

    } catch (res) {
        console.error("Erro ao salvar projetos:", res);
        alert("Erro ao salvar projetos.");
    }
}

async function generateCode() {
    try {
        const res = await fetch(`${API_URL}/preview/${projetoID}`,{headers: { "Authorization": `Bearer ${getToken()}`}});
        const html = await res.json();
        document.querySelector('.export-panel').innerHTML = html;
        document.getElementById('saveProjectBtn').style.display = 'inline-block';
        alert("Código gerado com sucesso!");

    } catch (error) {
        alert("Erro ao gerar codigo", html);

    }
}
window.onload = fetchComponents;

document.addEventListener("DOMContentLoaded", function () {
          
   const token = getAuth();
    
    if (!token) {
        window.location.href = "index.html";
    } 
});