from flask import Flask, render_template, jsonify, session, request
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_seis_de_octubre'

# Lista de 10 componentes de la placa madre con sus preguntas y pistas específicas
COMPONENTES_DATA = [
    {
        "word": "RAM",
        "question": "¿Memoria de acceso aleatorio volátil donde se cargan temporalmente las aplicaciones en ejecución?",
        "hints": ["Es una memoria de lectura y escritura rápida.", "Pierde toda su información al apagar el equipo."]
    },
    {
        "word": "SOCKET",
        "question": "¿Zócalo o contenedor físico en la placa madre donde se instala y fija el procesador?",
        "hints": ["Tiene pines o contactos metálicos específicos.", "Su diseño y tamaño varían según la generación del CPU."]
    },
    {
        "word": "PROCESADOR",
        "question": "¿Unidad central de procesamiento (CPU), considerada el cerebro principal de todo el sistema?",
        "hints": ["Interpreta las instrucciones del software y realiza cálculos.", "Genera altas temperaturas y requiere un disipador dedicado."]
    },
    {
        "word": "CHIPSET",
        "question": "¿Conjunto de circuitos integrados que contralan el flujo de datos entre el procesador y los periféricos?",
        "hints": ["Tradicionalmente dividido en puente norte y puente sur.", "Administra los buses de comunicación de la placa base."]
    },
    {
        "word": "ATX",
        "question": "¿Factor de forma y estándar de diseño físico y energético más común en placas base y fuentes?",
        "hints": ["Define las dimensiones de la placa y distribución de tornillos.", "Introdujo el control de encendido por software (Soft-off)."]
    },
    {
        "word": "BIOS",
        "question": "¿Sistema básico de entrada/salida almacenado en una memoria ROM que arranca el hardware?",
        "hints": ["Realiza la comprobación inicial de componentes (POST) al encender.", "Permite configurar los parámetros esenciales de la placa madre."]
    },
    {
        "word": "DISIPADOR",
        "question": "¿Bloque metálico con aletas encargado de absorber y transferir el calor de componentes críticos?",
        "hints": ["Suele fabricarse de aluminio o cobre.", "Trabaja en conjunto con un ventilador (cooler) para enfriamiento."]
    },
    {
        "word": "SATA",
        "question": "¿Interfaz de bus en serie estándar para conectar unidades de almacenamiento modernas como SSD y HDD?",
        "hints": ["Sucedió a la antigua interfaz IDE con cables más delgados.", "Transmite datos a altas velocidades de transferencia."]
    },
    {
        "word": "IDE",
        "question": "¿Antigua interfaz de conexión paralela utilizada para conectar discos duros y unidades ópticas?",
        "hints": ["Utilizaba cables planos anchos de 40 u 80 hilos.", "Fue totalmente reemplazada por la tecnología SATA."]
    },
    {
        "word": "PILA",
        "question": "¿Batería de litio tipo botón encargada de mantener la configuración del BIOS y el reloj del sistema?",
        "hints": ["Conserva los datos cuando el computador está completamente apagado.", "Mantiene activo el chip CMOS con bajo consumo energético."]
    }
]

def reiniciar_juego():
    item = random.choice(COMPONENTES_DATA)
    session['word'] = item['word'].upper()
    session['question'] = item['question']
    session['hints'] = item['hints']
    session['guessed'] = []
    session['errors'] = 0
    session['max_errors'] = 6

@app.route('/')
def index():
    if 'word' not in session:
        reiniciar_juego()
    return render_template('index.html')

@app.route('/api/state')
def state():
    if 'word' not in session:
        reiniciar_juego()
        
    word = session['word']
    guessed = session['guessed']
    errors = session['errors']
    max_errors = session['max_errors']
    
    # Construir palabra oculta
    hidden_word = " ".join([letter if letter in guessed else "_" for letter in word])
    
    # Pistas dinámicas basadas en errores
    active_hints = []
    if errors >= 2:
        active_hints.append(session['hints'][0])
    if errors >= 4:
        active_hints.append(session['hints'][1])
        
    won = all(letter in guessed for letter in word)
    lost = errors >= max_errors
    
    return jsonify({
        "hidden_word": hidden_word,
        "question": session['question'],
        "hints": active_hints,
        "errors": errors,
        "max_errors": max_errors,
        "guessed": guessed,
        "won": won,
        "lost": lost,
        "word_to_reveal": word if lost else ""
    })

@app.route('/api/guess', methods=['POST'])
def guess():
    if 'word' not in session:
        return jsonify({"error": "Juego no iniciado"}), 400
        
    data = request.get_json()
    letter = data.get('letter', '').upper()
    
    word = session['word']
    guessed = session['guessed']
    errors = session['errors']
    max_errors = session['max_errors']
    
    won = all(l in guessed for l in word)
    lost = errors >= max_errors
    
    if not won and not lost and letter and letter not in guessed:
        guessed.append(letter)
        session['guessed'] = guessed
        if letter not in word:
            session['errors'] = errors + 1
            
    return state()

@app.route('/api/reset', methods=['POST'])
def reset():
    reiniciar_juego()
    return state()

if __name__ == '__main__':
    app.run(debug=True)