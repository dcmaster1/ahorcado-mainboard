const ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ".split("");

document.addEventListener("DOMContentLoaded", () => {
    crearTeclado();
    actualizarEstado();
});

function crearTeclado() {
    const contenedor = document.getElementById("teclado");
    contenedor.innerHTML = "";
    
    ALFABETO.forEach(letra => {
        const btn = document.createElement("button");
        btn.innerText = letra;
        btn.classList.add("key-btn");
        btn.id = `key-${letra}`;
        btn.onclick = () => enviarLetra(letra);
        contenedor.appendChild(btn);
    });
}

async function actualizarEstado() {
    const res = await fetch('/api/estado');
    const data = await res.json();
    renderizar(data);
}

async function enviarLetra(letra) {
    const res = await fetch('/api/intentar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letra })
    });
    const data = await res.json();
    renderizar(data);
}

async function reiniciarJuego() {
    const res = await fetch('/api/reiniciar', { method: 'POST' });
    const data = await res.json();
    
    ALFABETO.forEach(letra => {
        const btn = document.getElementById(`key-${letra}`);
        if (btn) btn.disabled = false;
    });
    
    renderizar(data);
}

function renderizar(data) {
    document.getElementById("palabra-display").innerText = data.palabra_oculta;
    document.getElementById("intentos").innerText = data.intentos_restantes;

    // Actualizar la lista de pistas visuales en pantalla
    const listaPistas = document.getElementById("lista-pistas");
    listaPistas.innerHTML = "";
    
    if (data.pistas.length === 0) {
        const li = document.createElement("li");
        li.innerText = "Acumula errores para desbloquear pistas (Pista 1 a los 2 errores, Pista 2 a los 4 errores).";
        listaPistas.appendChild(li);
    } else {
        data.pistas.forEach((pista, index) => {
            const li = document.createElement("li");
            li.innerText = `Pista ${index + 1}: ${pista}`;
            listaPistas.appendChild(li);
        });
    }

    // Gestionar la animacion del monigote segun los errores cometidos
    const errores = 6 - data.intentos_restantes;
    for (let i = 1; i <= 6; i++) {
        const parte = document.getElementById(`part-${i}`);
        if (parte) {
            if (i <= errores) {
                parte.classList.remove("hidden");
            } else {
                parte.classList.add("hidden");
            }
        }
    }

    data.letras_usadas.forEach(letra => {
        const btn = document.getElementById(`key-${letra}`);
        if (btn) btn.disabled = true;
    });

    const msgDiv = document.getElementById("mensaje");
    if (data.ganado) {
        msgDiv.innerText = "Felicidades, ganaste el juego";
        msgDiv.className = "message win";
        deshabilitarTodoElTeclado();
    } else if (data.perdido) {
        msgDiv.innerText = `Perdiste. La respuesta era: ${data.palabra_revelada}`;
        msgDiv.className = "message lose";
        deshabilitarTodoElTeclado();
    } else {
        msgDiv.innerText = "";
    }
}

function deshabilitarTodoElTeclado() {
    ALFABETO.forEach(letra => {
        const btn = document.getElementById(`key-${letra}`);
        if (btn) btn.disabled = true;
    });
}