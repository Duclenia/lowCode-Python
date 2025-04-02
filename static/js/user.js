const API_URL = "http://localhost:8000/api/v1";

async function loginUser(email, senha) {

    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, senha: senha })
    });

    const data = await response.json();

    if (data.token) {
        localStorage.setItem("token", data.token); 
        localStorage.setItem("user_id", data.id);

        alert("Login realizado com sucesso!");

        window.location.href = "projeto.html";
    } else {
        alert(data.erro);
    }
}
async function registerUser() {
    const nome = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("password").value.trim();
    if (!nome) {
        alert("O nome é obrigatório.");
        return;
    }

    const response = await fetch(`${API_URL}/registro`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: nome, email: email, senha: senha })
    });

    const data = await response.json();
    if (data.token) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("user_id", data.id);

        alert("Registro realizado com sucesso!");
        window.location.href = "projeto.html";
    } else {
        alert(data.erro);
    }
}

async function logout() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Você não está logado!");
        
        return;
    }
    const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name: "b" })
    });

    const data = await response.json();
    alert(data.mensagem || data.erro);

    if (response.ok) {
        localStorage.removeItem("token");
        localStorage.removeItem("user_id"); 
        window.location.href = "index.html";
        
    }
}

function getAuth() {
    return localStorage.getItem("user_id");
}
function getToken() {
    return localStorage.getItem("token");
}