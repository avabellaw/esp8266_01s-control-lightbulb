import socket as Socket


class ClientConnection:
    def __init__(self, hostname=Socket.gethostname(), port=9999):
        self.socket = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
        self.server_address = (hostname, port)
        self.socket.settimeout(10)

    def send_message(self, message):
        self.socket.sendto(message, self.server_address)
        try:
            data = self.socket.recvfrom(1)
            return data == message
        except Socket.timeout:
            print("Request timed out")
        except ConnectionResetError:
            print('Connection lost')

        return False

    def close(self):
        self.socket.close()
