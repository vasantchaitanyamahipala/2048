import pygame
import sys
from game_logic import Game2048
from bfs_ai import BFSPlayer
from dfs_ai import DFSPlayer
from astar_ai import AStarPlayer

pygame.init()

def run_game(player_type):
    """Run a single game using the specified AI strategy and return the final score."""
    game = Game2048()
    player = player_type(game)  # Instantiate the strategy dynamically

    while not game.is_game_over():
        best_move = player.get_best_move()

        # Validate that the move is valid
        if best_move in ["left", "right", "up", "down"]:
            getattr(game, f"move_{best_move}")()  # Execute the valid move
        else:
            print(f"Invalid move: {best_move}")  # Debugging log
            break  # Stop if an invalid move is returned

    return game.score  # Return the final score

def run_all_strategies(runs_per_strategy):
    """Run BFS, DFS, and A* strategies multiple times and calculate the average score."""
    strategies = {
        "BFS": BFSPlayer,
        "DFS": DFSPlayer,
        "A*": AStarPlayer
    }

    total_scores = {name: 0 for name in strategies}  # Store the total score for each strategy
    results = {name: [] for name in strategies}  # Store individual run scores for reference

    # Run each strategy the specified number of times
    for name, strategy in strategies.items():
        for i in range(runs_per_strategy):
            print(f"Running {name} Strategy - Run {i + 1}")
            score = run_game(strategy)
            total_scores[name] += score  # Accumulate the total score
            results[name].append(score)  # Store individual score
            print(f"Result: {name} - Run {i + 1} - Final Score: {score}")
    # Print all individual results
    print("\nAll Results:")
    for name, scores in results.items():
        for i, score in enumerate(scores, 1):
            print(f"{name} - Run {i}: Final Score = {score}")

    # Calculate and print the average score for each strategy
    print("\nAverage Scores:")
    for name, total in total_scores.items():
        average_score = total / runs_per_strategy
        print(f"{name}: Average Score = {average_score:.2f}")



def get_runs_per_strategy():
    """Prompt the user to enter the number of runs per strategy."""
    while True:
        try:
            runs = int(input("How many times do you want to run each strategy? "))
            if runs > 0:
                return runs
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    # Get the number of runs per strategy from the user
    runs_per_strategy = get_runs_per_strategy()
    
    # Run all strategies the specified number of times
    run_all_strategies(runs_per_strategy)
    
    # Quit Pygame and exit
    pygame.quit()
    sys.exit()
