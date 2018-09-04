class BooleanModel:
    """BooleanModel is the model built to hold the raw data behind the cells of LifeGUI."""

    def __init__(self, grid: list):
        """Construct a BooleanModel object.

        GRID is a two-dimensional Boolean list that describes each corresponding cell of LifeGUI.
        GENERATION is the integer value of the generation which is being displayed in the LifeGUI view.
        ALIVE is the Boolean variable which corresponds with True in the grid.
        DEAD is the Boolean variable which corresponds with False in the grid.
        """
        self.grid = grid
        self.generation = 0
        self.alive = True
        self.dead = False

    def next_generation(self):
        """Updates BooleanModel to the next generation based on the rules of Conway's Game of Life."""
        self.generation += 1

        grid_copy = list()
        for row in range(len(self.grid)):
            grid_copy.append(list())
            for col in range(len(self.grid[0])):
                grid_copy[row].append(self.grid[row][col])

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.num_adjacent_alive(row, col, grid_copy) == 0 or self.num_adjacent_alive(row, col, grid_copy) == 1:
                    self.grid[row][col] = self.dead
                elif self.num_adjacent_alive(row, col, grid_copy) == 2 or self.num_adjacent_alive(row, col, grid_copy) == 3:
                    if self.num_adjacent_alive(row, col, grid_copy) == 3:
                        self.grid[row][col] = self.alive
                elif self.num_adjacent_alive(row, col, grid_copy) > 3:
                    self.grid[row][col] = self.dead

    def num_adjacent_alive(self, row: int, col: int, grid_copy: list) -> int:
        """Returns the cells adjacent to the given cell which are alive.

        ROW is the row index of the given cell.
        COL is the column index of the given cell.
        GRID_COPY is a copy of the current grid which does not hold references to it.
        """
        moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        valid_moves = list()

        num = 0

        for move in range(8):
            if (0 <= (row + moves[move][1]) < len(self.grid)) and (0 <= (col + moves[move][0]) < len(self.grid[0])):
                valid_moves.append(moves[move])

        if len(valid_moves) != 0:
            for valid_move in valid_moves:
                if grid_copy[row + valid_move[1]][col + valid_move[0]] == self.alive:
                    num += 1
            return num
        else:
            return 0

    def set_false_color(self):
        """Sets all of the cells in the grid to DEAD."""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.grid[row][col] = self.dead
