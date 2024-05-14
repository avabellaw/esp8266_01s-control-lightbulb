import socket
import config
import sys
import threading

connection_threads = []

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
                if active_connections_count != len(connection_threads):
                    active_connections_count = len(connection_threads)
                    print(f"Active connections: {len(connection_threads)}")

                try:
                    connection, addr = s.accept()

                    print(f"Connection received: {addr}")
                    thread = threading.Thread(target=handle_client,
                                              args=(connection, ))
                    connection_threads.append(thread)
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
    this_thread = connection_threads[-1]
    while is_running:
        data = connection.recv(1)
        if data == config.BUTTON_CLICK:
            print("Button pressed")
        elif not data:
            print("Client disconnected")
            connection_threads.remove(this_thread)
            break
        else:
            print(data)
            pass


start_server()
