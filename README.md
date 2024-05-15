# client
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


# server

import socket
import random
import json

class NumberGuessingGameServer:
    def __init__(self, host='0.0.0.0', port=7777):
        self.host = host
        self.port = port
        self.leaderboard_file = "leaderboard.json"
        self.leaderboard = self.load_leaderboard()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def load_leaderboard(self):
        try:
            with open(self.leaderboard_file, "r") as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []
        return leaderboard
    
    def save_leaderboard(self):
        with open(self.leaderboard_file, "w") as file:
            json.dump(self.leaderboard, file)
    
    def display_leaderboard(self):
        print("Leaderboard:")
        print("Name\tScore")
        for entry in self.leaderboard:
            print(f"{entry['name']}\t{entry['score']}")

    def generate_random_number(self, difficulty):
        if difficulty == "easy":
            return random.randint(1, 50)
        elif difficulty == "medium":
            return random.randint(1, 100)
        elif difficulty == "hard":
            return random.randint(1, 500)

    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        conn.sendall(b"Enter your name: ")
        username = conn.recv(1024).decode().strip()
        conn.sendall(b"Choose difficulty (easy, medium, hard): ")
        difficulty = conn.recv(1024).decode().strip().lower()
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "easy"
        random_number = self.generate_random_number(difficulty)
        max_guess = {"easy": 50, "medium": 100, "hard": 500}[difficulty]
        conn.sendall(f"Guess the number between 1 and {max_guess}\n".encode())

        tries = 0
        while True:
            guess = int(conn.recv(1024).decode().strip())
            tries += 1
            if guess == random_number:
                conn.sendall(f"Congratulations, {username}! You guessed the number in {tries} tries.\n".encode())
                self.update_leaderboard(username, tries)
                break
            elif guess < random_number:
                conn.sendall(b"Too low, try again.\n")
            else:
                conn.sendall(b"Too high, try again.\n")
        conn.close()

    def update_leaderboard(self, username, score):
        self.leaderboard.append({"name": username, "score": score})
        self.save_leaderboard()
        self.display_leaderboard()

    def start(self):
        while True:
            conn, addr = self.server_socket.accept()
            self.handle_client(conn, addr)

if __name__ == "__main__":
    server = NumberGuessingGameServer()
    server.start()


