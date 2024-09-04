import requests
import subprocess
import logging

# Configuración del logger
logging.basicConfig(filename='logs/utils.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(url, local_filename):
    """Descarga un archivo desde una URL y lo guarda localmente."""
    try:
        logging.info(f"Descargando archivo desde {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza un error si la descarga falla
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"Archivo descargado y guardado como {local_filename}")
    except requests.RequestException as e:
        logging.error(f"Error al descargar el archivo: {e}")
        raise

def execute_command(command):
    """Ejecuta un comando en el sistema y maneja errores."""
    try:
        logging.info(f"Ejecutando comando: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logging.info(f"Comando ejecutado exitosamente. Salida: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando: {e}")
        logging.error(f"Salida del error: {e.stderr}")
        raise

def clean_up(file_path):
    """Elimina un archivo del sistema si existe."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Archivo {file_path} eliminado")
    except OSError as e:
        logging.error(f"Error al eliminar el archivo {file_path}: {e}")
        raise
