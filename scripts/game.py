import pygame
import numpy as np

from ball import Ball
from obstacle_manager import ObstacleManager


BOARD_HEIGHT = 960
BOARD_WIDTH = 540

BALL_RADIUS = 12   # size of player balls
CIRCLE_RADIUS = 100   # distance between the balls
CIRCLE_WIDTH = 1  # width or grey circle
DIST_TO_BOTTOM = CIRCLE_RADIUS + 15  # dist from ball to bottom of screen
SPIN_STEP = 0.02  # angular step of player balls in radians

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (169, 169, 169)


class DuetGame(object):

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Duet Game")

        self.init_game_board()
        self.init_balls()

    def init_game_board(self):
        """
        Draws the game board.
        """

        pass

    def init_balls(self):
        """
        Initializes the red and blue balls.
        """

        # Create blue ball
        blue_x = BOARD_WIDTH//2 - CIRCLE_RADIUS
        blue_y = BOARD_HEIGHT - DIST_TO_BOTTOM
        blue_theta = np.pi
        self.blue_ball = Ball(blue_x, blue_y, blue_theta,
                              CIRCLE_RADIUS, SPIN_STEP)

        # Create red ball
        red_x = BOARD_WIDTH//2 + CIRCLE_RADIUS
        red_y = BOARD_HEIGHT - DIST_TO_BOTTOM
        red_theta = 0
        self.red_ball = Ball(red_x, red_y, red_theta,
                             CIRCLE_RADIUS, SPIN_STEP)

    def draw_circle(self):
        """
        Draws the gray circle.
        """
        pygame.draw.circle(self.screen, GREY,
                           (BOARD_WIDTH//2, BOARD_HEIGHT - DIST_TO_BOTTOM),
                           CIRCLE_RADIUS, CIRCLE_WIDTH)

    def draw_balls(self):
        """
        Draws the player balls.
        """
        pygame.draw.circle(self.screen, BLUE,
                           self.blue_ball.position(), BALL_RADIUS)
        pygame.draw.circle(self.screen, RED,
                           self.red_ball.position(), BALL_RADIUS)

    def main_game_loop(self):
        """
        Runs the game.
        """

        quit_game = False
        while not quit_game:

            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:

                self.blue_ball.spin_left()
                self.red_ball.spin_left()

            elif keys[pygame.K_RIGHT]:

                self.blue_ball.spin_right()
                self.red_ball.spin_right()

            self.screen.fill(BLACK)
            self.draw_circle()
            self.draw_balls()
            pygame.display.update()

        pygame.quit()


def main():

    game = DuetGame()
    game.main_game_loop()


if __name__ == "__main__":
    main()
