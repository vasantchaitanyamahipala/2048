import random

class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.reset()

    def reset(self):
        """Reset the board and add two random tiles."""
        self.board = [[0] * 4 for _ in range(4)]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a new tile with value 2 or 4 to a random empty spot."""
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2

    def move_left(self):
        """Move tiles to the left."""
        changed = False
        for row in self.board:
            merged = self.merge([tile for tile in row if tile != 0])
            if merged != row:
                changed = True
            row[:] = merged + [0] * (4 - len(merged))
        if changed:
            self.add_random_tile()

    def merge(self, row):
        """Merge row tiles if adjacent values are the same."""
        merged = []
        skip = False
        for i in range(len(row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(row) and row[i] == row[i + 1]:
                merged.append(row[i] * 2)
                self.score += row[i] * 2
                skip = True
            else:
                merged.append(row[i])
        return merged

    def rotate_clockwise(self):
        """Rotate the board clockwise."""
        self.board = [list(row) for row in zip(*self.board[::-1])]

    def move_right(self):
        """Move tiles to the right."""
        self.rotate_clockwise()
        self.rotate_clockwise()
        self.move_left()
        self.rotate_clockwise()
        self.rotate_clockwise()

    def move_up(self):
        """Move tiles up."""
        self.rotate_clockwise()
        self.rotate_clockwise()
        self.rotate_clockwise()
        self.move_left()
        self.rotate_clockwise()

    def move_down(self):
        """Move tiles down."""
        self.rotate_clockwise()
        self.move_left()
        self.rotate_clockwise()
        self.rotate_clockwise()
        self.rotate_clockwise()

    def is_game_over(self):
        """Check if there are no valid moves left."""
        # Create a temporary copy of the board and score
        temp_board = [row[:] for row in self.board]
        temp_score = self.score

        # Check if any move changes the board state
        for move in [self.move_left, self.move_right, self.move_up, self.move_down]:
            self.board = [row[:] for row in temp_board]  # Reset the board
            self.score = temp_score  # Reset the score
            move()
            if self.board != temp_board:  # If the board changed, the game is not over
                return False

        # If no move changes the board, the game is over
        return True
