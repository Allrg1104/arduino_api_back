import serial
from datetime import datetime
import requests
import threading
import keyboard

puerto_serial = 'COM7'  # ⚠️ CAMBIA ESTO
baud_rate = 9600
url_api = 'https://arduino-api-back.vercel.app/api/datos'

def enviar_dato(dato, jugador):
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{hora} - Presionó {jugador}: {dato}")

    payload = {
        'fechaHora': hora,
        'dato': f"{jugador}: {dato}"
    }

    try:
        response = requests.post(url_api, json=payload)
        if response.status_code == 200:
            print("✅ Dato guardado correctamente.")
        else:
            print(f"⚠️ Error al enviar. Código: {response.status_code}")
            print("📬 Respuesta del servidor:", response.text)
    except Exception as e:
        print(f"❌ Error al conectar con el API: {e}")

# Detectar teclas desde el teclado físico (Jugador 1)
def manejar_tecla(evento):
    tecla = evento.name
    if tecla == 'w':
        enviar_dato('↑', 'Jugador 1')
    elif tecla == 's':
        enviar_dato('↓', 'Jugador 1')
    elif tecla == 'a':
        enviar_dato('←', 'Jugador 1')
    elif tecla == 'd':
        enviar_dato('→', 'Jugador 1')
    elif tecla == 'enter':
        enviar_dato('Enter', 'Jugador 1')

def escuchar_arduino():
    try:
        with serial.Serial(puerto_serial, baud_rate, timeout=1) as arduino:
            while True:
                linea = arduino.readline().decode('utf-8').strip()
                if linea:
                    enviar_dato(linea, 'Jugador 2')
    except serial.SerialException:
        print(f"❌ No se pudo abrir el puerto {puerto_serial}. Verifica que esté conectado.")
    except KeyboardInterrupt:
        print("\n🛑 Programa terminado por el usuario.")

# MAIN
if __name__ == '__main__':
    print(f"🎮 Escuchando Arduino por {puerto_serial} y teclado del PC...")

    # Conecta eventos de teclado
    keyboard.on_press(manejar_tecla)

    # Inicia hilo para Arduino
    hilo_arduino = threading.Thread(target=escuchar_arduino)
    hilo_arduino.start()

    # Mantén el hilo principal activo
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Programa terminado por el usuario.")