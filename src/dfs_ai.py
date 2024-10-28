from player import Player

class DFSPlayer(Player):
    def __init__(self, game):
        self.game = game

    def dfs(self, depth):
        """Perform DFS to find the best move."""
        if depth == 0 or self.game.is_game_over():
            return self.game.score

        max_score = self.game.score
        best_move = None

        for move_func, move_name in [
            (self.game.move_left, 'left'),
            (self.game.move_right, 'right'),
            (self.game.move_up, 'up'),
            (self.game.move_down, 'down')
        ]:
            # Create a temporary copy of the board and score
            temp_board = [row[:] for row in self.game.board]
            temp_score = self.game.score

            # Perform the move
            move_func()

            # If the move changed the board, recurse into deeper levels
            if self.game.board != temp_board:
                score = self.dfs(depth - 1)
                if isinstance(score, int) and score > max_score:
                    max_score = score
                    best_move = move_name

            # Restore the original board and score
            self.game.board = temp_board
            self.game.score = temp_score

        return best_move if best_move else max_score

    def get_best_move(self):
        """Return the best move using DFS."""
        return self.dfs(3)  # Search depth 6
