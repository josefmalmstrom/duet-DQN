import turtle
from ball import Ball


BOARD_HEIGHT = 750
BOARD_WIDTH = 550

BALL_DIAMETER = 10   # size of red/blue balls
CIRCLE_RADIUS = 100   # distance between the balls

# distance from balls to bottom of board
DIST_TO_BOTTOM = CIRCLE_RADIUS + 10


class DuetGame(object):

    def __init__(self):

        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.title("Duet Game")

        self.init_game_board()
        self.init_balls()

    def init_game_board(self):
        """
        Draws the game board.
        """

        border_pen = turtle.Turtle()
        border_pen.speed(0)
        border_pen.color("white")
        border_pen.penup()
        border_pen.setposition(-BOARD_WIDTH/2, -BOARD_HEIGHT/2)
        border_pen.pendown()
        border_pen.pensize(3)
        for side in range(2):
            border_pen.forward(BOARD_WIDTH)
            border_pen.left(90)
            border_pen.forward(BOARD_HEIGHT)
            border_pen.left(90)
        border_pen.hideturtle()

    def init_balls(self):
        """
        Initializes the red and blue balls.
        """

        self.blue_ball = turtle.Turtle()
        self.blue_ball.penup()
        self.blue_ball.speed(0)
        self.blue_ball.color("blue")
        self.blue_ball.shape("circle")
        self.blue_ball.resizemode("user")
        self.blue_ball.shapesize(1.3, 1.3)
        blue_start_pose = (-CIRCLE_RADIUS, -BOARD_HEIGHT/2 + DIST_TO_BOTTOM)
        self.blue_ball.setposition(*blue_start_pose)
        self.blue_ball.right(90)

        self.red_ball = turtle.Turtle()
        self.red_ball.penup()
        self.red_ball.speed(0)
        self.red_ball.color("red")
        self.red_ball.shape("circle")
        self.red_ball.resizemode("user")
        self.red_ball.shapesize(1.3, 1.3)
        red_start_pose = (CIRCLE_RADIUS, -BOARD_HEIGHT/2 + DIST_TO_BOTTOM)
        self.red_ball.setposition(*red_start_pose)
        self.red_ball.left(90)

        # Draw circle for balls to live on
        circle_drawer = turtle.Turtle()
        circle_drawer.penup()
        circle_drawer.speed(0)
        circle_drawer.color("gray")
        bottom_mid_point = (0,
                            -BOARD_HEIGHT/2 + DIST_TO_BOTTOM - CIRCLE_RADIUS)
        circle_drawer.setposition(bottom_mid_point)
        circle_drawer.pendown()
        circle_drawer.circle(CIRCLE_RADIUS)
        circle_drawer.hideturtle()

    def spin_left(self):
        """
        Spins the balls counterclockwise.
        """

        self.blue_ball.circle(CIRCLE_RADIUS, 1)
        self.red_ball.circle(CIRCLE_RADIUS, 1)

    def spin_right(self):
        """
        Spins the balls clockwise.
        """

        self.blue_ball.circle(CIRCLE_RADIUS, 1)
        self.red_ball.circle(CIRCLE_RADIUS, 1)

    def main_game_loop(self):

        while True:

            self.screen.onkey(self.spin_left, "Left")
            self.screen.onkey(self.spin_right, "Right")
            self.screen.listen()


def main():

    game = DuetGame()
    game.main_game_loop()


if __name__ == "__main__":
    main()
