import socket as Socket
import time

global is_running
is_running = True


def connect_to_server():
    s = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
    server_address = (Socket.gethostname(), 9999)
    s.connect(server_address)

    s.setblocking(False)

    return (server_address, s)


def listen_for_ping(socket):
    socket.settimeout(2)
    while is_running:
        try:
            data = socket.recv(1)
            if data == b'0':
                socket.send(data)
            if not data:
                break
        except Socket.timeout:
            print('Timeout')
            break


addr, socket = connect_to_server()

print(f'Connected to server: {addr}')


def send_message(socket, message):
    try:
        socket.send(message)
        data = socket.recv(1)
    except (BrokenPipeError, ConnectionResetError):
        print('Connection lost')
        addr, s = connect_to_server()
        socket = s
        socket.send(message)


for i in range(4):
    # listen_for_ping(socket)
    send_message(socket, b'1')
    time.sleep(4)

is_running = False
socket.close()
