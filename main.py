import base64
import json
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# 1. Configura tus credenciales y la ruta de tu foto de prueba
API_KEY_MINIMAX = os.getenv("API_KEY_MINIMAX")  # Carga desde .env
RUTA_IMAGEN = "./bot-boletas/boleta1.jpg"            # Asegúrate de poner una foto real en la misma carpeta

def extraer_datos_boleta(ruta_imagen, api_key):
    # Convertir la imagen local a Base64
    with open(ruta_imagen, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    url = "https://api.minimax.io/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt_instrucciones = (
        "Analiza esta boleta/factura electrónica. Extrae la información y responde "
        "EXCLUSIVAMENTE en formato JSON válido, sin texto adicional ni bloques de código markdown. "
        "Usa las siguientes claves: 'ruc', 'razon_social', 'fecha', 'monto_total', 'igv'."
    )

    payload = {
        "model": "MiniMax-M3",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_instrucciones},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    }

    print("Enviando imagen a MiniMax...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        res_data = response.json()
        print(f"Respuesta completa: {json.dumps(res_data, indent=2)}")
        
        # Verificar si 'choices' existe y no es None
        if res_data.get('choices') is None:
            print("Error: 'choices' es None en la respuesta")
            return None
            
        contenido_texto = res_data['choices'][0]['message']['content']
        return contenido_texto
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def generar_nombre_unico(carpeta, nombre_base, extension):
    """Genera un nombre de archivo único, incrementando si ya existe"""
    import os
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    contador = 0
    while True:
        if contador == 0:
            nombre_archivo = f"{nombre_base}.{extension}"
        else:
            nombre_archivo = f"{nombre_base}_{contador}.{extension}"
        
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        if not os.path.exists(ruta_completa):
            return ruta_completa
        contador += 1

if __name__ == "__main__":
    resultado_raw = extraer_datos_boleta(RUTA_IMAGEN, API_KEY_MINIMAX)
    
    if resultado_raw:
        try:
            # Convertir el texto a un diccionario de Python
            datos_json = json.loads(resultado_raw)
            print("\n--- DATOS EXTRAÍDOS CON ÉXITO ---")
            print(json.dumps(datos_json, indent=2, ensure_ascii=False))
            
            # Guardar resultado en archivo con nombre único
            ruta_salida = generar_nombre_unico("output", "resultado_boleta", "json")
            with open(ruta_salida, "w", encoding="utf-8") as f:
                json.dump(datos_json, f, indent=2, ensure_ascii=False)
            print(f"\nResultado guardado en {ruta_salida}")
        except json.JSONDecodeError:
            print("\nEl modelo devolvió texto pero no en formato JSON puro:")
            print(resultado_raw)
            # Guardar respuesta cruda con nombre único
            ruta_salida = generar_nombre_unico("output", "resultado_boleta_raw", "txt")
            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write(resultado_raw)
            print(f"Respuesta guardada en {ruta_salida}")