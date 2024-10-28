import pygame
import sys
from game_logic import Game2048
from bfs_ai import BFSPlayer
from dfs_ai import DFSPlayer
from astar_ai import AStarPlayer

pygame.init()

def get_all_heuristics():
    """Return a dictionary of all available heuristics for A*."""
    return {
        "Empty Tiles": "empty_tiles",
        "Max Tile": "max_tile",
        "Monotonicity": "monotonicity",
        "Clustering": "clustering"
    }

def run_game(player_type, heuristic=None):
    """Run a single game using the specified AI strategy and return the final score."""
    game = Game2048()
    
    # Instantiate the strategy dynamically, including heuristic choice for A*
    if heuristic:
        player = player_type(game, heuristic)
    else:
        player = player_type(game)

    while not game.is_game_over():
        best_move = player.get_best_move()

        if best_move in ["left", "right", "up", "down"]:
            getattr(game, f"move_{best_move}")()  # Execute the valid move
        else:
            print(f"Invalid move: {best_move}")
            break  # Stop if an invalid move is returned

    return game.score  # Return the final score

def run_all_strategies(runs_per_strategy):
    """Run BFS, DFS, and all A* heuristics multiple times and calculate the average score."""
    strategies = {
        "BFS": BFSPlayer,
        "DFS": DFSPlayer
    }

    heuristics = get_all_heuristics()  # Get all A* heuristics
    total_scores = {name: 0 for name in strategies}
    total_scores.update({f"A* ({h})": 0 for h in heuristics})  # Track scores for all heuristics
    results = {name: [] for name in strategies}
    results.update({f"A* ({h})": [] for h in heuristics})

    # Run BFS and DFS strategies
    for name, strategy in strategies.items():
        for i in range(runs_per_strategy):
            print(f"Running {name} Strategy - Run {i + 1}")
            score = run_game(strategy)
            total_scores[name] += score
            results[name].append(score)
            print(f"Result: {name} - Run {i + 1} - Final Score: {score}")

    # Run A* strategy for each heuristic
    for heuristic_name, heuristic_key in heuristics.items():
        for i in range(runs_per_strategy):
            print(f"Running A* ({heuristic_name}) - Run {i + 1}")
            score = run_game(AStarPlayer, heuristic_key)
            total_scores[f"A* ({heuristic_name})"] += score
            results[f"A* ({heuristic_name})"].append(score)
            print(f"Result: A* ({heuristic_name}) - Run {i + 1} - Final Score: {score}")

    print("\nAll Results:")
    for name, scores in results.items():
        for i, score in enumerate(scores, 1):
            print(f"{name} - Run {i}: Final Score = {score}")

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
    runs_per_strategy = get_runs_per_strategy()
    run_all_strategies(runs_per_strategy)
    pygame.quit()
    sys.exit()
