document.addEventListener("DOMContentLoaded", () => {
    cargarEstado();
    construirTeclado();
});

function cargarEstado() {
    fetch('/api/state')
        .then(response => response.json())
        .then(data => actualizarInterfaz(data));
}

function enviarLetra(letra) {
    fetch('/api/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letter: letra })
    })
    .then(response => response.json())
    .then(data => actualizarInterfaz(data));
}

function reiniciarJuego() {
    fetch('/api/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById("message").innerText = "";
            document.getElementById("message").className = "message";
            actualizarInterfaz(data);
            habilitarTeclado(true);
        });
}

function actualizarInterfaz(data) {
    // Mostrar la palabra oculta
    document.getElementById("palabra-display").innerText = data.hidden_word;
    
    // Mostrar la pregunta descriptiva
    document.getElementById("question-container").innerText = "Pregunta: " + data.question;

    // Actualizar intentos restantes
    document.getElementById("intentos").innerText = data.max_errors - data.errors;

    // Actualizar partes del monigote según los errores (1 a 6)
    for (let i = 1; i <= 6; i++) {
        const parte = document.getElementById(`part-${i}`);
        if (parte) {
            if (i <= data.errors) {
                parte.classList.remove("hidden");
            } else {
                parte.classList.add("hidden");
            }
        }
    }

    // Manejo de pistas
    const hintsContainer = document.getElementById("hints-container");
    const hintsList = document.getElementById("hints-list");
    hintsList.innerHTML = "";
    
    if (data.hints.length > 0) {
        hintsContainer.style.display = "block";
        data.hints.forEach(hint => {
            const li = document.createElement("li");
            li.innerText = hint;
            hintsList.appendChild(li);
        });
    } else {
        hintsContainer.style.display = "none";
    }

    // Actualizar estado del teclado virtual
    const botones = document.querySelectorAll(".key-btn");
    botones.forEach(btn => {
        const letra = btn.innerText;
        if (data.guessed.includes(letra)) {
            btn.disabled = true;
        } else {
            if (!data.won && !data.lost) {
                btn.disabled = false;
            }
        }
    });

    // Mensajes de fin de juego
    const msgDiv = document.getElementById("message");
    if (data.won) {
        msgDiv.innerText = "¡Felicitaciones! Has adivinado el componente.";
        msgDiv.className = "message win";
        habilitarTeclado(false);
    } else if (data.lost) {
        msgDiv.innerText = `¡Juego Terminado! La respuesta era: ${data.word_to_reveal}`;
        msgDiv.className = "message lose";
        habilitarTeclado(false);
    }
}

function construirTeclado() {
    const tecladoDiv = document.getElementById("keyboard");
    tecladoDiv.innerHTML = "";
    const letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for (let letra of letras) {
        const btn = document.createElement("button");
        btn.innerText = letra;
        btn.classList.add("key-btn");
        btn.onclick = () => {
            btn.disabled = true;
            enviarLetra(letra);
        };
        tecladoDiv.appendChild(btn);
    }
}

function habilitarTeclado(habilitar) {
    const botones = document.querySelectorAll(".key-btn");
    botones.forEach(btn => {
        if (habilitar) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    });
}