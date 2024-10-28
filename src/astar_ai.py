from player import Player
import heapq

class AStarPlayer(Player):
    def __init__(self, game, heuristic_choice):
        self.game = game
        self.heuristic_function = self.get_heuristic(heuristic_choice)

    def get_heuristic(self, heuristic_choice):
        """Select the heuristic function based on user input."""
        heuristics = {
            "empty_tiles": self.heuristic_empty_tiles,
            "max_tile": self.heuristic_max_tile,
            "monotonicity": self.heuristic_monotonicity,
            "clustering": self.heuristic_clustering,
        }
        return heuristics.get(heuristic_choice, self.heuristic_empty_tiles)

    def heuristic_empty_tiles(self, board):
        """Heuristic: Number of empty tiles."""
        return sum(tile == 0 for row in board for tile in row)

    def heuristic_max_tile(self, board):
        """Heuristic: Maximum tile value."""
        return max(tile for row in board for tile in row)

    def heuristic_monotonicity(self, board):
        """Heuristic: Penalize non-monotonic sequences."""
        penalty = 0
        for row in board:
            for i in range(len(row) - 1):
                if row[i] > row[i + 1]:
                    penalty += 1
        return penalty

    def heuristic_clustering(self, board):
        """Heuristic: Penalize large tiles being far apart."""
        penalty = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] > 0:
                    neighbors = self.get_neighbors(board, i, j)
                    penalty += sum(abs(board[i][j] - n) for n in neighbors)
        return penalty

    def get_neighbors(self, board, i, j):
        """Get the neighbors of a tile at position (i, j)."""
        neighbors = []
        if i > 0:
            neighbors.append(board[i - 1][j])
        if i < len(board) - 1:
            neighbors.append(board[i + 1][j])
        if j > 0:
            neighbors.append(board[i][j - 1])
        if j < len(board[i]) - 1:
            neighbors.append(board[i][j + 1])
        return neighbors

    def astar(self):
        """Perform A* search to find the best move."""
        priority_queue = []
        initial_heuristic = self.heuristic_function(self.game.board)
        heapq.heappush(priority_queue, (initial_heuristic, self.game.board, self.game.score, []))
        best_score = self.game.score
        best_moves = []

        while priority_queue:
            _, board, score, moves = heapq.heappop(priority_queue)

            if len(moves) >= 3:  # Limit the depth to avoid long computations
                if score > best_score:
                    best_score = score
                    best_moves = moves
                continue

            for move_func, move_name in [
                (self.game.move_left, 'left'),
                (self.game.move_right, 'right'),
                (self.game.move_up, 'up'),
                (self.game.move_down, 'down')
            ]:
                temp_board = [row[:] for row in self.game.board]
                temp_score = self.game.score

                self.game.board = board
                self.game.score = score
                move_func()

                if self.game.board != temp_board:
                    heuristic_value = self.heuristic_function(self.game.board)
                    heapq.heappush(
                        priority_queue,
                        (heuristic_value, self.game.board, self.game.score, moves + [move_name])
                    )

                self.game.board = temp_board
                self.game.score = temp_score

        return best_moves[0] if best_moves else None

    def get_best_move(self):
        """Return the best move using A*."""
        return self.astar()
