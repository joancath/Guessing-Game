import random
import json

class NumberGuessingGame:
    def __init__(self):
        self.leaderboard_file = "leaderboard.json"
        self.leaderboard = self.load_leaderboard()
        self.username = None
        self.difficulty = "easy"
    
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
    
    def set_username(self):
        self.username = input("Enter your name: ")
    
    def set_difficulty(self):
        difficulty_choice = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty_choice in ["easy", "medium", "hard"]:
            self.difficulty = difficulty_choice
        else:
            print("Invalid difficulty choice. Defaulting to easy.")
            self.difficulty = "easy"
    
    def generate_random_number(self):
        if self.difficulty == "easy":
            return random.randint(1, 50)
        elif self.difficulty == "medium":
            return random.randint(1, 100)
        elif self.difficulty == "hard":
            return random.randint(1, 500)
    
    def play_game(self):
        if not self.username:
            self.set_username()
        self.set_difficulty()
        random_number = self.generate_random_number()
        print(f"Guess the number between 1 and {random_number}")
        tries = 0
        while True:
            guess = int(input("Enter your guess: "))
            tries += 1
            if guess == random_number:
                print(f"Congratulations, {self.username}! You guessed the number in {tries} tries.")
                self.update_leaderboard(tries)
                break
            elif guess < random_number:
                print("Too low, try again.")
            else:
                print("Too high, try again.")
    
    def update_leaderboard(self, score):
        self.leaderboard.append({"name": self.username, "score": score})
        self.save_leaderboard()
        self.display_leaderboard()

if __name__ == "__main__":
    game = NumberGuessingGame()
    while True:
        game.play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break
            
