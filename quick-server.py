import socket

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name and port
host = socket.gethostname()
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

while True:
    print("Listening...")

    # Establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    # Receive data from the client
    while True:
        data = clientsocket.recv(1024)
        msg = data.decode('utf-8')
        if not msg:
            break
        print("Received data: %s" % msg)

    # Close the connection
    clientsocket.close()
