from collections import deque
from player import Player

class BFSPlayer(Player):
    def __init__(self, game):
        self.game = game

    def bfs(self, max_depth=3):
        """Perform BFS to find the best move up to a given depth."""
        queue = deque([(self.game.board, self.game.score, [])])
        best_score = self.game.score
        best_moves = []

        while queue:
            board, score, moves = queue.popleft()

            if len(moves) >= max_depth:
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
                    queue.append((self.game.board, self.game.score, moves + [move_name]))

                self.game.board = temp_board
                self.game.score = temp_score

        return best_moves[0] if best_moves else None

    def get_best_move(self):
        """Return the best move using BFS."""
        return self.bfs()
