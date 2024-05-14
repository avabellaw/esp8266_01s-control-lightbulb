import socket
import config
import sys
import threading


class ClientConnection:
    def __init__(self, thread, connection, address):
        self.thread = thread
        self.connection = connection
        self.address = address

    def has_disconnected(self):
        print("~Client disconnected~")
        client_connections.remove(self)

    def has_error(self, error):
        print(f"Client error: {error}")
        self.has_disconnected()


client_connections = []

global is_running
is_running = True


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
                if active_connections_count != len(client_connections):
                    active_connections_count = len(client_connections)
                    print(f"Active connections: {len(client_connections)}")

                try:
                    connection, addr = s.accept()

                    print(f"Connection received: {addr}")
                    thread = threading.Thread(target=handle_client,
                                              args=(connection, ))

                    client = ClientConnection(thread, connection, addr)
                    client_connections.append(client)

                    thread.start()
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            # End connection threads
            print("Ending client threads...")
            global is_running
            is_running = False
            # print("Waiting for threads to end...")
            # for t in connection_threads:
            #     t.join()

            # Forcefully close for now until I implement check to see if 
            # client is still connected
            print("Closing socket...")
            s.close()
            print("Server shutdown successfully.")
            # Exit without error
            sys.exit(0)


def handle_client(connection):
    this_client = client_connections[-1]

    while is_running:
        try:
            data = connection.recv(1)
            if data == config.BUTTON_CLICK:
                print("Button pressed")
            elif not data:
                this_client.has_disconnected()
                break
            else:
                print("data: " + data)
                pass
        except ConnectionResetError as e:
            this_client.has_error(e)
            break
        except Exception as e:
            this_client.has_error(e)
            break


start_server()
