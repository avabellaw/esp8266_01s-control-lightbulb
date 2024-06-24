import socket
import config
import sys
import threading
from control_lightbulb import get_lightbulb_instance
from log import log

light = get_lightbulb_instance()

global dead_connections_num
dead_connections_num = 0

global is_running
is_running = True


def start_server():
    global is_running

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        host = "0.0.0.0"
        port = config.SERVER_PORT

        s.bind((host, port))
        s.settimeout(5)
        try:
            print("Server started...")
            while is_running:
                try:
                    data, addr = s.recvfrom(1024)
                    handle_data_recv(data, addr, s)
                except socket.timeout:
                    pass
                except Exception as e:
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            shutdown_server()
        finally:
            # End connection threads
            print("Ending client threads...")
            is_running = False
            print("Closing socket...")
            s.close()
            print("Server shutdown successfully.")
            # Exit without error
            sys.exit(0)


def handle_data_recv(data, addr, socket):
    if data == config.BUTTON_SHORT_CLICK:
        print(f"Button pressed [{addr}]")
        if not config.DEBUG:
            print("not debug")
            try:
                light.toggle()
            except Exception as e:
                handle_light_bulb_exception(e)
    elif data == config.BUTTON_LONG_CLICK:
        print(f"Button held [{addr}]")
        if not config.DEBUG:
            try:
                light.toggle_brightness()
            except Exception as e:
                handle_light_bulb_exception(e)
    else:
        print(f"Unknown data received: {data} [{addr}]")
        pass

    print("sending response")
    socket.sendto(data, addr)


def shutdown_server():
    global is_running
    is_running = False


def handle_light_bulb_exception(e):
    log(e)
    global light
    light = get_lightbulb_instance()


def check_console_input():
    global is_running
    while is_running:
        user_input = input()
        if user_input == "connection history":
            print(f"{dead_connections_num} connections have been lost")
        elif user_input == "quit":
            is_running = False


console_thread = threading.Thread(target=check_console_input)
console_thread.start()

start_server()
