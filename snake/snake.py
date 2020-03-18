#!/usr/bin/env python
"""
Snake game using pygame
"""
import random
import pygame


class Grid:
    """ The board. As visual help, the lines are drawn."""
    def __init__(self, width, rows):
        self.width = width
        self.rows = rows
        self.size = self.width // self.rows
        self.window = pygame.display.set_mode((self.width, self.width))
        self.bgcolor = (0, 0, 0)
        self.linecolor = (50, 50, 50)

    def draw(self):
        self.window.fill(self.bgcolor)
        for l in range(0, self.width, self.size):
            pygame.draw.line(self.window, self.linecolor, (l, 0), (l, self.width))
            pygame.draw.line(self.window, self.linecolor, (0, l), (self.width, l))


class Cube:
    """ A cube on the grid. """
    def __init__(self, grid, pos, color=(255, 0, 0)):
        """
        Constructor
        :param grid: The grid where the cube is drawn.
        :param pos: Coordinates (x, y) where the cube is placed. These are grid coordinates, not display coordinates.
        :param color: RGB values as a tuple.
        """
        self.grid = grid
        self.side = self.grid.size
        self.pos = pos
        self.direction = (1, 0)
        self.color = color

    def move(self, direction):
        """
        Move to a new position on the grid and change the trajectory.
        :param direction: Tuple with the direction (x, y)
        """
        self.direction = direction
        self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

    def draw(self):
        """ Draws the cube in the correct grid cell. """
        pygame.draw.rect(self.grid.window, self.color,
                         (self.pos[0] * self.side + 1, self.pos[1] * self.side + 1, self.side - 2, self.side - 2))


class Snake(object):
    """
    A moving sequence of cubes.
    To move over a grid, we need to store the position of the cubes and in which squares they turn and in which direction (what we call a trail).
    The trail will map grid positions to directions and will be as long as the snake is.
    When a the snake turns, a new entry is added. When the last body segment passes through an entry, the entry is removed.
    """
    def __init__(self, grid, color, pos):
        self.grid = grid
        self.color = color
        self.head = Cube(self.grid, pos, color=self.color)
        self.body = [self.head]
        self.trail = {}
        self.direction = (0, 1)

    def move(self):
        """ Slide the segments of the body through the trail. """
        for segment in self.body:
            p = segment.pos
            if segment.pos in self.trail:
                turn = self.trail[p]
                segment.move((turn[0], turn[1]))
                if segment == self.body[-1]:
                    self.trail.pop(p)
            else:
                if segment.direction[0] == -1 and segment.pos[0] <= 0:
                    segment.pos = (segment.grid.rows - 1, segment.pos[1])
                elif segment.direction[0] == 1 and segment.pos[0] >= segment.grid.rows - 1:
                    segment.pos = (0, segment.pos[1])
                elif segment.direction[1] == 1 and segment.pos[1] >= segment.grid.rows - 1:
                    segment.pos = (segment.pos[0], 0)
                elif segment.direction[1] == -1 and segment.pos[1] <= 0:
                    segment.pos = (segment.pos[0], segment.grid.rows - 1)
                else:
                    segment.move(segment.direction)

    def reset(self):
        """ Reset snake's body and trail. """
        self.body = [self.head]
        self.trail = {}
        self.direction = (0, 1)

    def add_segment(self):
        """ Add a new segment to the snake's body. """
        tail = self.body[-1]
        if tail.direction == (1, 0):
            self.body.append(Cube(self.grid, (tail.pos[0] - 1, tail.pos[1]), color=self.color))
        elif tail.direction == (-1, 0):
            self.body.append(Cube(self.grid, (tail.pos[0] + 1, tail.pos[1]), color=self.color))
        elif tail.direction == (0, 1):
            self.body.append(Cube(self.grid, (tail.pos[0], tail.pos[1] - 1), color=self.color))
        elif tail.direction == (0, -1):
            self.body.append(Cube(self.grid, (tail.pos[0], tail.pos[1] + 1), color=self.color))
        self.body[-1].direction = tail.direction

    def draw(self):
        """ Plots the snake on the grid. """
        for segment in self.body:
            segment.draw()
            if segment == self.head:  # Draw eyes on the head.
                centre = segment.side // 2
                radius = 3
                eye1 = (segment.pos[0] * segment.side + centre - radius, segment.pos[1] * segment.side + 8)
                eye2 = (segment.pos[0] * segment.side + segment.side - radius * 2, segment.pos[1] * segment.side + 8)
                pygame.draw.circle(self.grid.window, (0, 0, 0), eye1, radius)
                pygame.draw.circle(self.grid.window, (0, 0, 0), eye2, radius)


def random_cell(grid, snake):
    """
    Generates a new random position on the space of free cells.
    :param grid: The grid.
    :param snake: The snake whose body will represent occupied cells.
    :returns: Position of a free cell.
    """
    while True:
        x = random.randrange(grid.rows)
        y = random.randrange(grid.rows)
        if len(list(filter(lambda z: z.pos == (x, y), snake.body))) > 0:
            continue
        else:
            break

    return x, y


def pause():
    """ Pauses the game until a key is pressed. """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # I need this to be able to close the game while paused.
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return


def main():
    width = 500
    rows = 20
    grid = Grid(width, rows)
    snake = Snake(grid, (0, 255, 0), (10, 10))
    snack = Cube(grid, random_cell(rows, snake), color=(255, 0, 0))
    pygame.init()
    myfont = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    # You will want to use a clock to set the pace of the game, otherwise it will run as fast as your CPU can.
    clock = pygame.time.Clock()
    while True:  # Game loop.
        clock.tick(10)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for window close.
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # Check for key presses.
                if event.key == pygame.K_LEFT:
                    snake.direction = (-1, 0)
                    snake.trail[snake.head.pos[:]] = [snake.direction[0], snake.direction[1]]
                elif event.key == pygame.K_RIGHT:
                    snake.direction = (1, 0)
                    snake.trail[snake.head.pos[:]] = [snake.direction[0], snake.direction[1]]
                elif event.key == pygame.K_UP:
                    snake.direction = (0, -1)
                    snake.trail[snake.head.pos[:]] = [snake.direction[0], snake.direction[1]]
                elif event.key == pygame.K_DOWN:
                    snake.direction = (0, 1)
                    snake.trail[snake.head.pos[:]] = [snake.direction[0], snake.direction[1]]
        snake.move()
        # Check collisions: Snack.
        if snake.body[0].pos == snack.pos:
            snake.add_segment()
            snack = Cube(grid, random_cell(rows, snake), color=(255, 0, 0))
        # Check collisions: Own body.
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print('Score: ', len(snake.body))
                grid.window.blits([(myfont.render('GAME OVER', False, (255, 255, 255)), (200, 230)),
                                   (myfont.render('Press a key to continue ...', False, (255, 255, 255)), (150, 270))])
                pygame.display.update()
                pause()
                snake.reset()
                break
        grid.draw()
        snake.draw()
        snack.draw()
        scoretext = myfont.render('Score: {}'.format(len(snake.body) - 1), False, (255, 255, 255))
        grid.window.blit(scoretext, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    main()
