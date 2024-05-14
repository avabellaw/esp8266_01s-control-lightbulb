import socket
import config
import sys
import threading


class ClientConnection:
    def __init__(self, thread, connection, address):
        self.thread = thread
        self.connection = connection
        self.address = address
        self.pings_missed = 0
        self.is_alive = True

    def ping(self):
        self.connection.sendall(b'0')
        self.pings_missed += 1

        if self.pings_missed > 5:
            print("Client not responding...")
            self.connection.close()

    def has_disconnected(self):
        print("~Client disconnected~")
        self.is_alive = False
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
        host = socket.gethostname()
        port = config.SERVER_PORT

        s.bind((host, port))
        s.listen()
        s.settimeout(2)
        try:
            print("Waiting for new connection")
            while True:
                for client in client_connections:
                    client.ping()

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
            print("Waiting for threads to end...")
            for c in client_connections:
                c.thread.join()
            print("Closing socket...")
            s.close()
            print("Server shutdown successfully.")
            # Exit without error
            sys.exit(0)


def handle_client(connection):
    this_client = client_connections[-1]

    while is_running and this_client.is_alive:
        try:
            data = connection.recv(1)
            if data == config.BUTTON_CLICK:
                print("Button pressed")
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
