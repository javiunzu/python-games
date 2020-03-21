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

    def __init__(self, width, height):
        """
        Initializes the value matrix. the drawing surface and the color values.
        :param width: Number of rows.
        :param height: Number of columns.
        """
        self.width = width
        self.height = height
        self.cells = numpy.zeros((width, height))
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
        for x in range(0, self.width):
            for y in range(0, self.height):
                pygame.draw.circle(self.surface,
                                   {-1: self.p2color,
                                    0: self.bgcolor,
                                    1: self.p1color}[self.cells[x][y]],
                                   (x * self.cell_size + self.cell_size // 2, self.cell_size + y * self.cell_size + self.cell_size // 2),
                                   self.cell_size // 2 - self.cell_size // 10)


def main():

    board = Board(7, 6)
    pygame.init()
    turn = 1
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for window close.
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                # Get mouse position and map it to a column.
                print(event.pos)
                column = event.pos[0] // board.cell_size
                row = event.pos[1] // board.cell_size
                print("col {}".format(column))
                # Find the first non zero cell on that column and set it to the turn marker.
                row = board.height - 1 if numpy.count_nonzero(board.cells[column]) == 0 else numpy.nonzero(board.cells[column])[0][0] - 1
                print("row {}".format(row))
                if row >= 0:
                    board.cells[column][row] = turn
                    turn *= -1  # Change to the other player.

        board.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()