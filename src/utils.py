import requests
import subprocess
import logging
import os  # Necesario para la función clean_up

# Configuración del logger
logging.basicConfig(
    filename='logs/utils.log',  # Archivo donde se guardarán los registros
    level=logging.INFO,  # Nivel de los mensajes a registrar
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del mensaje de registro
)

def download_file(url, local_filename):
    """Descarga un archivo desde una URL y lo guarda localmente."""
    try:
        logging.info(f"Descargando archivo desde {url}")  # Registra el inicio de la descarga
        response = requests.get(url, stream=True)  # Realiza la solicitud GET para descargar el archivo
        response.raise_for_status()  # Lanza una excepción si la solicitud falla

        # Abre el archivo local en modo de escritura binaria
        with open(local_filename, 'wb') as file:
            # Escribe el contenido descargado en el archivo local en bloques
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        logging.info(f"Archivo descargado y guardado como {local_filename}")  # Registra el éxito de la descarga
    except requests.RequestException as e:
        logging.error(f"Error al descargar el archivo: {e}")  # Registra el error si ocurre una excepción
        raise

def execute_command(command):
    """Ejecuta un comando en el sistema y maneja errores."""
    try:
        logging.info(f"Ejecutando comando: {command}")  # Registra el comando que se va a ejecutar
        # Ejecuta el comando y captura la salida
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,  # Lanza una excepción si el comando falla
            text=True,  # La salida se trata como texto en lugar de bytes
            capture_output=True  # Captura la salida y el error del comando
        )
        logging.info(f"Comando ejecutado exitosamente. Salida: {result.stdout}")  # Registra la salida del comando
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando: {e}")  # Registra el error si el comando falla
        logging.error(f"Salida del error: {e.stderr}")  # Registra la salida del error
        raise

def clean_up(file_path):
    """Elimina un archivo del sistema si existe."""
    try:
        if os.path.exists(file_path):  # Verifica si el archivo existe
            os.remove(file_path)  # Elimina el archivo
            logging.info(f"Archivo {file_path} eliminado")  # Registra la eliminación del archivo
    except OSError as e:
        logging.error(f"Error al eliminar el archivo {file_path}: {e}")  # Registra el error si ocurre una excepción
        raise
