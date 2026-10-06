import time
import random
import urllib.request
import json

URL = "http://localhost:8000/users"

NOMBRES = [
    "Carlos Perez", "Maria Lopez", "Andres Gomez", "Laura Rodriguez",
    "Juan Martinez", "Sofia Hernandez", "Diego Castro", "Valentina Morales",
    "Mateo Silva", "Camila Torres", "Sebastian Vargas", "Daniela Rios"
]

print(">>> Iniciando simulador de tráfico... Presiona Ctrl + C para detener.")

while True:
    payload = {
        "name": random.choice(NOMBRES),
        "age": random.randint(18, 65)
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL, 
        data=data, 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                res_body = json.loads(response.read().decode("utf-8"))
                print(f"[OK] Usuario creado: ID={res_body.get('id')} - {payload['name']} ({payload['age']} años)")
    except urllib.error.HTTPError as e:
        print(f"[Error] Falló la petición: HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"[Error de conexión]: {e}")
        
    time.sleep(2)