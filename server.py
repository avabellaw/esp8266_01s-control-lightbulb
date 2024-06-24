import socket
import config
import sys
import threading
from control_lightbulb import get_lightbulb_instance
from log import log

light = get_lightbulb_instance()


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
        global dead_connections_num
        dead_connections_num += 1
        self.is_alive = False
        self.connection.close()
        client_connections.remove(self)

    def has_error(self, error):
        print(f"Client error: {error}")


client_connections = []

global dead_connections_num
dead_connections_num = 0

global is_running
is_running = True


def start_server():
    global is_running
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
            while is_running:
                if active_connections_count != len(client_connections):
                    active_connections_count = len(client_connections)
                    print_active_connections()

                try:
                    connection, addr = s.accept()

                    print(f"Connection received: {addr}")
                    thread = threading.Thread(target=handle_client,
                                              args=(connection, ))

                    client = ClientConnection(thread, connection, addr)
                    client_connections.append(client)

                    thread.start()
                except socket.timeout:
                    for c in client_connections:
                        c.query_alive()

        except KeyboardInterrupt:
            shutdown_server()
        finally:
            # End connection threads
            print("Ending client threads...")
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
    connection.settimeout(4)
    this_client = client_connections[-1]

    while is_running and this_client.is_alive:
        try:
            data = connection.recv(1)
        except socket.timeout:
            pass
        else:
            if data == config.BUTTON_SHORT_CLICK:
                print("Button pressed")
                try:
                    light.toggle()
                except Exception as e:
                    handle_light_bulb_exception(e)
            elif data == config.BUTTON_LONG_CLICK:
                print("Button held")
                try:
                    light.toggle_brightness()
                except Exception as e:
                    handle_light_bulb_exception(e)
            elif data == b'0':
                this_client.pings_missed = 0
            elif not data:
                this_client.has_disconnected()
                break
            else:
                print("data: " + data)
                pass


def shutdown_server():
    global is_running
    is_running = False


def handle_light_bulb_exception(e):
    log(e)
    global light
    light = get_lightbulb_instance()


def print_active_connections():
    print(f"Active connections: {len(client_connections)}")


def check_console_input():
    global is_running
    while is_running:
        user_input = input()
        match user_input:
            case "connections":
                print_active_connections()
                break
            case "connection history":
                print(f"{dead_connections_num} connections have been lost")
                break
            case "quit":
                is_running = False


console_thread = threading.Thread(target=check_console_input)
console_thread.start()

start_server()
