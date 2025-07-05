import random

class RockPaperScissors:
    def __init__(self):
        self.choices = ["rock", "paper", "scissors"]
        self.emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        self.user_patterns = []  # Track user's previous choices for smart mode
        
    def get_computer_choice(self, difficulty="normal"):
        """Computer makes choice based on difficulty level"""
        if difficulty == "easy":
            # Easy: Slightly favor losing moves
            weights = [0.4, 0.4, 0.2] if len(self.user_patterns) == 0 else self._get_easy_weights()
            return random.choices(self.choices, weights=weights)[0]
        
        elif difficulty == "hard":
            # Hard: Try to predict user patterns
            if len(self.user_patterns) >= 2:
                return self._predict_and_counter()
            else:
                return random.choice(self.choices)
        
        else:  # normal
            return random.choice(self.choices)
    
    def _get_easy_weights(self):
        """Make computer slightly more likely to lose in easy mode"""
        last_choice = self.user_patterns[-1]
        if last_choice == "rock":
            return [0.2, 0.5, 0.3]  # Favor paper (user wins)
        elif last_choice == "paper":
            return [0.3, 0.2, 0.5]  # Favor scissors (user wins)
        else:  # scissors
            return [0.5, 0.3, 0.2]  # Favor rock (user wins)
    
    def _predict_and_counter(self):
        """Try to predict user's next move and counter it"""
        # Look for patterns in last few moves
        recent_moves = self.user_patterns[-3:]
        
        # Simple pattern detection
        if len(recent_moves) >= 2 and recent_moves[-1] == recent_moves[-2]:
            # User repeated last move, predict they'll do it again
            predicted = recent_moves[-1]
        elif len(self.user_patterns) >= 3:
            # Look for most common choice
            predicted = max(set(self.user_patterns), key=self.user_patterns.count)
        else:
            predicted = random.choice(self.choices)
        
        # Counter the prediction
        counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        return counters[predicted]
    
    def get_user_choice(self):
        """Get user's choice with input validation"""
        while True:
            choice = input("\nEnter your choice (rock/paper/scissors) or 'quit': ").lower().strip()
            if choice in ["rock", "paper", "scissors", "quit"]:
                if choice != "quit":
                    self.user_patterns.append(choice)
                return choice
            print("Invalid choice! Please enter 'rock', 'paper', or 'scissors'")
    
    def determine_winner(self, user_choice, computer_choice):
        """Determine the winner of the round"""
        if user_choice == computer_choice:
            return "tie"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            return "user"
        else:
            return "computer"
    
    def display_choices(self, user_choice, computer_choice):
        """Display both choices with emojis"""
        print(f"\nYou chose: {user_choice} {self.emojis[user_choice]}")
        print(f"Computer chose: {computer_choice} {self.emojis[computer_choice]}")
    
    def display_result(self, result, user_score, computer_score, round_num=None, total_rounds=None):
        """Display the result of the round"""
        if result == "tie":
            print("🤝 It's a tie!")
        elif result == "user":
            print("🎉 You win this round!")
        else:
            print("🤖 Computer wins this round!")
        
        score_text = f"Score - You: {user_score} | Computer: {computer_score}"
        if round_num and total_rounds:
            score_text += f" | Round {round_num}/{total_rounds}"
        print(score_text)

def get_game_mode():
    """Get the game mode from user"""
    print("\n🎯 Choose Game Mode:")
    print("1. Quick Play (unlimited rounds)")
    print("2. Best of 3")
    print("3. Best of 5")
    print("4. Best of 7")
    print("5. Custom (choose your own)")
    
    while True:
        try:
            choice = int(input("Enter mode (1-5): "))
            if choice == 1:
                return None  # Unlimited
            elif choice == 2:
                return 3
            elif choice == 3:
                return 5
            elif choice == 4:
                return 7
            elif choice == 5:
                rounds = int(input("Enter number of rounds: "))
                return rounds if rounds > 0 else None
            else:
                print("Please enter a number between 1-5")
        except ValueError:
            print("Please enter a valid number")

def get_difficulty():
    """Get difficulty level from user"""
    print("\n⚡ Choose Difficulty:")
    print("1. Easy (computer makes more mistakes)")
    print("2. Normal (completely random)")
    print("3. Hard (computer learns your patterns)")
    
    while True:
        try:
            choice = int(input("Enter difficulty (1-3): "))
            if choice == 1:
                return "easy"
            elif choice == 2:
                return "normal"
            elif choice == 3:
                return "hard"
            else:
                print("Please enter 1, 2, or 3")
        except ValueError:
            print("Please enter a valid number")

def play_unlimited_mode(game, difficulty):
    """Play unlimited rounds mode"""
    user_score = 0
    computer_score = 0
    rounds_played = 0
    
    while True:
        user_choice = game.get_user_choice()
        if user_choice == "quit":
            break
            
        computer_choice = game.get_computer_choice(difficulty)
        rounds_played += 1
        
        game.display_choices(user_choice, computer_choice)
        result = game.determine_winner(user_choice, computer_choice)
        
        if result == "user":
            user_score += 1
        elif result == "computer":
            computer_score += 1
            
        game.display_result(result, user_score, computer_score)
        print("-" * 40)
    
    return user_score, computer_score, rounds_played

def play_best_of_mode(game, difficulty, total_rounds):
    """Play best-of-X rounds mode"""
    user_score = 0
    computer_score = 0
    rounds_to_win = (total_rounds // 2) + 1
    
    print(f"\n🏆 First to win {rounds_to_win} rounds wins the match!")
    
    for round_num in range(1, total_rounds + 1):
        # Check if someone already won
        if user_score >= rounds_to_win or computer_score >= rounds_to_win:
            break
            
        print(f"\n--- Round {round_num} ---")
        user_choice = game.get_user_choice()
        
        if user_choice == "quit":
            return user_score, computer_score, round_num - 1
            
        computer_choice = game.get_computer_choice(difficulty)
        
        game.display_choices(user_choice, computer_choice)
        result = game.determine_winner(user_choice, computer_choice)
        
        if result == "user":
            user_score += 1
        elif result == "computer":
            computer_score += 1
            
        game.display_result(result, user_score, computer_score, round_num, total_rounds)
        
        # Check for early win
        if user_score >= rounds_to_win:
            print(f"\n🎊 You won the match {user_score}-{computer_score}!")
            break
        elif computer_score >= rounds_to_win:
            print(f"\n🤖 Computer won the match {computer_score}-{user_score}!")
            break
            
        print("-" * 40)
    
    return user_score, computer_score, round_num

def main():
    """Main game function"""
    print("🎮 Welcome to Rock Paper Scissors DELUXE!")
    print("=" * 45)
    
    game_mode = get_game_mode()
    difficulty = get_difficulty()
    
    difficulty_names = {"easy": "Easy 😌", "normal": "Normal 😐", "hard": "Hard 😤"}
    print(f"\n🎲 Starting game - Difficulty: {difficulty_names[difficulty]}")
    
    if game_mode:
        print(f"🎯 Mode: Best of {game_mode}")
    else:
        print("🎯 Mode: Quick Play (unlimited rounds)")
    
    game = RockPaperScissors()
    
    if game_mode:
        user_score, computer_score, rounds_played = play_best_of_mode(game, difficulty, game_mode)
    else:
        user_score, computer_score, rounds_played = play_unlimited_mode(game, difficulty)
    
    # Final results
    print(f"\n🏆 Final Results after {rounds_played} rounds:")
    print(f"You: {user_score} wins")
    print(f"Computer: {computer_score} wins")
    
    if user_score > computer_score:
        print("🎊 Congratulations! You're the champion!")
    elif computer_score > user_score:
        print("🤖 Computer is the champion! Better luck next time!")
    else:
        print("🤝 Perfect tie! Amazing game!")
    
    # Show some stats for hard mode
    if difficulty == "hard" and len(game.user_patterns) > 0:
        most_used = max(set(game.user_patterns), key=game.user_patterns.count)
        print(f"📊 Your most used move: {most_used} {game.emojis[most_used]}")
    
    print("Thanks for playing! 👋")

if __name__ == "__main__":
    main()