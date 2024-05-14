import socket as Socket
import time


def connect_to_server():
    s = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
    server_address = (Socket.gethostname(), 9999)
    s.connect(server_address)

    return (server_address, s)


addr, socket = connect_to_server()

print(f'Connected to server: {addr}')

socket.send(b'1')

time.sleep(5)

socket.send(b'0')

time.sleep(5)

socket.send(b'1')

socket.close()
