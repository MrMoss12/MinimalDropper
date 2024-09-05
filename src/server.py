import logging
import socket
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import signal
import sys
from utils import clean_up

# Configuración del logging
log_dir = 'logs'  # Directorio donde se guardarán los logs
log_file = os.path.join(log_dir, 'server.log')  # Archivo de log

def setup_logging(log_file):
    """Configura el logging para el servidor."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Crear el directorio de logs si no existe
    logging.basicConfig(
        filename=log_file,  # Archivo donde se guardarán los registros
        level=logging.INFO,  # Nivel de los mensajes a registrar
        format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del mensaje de registro
    )

def signal_handler(sig, frame):
    """Manejador para señales de interrupción (Ctrl+C)."""
    logging.info('Servidor detenido manualmente')  # Registra la detención manual del servidor
    clean_up(log_file)  # Limpiar el archivo de log si es necesario
    sys.exit(0)  # Sale del programa

# Asignar la señal de interrupción (Ctrl+C) al manejador
signal.signal(signal.SIGINT, signal_handler)  # Configura el manejador de señales

def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8083):
    """Inicializa y ejecuta el servidor HTTP."""
    setup_logging(log_file)  # Configura el logging
    try:
        # Verificar si el puerto está disponible
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                raise OSError(f"El puerto {port} ya está en uso")  # Lanza una excepción si el puerto está en uso

        server_address = ('', port)  # Configura la dirección del servidor
        httpd = server_class(server_address, handler_class)  # Crea una instancia del servidor HTTP
        logging.info(f'Servidor iniciado en el puerto {port}')  # Registra la información de inicio
        print(f'Servidor iniciado en el puerto {port}')  # Imprime la información de inicio
        httpd.serve_forever()  # Inicia el servidor y lo mantiene en ejecución
    except OSError as e:
        logging.error(f"Error al iniciar el servidor: {e}")  # Registra el error si el puerto está en uso
        print(f"Error al iniciar el servidor: {e}")  # Imprime el error
    except Exception as e:
        logging.error(f"Error inesperado: {e}")  # Registra cualquier otro error inesperado
        print(f"Error inesperado: {e}")  # Imprime el error inesperado

if __name__ == '__main__':
    run_server()  # Llama a la función para iniciar el servidor cuando se ejecute el script
