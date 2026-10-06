import time
import random
import urllib.request
import urllib.parse

nombres = ["Santiago", "Christian", "Camila", "Mateo", "Valeria", "Andres", "Sofia"]

print(">>> Iniciando simulador de tráfico... Presiona Ctrl + C para detener.")

while True:
    nombre = random.choice(nombres)
    edad = random.randint(18, 50)
    params = urllib.parse.urlencode({"nombre": nombre, "edad": edad})
    url = f"http://localhost:8000/usuarios?{params}"
    
    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            print(f"[OK] Usuario registrado: {nombre} ({edad} años)")
    except Exception as e:
        print(f"[Error] Falló la petición: {e}")
    
    # Pausa aleatoria entre 1 y 3 segundos
    time.sleep(random.uniform(1.0, 3.0))