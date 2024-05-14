import socket
import config
import sys


def start_server():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = socket.gethostname()
        port = config.SERVER_PORT

        s.bind((host, port))
        s.listen(2)
        s.settimeout(2)
        try:
            while True:
                print("Waiting for connection")
                try:
                    connection, addr = s.accept()
                except socket.timeout:
                    pass

                print(f"Connect received: {addr}")
                handle_client(connection)
        except KeyboardInterrupt:
            print("Shutting down server")
            s.close()
            # Exit without error
            sys.exit(0)


def handle_client(connection):
    while True:
        data = connection.recv(1)
        if data == b'1':
            print("Turning on light")
        elif data == b'0':
            print("Turning off light")
        elif not data:
            # Client disconnected
            break
        else:
            pass


start_server()
