import socket
import sys

class TcpClient:

    def __init__(self,host_ip,server_port):

        self.host_ip = host_ip
        self.server_port = server_port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket Created')
        except socket.error:
            print('Failed to create socket')
            sys.exit()



    def connet_server(self):
        try:
            self.client.connect((host_ip, server_port))
            print("Conneting to server at IP: {}, port: {}".format(host_ip, server_port))

        except:
            print('Failed to create socket')
            sys.exit('Please provide a correct server address')


    def send_data(self, data):
        try:
            self.client.sendall(data.encode())
            print("Bytes Sent: {}".format(data))
        except socket.error:
            print("Failed to send data")

    def reveive_data(self):
        try:
            received = self.client.recv(1024)
            print("Bytes Received: {}".format(received.decode()))
        except socket.error:
            print("Failed to receive data")

    def close(self):
        self.client.close()

host_ip, server_port = "127.0.0.1", 8080

if __name__ == "__main__":
    client = TcpClient(host_ip, server_port)
    client.connet_server()
    client.send_data("hello\n")
    client.send_data("what are you doing\n")
    client.send_data("can you hear me\n")
    client.reveive_data()
    client.send_data("ok good \n")
    client.close()

