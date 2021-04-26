import socket
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP and port for accepting connections
server_address = ('localhost', 8090)

# print server address and port
print("[+] Server IP {} | Port {}".format(server_address[0], server_address[1]))
# bind socket with server
sock.bind(server_address)
# # Listen for incomingconnections
sock.listen(1)
# # Create Loop
while True:
    # Wait for a connection
    print('[+]  Waiting for a client connection')
    # connection established
    connection, client_address = sock.accept()
    print('here')
    try:
        print('[+] Connection from', client_address)

        # Receive the data in small chunks and retransmit it

        data = connection.recv(1024)
        print('received "%s"' % data)
        test_number = 10

        while test_number >= 1.0:

            command = b"try this command..."
            connection.send(command)
            print('sending data "%s" to the client' % command)
            test_number = test_number - 1.0
            time.sleep(0.1)

            # data = connection.recv(1024)
            # print('received "%s"' % data)
                # print('no more data from', client_address)
                # break


    finally:
        # Close the connection
        connection.close()
