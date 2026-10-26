from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Lista de componentes con sus 2 pistas máximas cada uno
PALABRAS = [
    {
        "palabra": "MEMORIA RAM", 
        "pistas": [
            "Almacena temporalmente los datos de los programas en ejecucion.", 
            "Es volatil, pierde toda la informacion al apagar el equipo."
        ]
    },
    {
        "palabra": "SOCKET", 
        "pistas": [
            "Conector fisico donde se instala directamente el microprocesador.", 
            "Tambien es conocido como zocalo de CPU."
        ]
    },
    {
        "palabra": "PROCESADOR", 
        "pistas": [
            "Es el cerebro del ordenador encargado de ejecutar instrucciones.", 
            "Realiza los calculos logicos y aritmeticos principales."
        ]
    },
    {
        "palabra": "CHIPSET", 
        "pistas": [
            "Conjunto de circuitos integrados que gestionan el flujo de datos.", 
            "Controla la comunicacion entre la CPU, la memoria y los perifericos."
        ]
    },
    {
        "palabra": "ATX", 
        "pistas": [
            "Es el formato estandar de placa base y fuente de alimentacion.", 
            "Fue definido comercialmente por Intel en la decada de los noventa."
        ]
    },
    {
        "palabra": "BIOS", 
        "pistas": [
            "Sistema basico de entrada y salida almacenado en memoria ROM o flash.", 
            "Realiza la comprobacion inicial del hardware al encender el equipo."
        ]
    },
    {
        "palabra": "DISIPADORES DE CALOR", 
        "pistas": [
            "Elementos metalicos que absorben y alejan la temperatura de los componentes.", 
            "Suelen combinarse con ventiladores o pasta termica para mayor eficiencia."
        ]
    },
    {
        "palabra": "PUERTO SATA", 
        "pistas": [
            "Interfaz de conexion para discos duros y unidades de estado solido.", 
            "Reemplazo moderno y mas rapido al antiguo puerto IDE."
        ]
    },
    {
        "palabra": "PUERTO IDE", 
        "pistas": [
            "Antigua interfaz de conexion basada en cables planos de cinta ancha.", 
            "Utilizado tradicionalmente para conectar discos duros y unidades opticas."
        ]
    },
    {
        "palabra": "PILA CMOS", 
        "pistas": [
            "Bateria pequena de tipo boton instalada en la placa base.", 
            "Mantiene la configuracion del sistema, la fecha y la hora cuando esta apagado."
        ]
    }
]

juego = {
    "palabra": "",
    "pistas": [],
    "letras_adivinadas": [],
    "intentos_restantes": 6,
    "ganado": False,
    "perdido": False
}

def iniciar_nuevo_juego():
    item = random.choice(PALABRAS)
    juego["palabra"] = item["palabra"]
    juego["pistas"] = item["pistas"]
    juego["letras_adivinadas"] = []
    juego["intentos_restantes"] = 6
    juego["ganado"] = False
    juego["perdido"] = False

def obtener_estado():
    palabra_oculta = " ".join([letra if letra == ' ' or letra in juego["letras_adivinadas"] else "_" for letra in juego["palabra"]])
    
    # Calcular pistas activas segun los errores cometidos
    errores = 6 - juego["intentos_restantes"]
    pistas_activas = []
    if errores >= 2:
        pistas_activas.append(juego["pistas"][0])
    if errores >= 4:
        pistas_activas.append(juego["pistas"][1])

    return {
        "palabra_oculta": palabra_oculta,
        "intentos_restantes": juego["intentos_restantes"],
        "letras_usadas": [l for l in juego["letras_adivinadas"] if l != ' '],
        "ganado": juego["ganado"],
        "perdido": juego["perdido"],
        "palabra_revelada": juego["palabra"] if juego["perdido"] else "",
        "pistas": pistas_activas
    }

@app.route('/')
def index():
    iniciar_nuevo_juego()
    return render_template('index.html')

@app.route('/api/estado', methods=['GET'])
def estado():
    return jsonify(obtener_estado())

@app.route('/api/reiniciar', methods=['POST'])
def reiniciar():
    iniciar_nuevo_juego()
    return jsonify(obtener_estado())

@app.route('/api/intentar', methods=['POST'])
def intentar():
    if juego["ganado"] or juego["perdido"]:
        return jsonify(obtener_estado())

    data = request.get_json()
    letra = data.get('letra', '').upper()

    if letra and letra not in juego["letras_adivinadas"]:
        juego["letras_adivinadas"].append(letra)
        
        if letra not in juego["palabra"]:
            juego["intentos_restantes"] -= 1

        if all(l == ' ' or l in juego["letras_adivinadas"] for l in juego["palabra"]):
            juego["ganado"] = True
        
        if juego["intentos_restantes"] <= 0:
            juego["perdido"] = True

    return jsonify(obtener_estado())

if __name__ == '__main__':
    app.run(debug=True)