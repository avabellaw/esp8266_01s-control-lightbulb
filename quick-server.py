import socket
import config
import sys
import threading

connection_threads = []


def start_server():
    active_connections_count = 0

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = socket.gethostname()
        port = config.SERVER_PORT

        s.bind((host, port))
        s.listen()
        s.settimeout(2)
        try:
            print("Waiting for new connection")
            while True:
                if active_connections_count != len(connection_threads):
                    active_connections_count = len(connection_threads)
                    print(f"Active connections: {len(connection_threads)}")

                try:
                    connection, addr = s.accept()

                    print(f"Connect received: {addr}")
                    thread = threading.Thread(target=handle_client,
                                              args=(connection, ))
                    connection_threads.append(thread)
                    thread.start()
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            print("Shutting down server")
            # End connection threads
            for t in connection_threads:
                t.join()
            s.close()
            # Exit without error
            sys.exit(0)


def handle_client(connection):
    this_thread = connection_threads[-1]
    while True:
        data = connection.recv(1)
        if data == b'1':
            print("Turning on light")
        elif data == b'0':
            print("Turning off light")
        elif not data:
            print("Client disconnected")
            connection_threads.remove(this_thread)
            break
        else:
            pass


start_server()
