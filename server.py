import socket
import config
import sys
import threading
from control_lightbulb import light


class ClientConnection:
    def __init__(self, thread, connection, address):
        self.thread = thread
        self.connection = connection
        self.address = address
        self.pings_missed = 0
        self.is_alive = True

    def query_alive(self):
        self.pings_missed += 1

        if self.pings_missed > 10:
            print("Client not responding...")
            self.has_disconnected()

    def has_disconnected(self):
        print("~Client disconnected~")
        self.is_alive = False
        self.connection.close()
        client_connections.remove(self)

    def has_error(self, error):
        print(f"Client error: {error}")


client_connections = []

global is_running
is_running = True


def start_server():
    active_connections_count = 0

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = "0.0.0.0"
        port = config.SERVER_PORT

        s.bind((host, port))
        s.listen()
        s.settimeout(5)
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
            # FORCE THREADS TO END BY UNCOMMENTING THE FOLLOWING CODE
            # print("Waiting for threads to end...")
            # for c in client_connections:
            #     c.thread.join()
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
                light.toggle()
            elif data == b'0':
                this_client.pings_missed = 0
            elif not data:
                this_client.has_disconnected()
                break
            else:
                print("data: " + data)
                pass
        except Exception as e:
            this_client.has_error(e)
            if this_client in client_connections:
                client_connections.remove(this_client)
            break


start_server()
