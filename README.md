#client
import socket

class NumberGuessingGameClient:
    def __init__(self, host='127.0.0.1', port=7777):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.host, self.port))
        while True:
            server_message = self.client_socket.recv(1024).decode()
            print(server_message, end='')
            if "Congratulations" in server_message:
                break
            user_input = input()
            self.client_socket.sendall(user_input.encode())
        self.client_socket.close()

if __name__ == "__main__":
    client = NumberGuessingGameClient()
    client.start()
