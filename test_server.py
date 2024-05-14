import socket as Socket
import time
import threading

global is_running
is_running = True


def connect_to_server():
    s = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
    server_address = (Socket.gethostname(), 9999)
    s.connect(server_address)

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

t1 = threading.Thread(target=listen_for_ping, args=(socket,))
t1.start()

for i in range(4):
    socket.send(b'1')
    time.sleep(4)

is_running = False
t1.join()
socket.close()
