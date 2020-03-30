import numpy
import pygame


class Board:
    """
    The board is represented by a matrix. The values of that matrix represent the following states:
    0: Free cell.
    1: First player's token.
    -1: Second player's token.
    """
    cell_size = 80
    turn = 1

    def __init__(self, width, height):
        """
        Initializes the value matrix. the drawing surface and the color values.
        :param width: Number of rows.
        :param height: Number of columns.
        """
        self.width = width
        self.height = height
        self.cells = numpy.zeros((height, width))
        self.surface = pygame.display.set_mode((self.cell_size * width, self.cell_size * (height + 1)))
        self.bgcolor = (0, 0, 0)
        self.fgcolor = (0, 0, 255)
        self.p1color = (255, 0, 0)
        self.p2color = (255, 255, 0)

    def __repr__(self):
        return str(self.cells)

    def draw(self):
        self.surface.fill(self.bgcolor)
        # Draw one big blue rectangle
        pygame.draw.rect(self.surface, self.fgcolor,
                         (0, self.cell_size, self.width * self.cell_size, self.height * self.cell_size))
        for y in range(0, self.height):
            for x in range(0, self.width):
                pygame.draw.circle(self.surface,
                                   {-1: self.p2color,
                                    0: self.bgcolor,
                                    1: self.p1color}[self.cells[y][x]],
                                   (x * self.cell_size + self.cell_size // 2, self.cell_size + y * self.cell_size + self.cell_size // 2),
                                   self.cell_size // 2 - self.cell_size // 10)
        # Draw turn indicator
        pygame.draw.circle(self.surface,
                           {-1: self.p2color,
                            1: self.p1color}[self.turn],
                           (self.cell_size // 2, self.cell_size // 2),
                           self.cell_size // 2 - self.cell_size // 10)

    def drop(self, pos):
        """
        Get mouse position and map it to a column.
        When doing the conversion from screen coordinates to a cell, it's important to know that screen coordinates
        take as origin the upper-left corner of the screen and indexes columns-first, and numpy indexes arrays rows-first.
        :param pos: Tuple with screen coordinates.
        :returns: Tuple with the position where the token "drops". if there is no place in the column, returns None.
        """
        column = pos[0] // self.cell_size
        # Find the first non zero cell on that column and set it to the turn marker.
        row = self.height - 1 if numpy.count_nonzero(self.cells[:, column]) == 0 else numpy.nonzero(self.cells[:, column])[0][0] - 1
        if row >= 0:
            self.cells[row, column] = self.turn
            print(self.cells)
            self.turn *= -1  # Change to the other player.
            return row, column
        else:
            return None

    def finished(self, row, column):
        """
        Checks if a slot is part of a four-in-a-row.
        Slides a 4-position window over the horizontal, the vertical, and the two diagonals.
        It's the most efficient solution I can come up with, as the operational cost remains the same, no matter how big the board is.
        :param row: Integer value of the row.
        :param column: Integer value of the column.
        :return: True if four in a row are found. False otherwise
        """
        value = self.cells[row, column]
        if value != 0:
            # Define the boundaries
            min_row = max(0, row - 3)
            max_row = min(self.height - 1, row + 3)
            min_col = max(0, column - 3)
            max_col = min(self.width - 1, column + 3)
            # Check horizontal line
            for c in range(min_col, min(max_col - 2, min_col + 4)):
                if numpy.all(value == self.cells[row, c:c+4]):
                    return True
            # Check vertical line
            for r in range(min_row, min(max_row - 2, min_row + 4)):
                if numpy.all(value == self.cells[r:r+4, column]):
                    return True
            # Check diagonal with negative slope. It is way easier to build a fixed-sized submatrix and skip the iteration if you end out of bounds rather than calculating the correct indexes.
            for d in range(0, 4):
                try:
                    vector = self.cells[row - 3 + d:row + 1 + d, column - 3 + d:column + 1 + d].diagonal()
                    if numpy.all(value == vector) and len(vector) == 4:
                        return True
                except IndexError:
                    continue
            # Check diagonal with positive slope. Same as before, but flipping the submatrix, as diagonal() works with the main diagonal.
            for d in range(0, 4):
                try:
                    vector = numpy.fliplr(self.cells[row - d:row + 4 - d, column - 3 + d:column + 1 + d]).diagonal()
                    if numpy.all(value == vector) and len(vector) == 4:
                        return True
                except IndexError:
                    continue

        return False


    def reset(self):
        self.cells = numpy.zeros((self.height, self.width))


def main():

    board = Board(7, 6)
    pygame.init()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for window close.
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = board.drop(event.pos)
                # Is the game ended?
                if board.finished(*pos):
                    print("Game over")

        board.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
