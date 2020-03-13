#!/usr/bin/env python3
"""
Pong game.
Object oriented reimplementation of the one found here.
http://christianthompson.com/sites/default/files/Pong/pong.py
It adds a game-ending condition.
"""
import turtle
import time


class Shape:
    """ Base class for shapes """
    def __init__(self):
        self.sprite = turtle.Turtle()
        self.sprite.speed(0)
        self.sprite.shape('square')
        self.sprite.color('white')
        self.sprite.penup()

    @property
    def xcor(self):  # To write less.
        return self.sprite.xcor()

    @property
    def ycor(self):
        return self.sprite.ycor()


class Paddle(Shape):
    """
    The paddle. It doesn't do anything other than moving up and down.
    """
    def __init__(self, *pos):
        super().__init__()
        self.sprite.shapesize(stretch_wid=5, stretch_len=1)
        self.sprite.penup()
        self.sprite.goto(pos)

    def move(self, ycoord=0):
        """
        Updates the position of the paddle by adding the value of ycoord.
        :param ycoord: Int. Add this to the Y-axis position. Negative values make the paddle go down.
        """
        self.sprite.sety(self.sprite.ycor() + ycoord)
        if  self.sprite.ycor() < -250:
            self.sprite.sety(-250)
        if self.sprite.ycor() > 250:
            self.sprite.sety(250)


class Ball(Shape):
    """
    The ball. It moves in both axes simultaneously and bounces when it encounters an obstacle.
    """
    def __init__(self):
        super().__init__()
        self.sprite.goto(0, 0)
        self.dx = 1  # Acceleration on x
        self.dy = 1  # Acceleration on y

    def bounce(self, axis):
        """
        Bounces on the specified axis, which is just inverting the acceleration.
        :param axis: String with either an x or a y.
        """
        assert axis in ('x', 'y'), 'Only "x" and "y" are valid values.'
        direction = {'x': 'dx', 'y': 'dy'}
        print(f'boink {direction[axis]}')
        setattr(self, direction[axis], getattr(self, direction[axis]) * -1)

    def move(self, paddle_a, paddle_b, score):
        """
        Updates the position of the ball on the screen. Adds the acceleration values to the position.
        :param paddle_a: Paddle object that represents the first player. Needed for collisions.
        :param paddle_b: Paddle for the second player.
        :param score: Score. It will be updated when a player scores.
        """
        self.sprite.setx(self.xcor + self.dx)
        self.sprite.sety(self.ycor + ball.dy)
        # Bounce on floor and ceiling.
        if self.ycor > 290 or self.ycor < -290:
            # self.sprite.sety(290)
            self.bounce('y')
        # Score
        if self.xcor > 350:
            score.player1 += 1
            self.sprite.goto(0,0)
            self.bounce('x')
            score.update()
            print('Player 1 scores ^^')
        elif self.xcor < -350:
            score.player2 +=1
            self.sprite.goto(0,0)
            self.bounce('x')
            score.update()
            print('Player 2 scores ^^')
        # Detect paddle collision
        if self.xcor < -340 and self.ycor < paddle_a.ycor + 50 and self.ycor > paddle_a.ycor -50:
            self.bounce('x')
        elif self.xcor > 340 and self.ycor < paddle_b.ycor + 50 and self.ycor > paddle_b.ycor - 50:
            self.bounce('x')


class Score:
    """
    A scoreboard on top of the screen.
    """
    def __init__(self):
        self.sprite = turtle.Turtle()
        self.sprite.speed(0)
        self.sprite.color('white')
        self.sprite.penup()
        self.sprite.hideturtle()
        self.sprite.goto(0, 260)
        self.player1 = 0
        self.player2 = 0

    def __repr__(self):
        return f'{self.player1}:{self.player2}'

    @property
    def winner(self):
        return '1' if self.player1 > self.player2 else '2'

    def update(self):
        """
        Re-draw the board on the screen with the updated values.
        """
        self.sprite.clear()
        self.sprite.write(str(self), align='center', font=('Courier', 24, 'normal'))


if __name__ == '__main__':
    window = turtle.Screen()
    window.title('Pong')
    window.bgcolor('black')
    window.setup(width=800, height=600)
    window.tracer(0)

    paddle_a = Paddle(-350, 0)
    paddle_b = Paddle(350, 0)
    ball = Ball()
    score = Score()

    # Key bindings (onkeypress only accepts lambdas)
    window.listen()
    window.onkeypress(lambda: paddle_a.move(20), 'w')
    window.onkeypress(lambda: paddle_a.move(-20), 's')
    window.onkeypress(lambda: paddle_b.move(20), 'Up')
    window.onkeypress(lambda: paddle_b.move(-20), 'Down')

    score.update()

    while max(score.player1, score.player2) < 10:
        ball.move(paddle_a, paddle_b, score)  # Ball must be aware of the paddles' position and the score.
        time.sleep(0.005)  # Without a delay it goes as fas as the CPU --> unplayable.
        window.update()
    else:
        message = turtle.Turtle()
        message.speed(0)
        message.color('yellow')
        message.penup()
        message.hideturtle()
        message.goto(0, 130)
        message.write(f'Player {score.winner} wins!', align='center', font=('Courier', 24, 'normal'))

    time.sleep(5)
