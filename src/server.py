import logging
import socket
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import signal
import sys

# Configuración del logging
log_dir = 'logs'
log_file = os.path.join(log_dir, 'server.log')

# Crear el directorio de logs si no existe
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def signal_handler(sig, frame):
    logging.info('Servidor detenido manualmente')
    sys.exit(0)

# Asignar la señal de interrupción (Ctrl+C) al manejador
signal.signal(signal.SIGINT, signal_handler)

def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8083):
    try:
        # Verificar si el puerto está disponible
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                raise OSError(f"El puerto {port} ya está en uso")

        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logging.info(f'Servidor iniciado en el puerto {port}')
        print(f'Servidor iniciado en el puerto {port}')
        httpd.serve_forever()
    except OSError as e:
        logging.error(f"Error al iniciar el servidor: {e}")
        print(f"Error al iniciar el servidor: {e}")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        print(f"Error inesperado: {e}")

if __name__ == '__main__':
    run_server()
