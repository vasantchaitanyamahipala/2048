import pygame
import sys
from game_logic import Game2048
from bfs_ai import BFSPlayer
from dfs_ai import DFSPlayer
from astar_ai import AStarPlayer  # Import AStarPlayer

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
FONT = pygame.font.Font(None, 40)

def draw_board(screen, game):
    """Draw the 2048 game board with grid lines."""
    screen.fill((187, 173, 160))  # Background color

    # Draw the tiles
    for i in range(4):
        for j in range(4):
            tile = game.board[i][j]
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (205, 193, 180) if tile == 0 else (238, 228, 218), rect)
            if tile != 0:
                text = FONT.render(str(tile), True, (119, 110, 101))
                screen.blit(text, text.get_rect(center=rect.center))

    # Draw the grid lines
    line_color = (119, 110, 101)  # Grey color for the grid lines
    for i in range(1, 4):
        pygame.draw.line(screen, line_color, (0, i * TILE_SIZE), (WIDTH, i * TILE_SIZE), 2)
        pygame.draw.line(screen, line_color, (i * TILE_SIZE, 0), (i * TILE_SIZE, HEIGHT), 2)

    pygame.display.flip()

def run_game(player_type):
    """Helper function to run the game with the specified player strategy."""
    game = Game2048()
    player = player_type(game)  # Inject strategy dynamically

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 with AI")

    clock = pygame.time.Clock()

    valid_moves = {"left", "right", "up", "down"}  # Set of valid move names

    while True:
        draw_board(screen, game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # AI makes a move
        best_move = player.get_best_move()
        if best_move in valid_moves:  # Ensure the move is valid
            getattr(game, f"move_{best_move}")()  # Execute the valid move
        else:
            print(f"Invalid move detected: {best_move}")  # Debugging print

        # Check for game over
        if game.is_game_over():
            print(f"Game Over! Final Score: {game.score}")
            pygame.quit()
            sys.exit()  # Ensure the program exits after printing the score

        clock.tick(1)  # Control the speed of AI moves


def select_player():
    """Prompt the user to select a player strategy and heuristic."""
    while True:
        choice = input("Select AI strategy (bfs/dfs/astar): ").strip().lower()
        if choice == "bfs":
            return BFSPlayer
        elif choice == "dfs":
            return DFSPlayer
        elif choice == "astar":
            heuristic = select_astar_heuristic()
            return lambda game: AStarPlayer(game, heuristic_choice=heuristic)
        else:
            print("Invalid choice. Please enter 'bfs', 'dfs', or 'astar'.")

def select_astar_heuristic():
    """Prompt the user to select a heuristic for A* strategy."""
    while True:
        print("Select A* heuristic:")
        print("1. Empty Tiles")
        print("2. Max Tile")
        print("3. Monotonicity")
        print("4. Clustering")
        choice = input("Enter the number of your choice: ").strip()
        if choice == "1":
            return "empty_tiles"
        elif choice == "2":
            return "max_tile"
        elif choice == "3":
            return "monotonicity"
        elif choice == "4":
            return "clustering"
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    # Get user input to select the strategy and run the game
    player_type = select_player()
    run_game(player_type)
