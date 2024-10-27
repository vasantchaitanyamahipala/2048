from player import Player
import heapq

class AStarPlayer(Player):
    def __init__(self, game):
        self.game = game

    def heuristic(self):
        """Heuristic function: Minimize the number of empty tiles."""
        return sum(tile == 0 for row in self.game.board for tile in row)

    def astar(self):
        """Perform A* search to find the best move."""
        priority_queue = []
        heapq.heappush(priority_queue, (self.heuristic(), self.game.board, self.game.score, []))
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
                    heapq.heappush(
                        priority_queue,
                        (self.heuristic(), self.game.board, self.game.score, moves + [move_name])
                    )

                self.game.board = temp_board
                self.game.score = temp_score

        return best_moves[0] if best_moves else None

    def get_best_move(self):
        """Return the best move using A*."""
        return self.astar()
