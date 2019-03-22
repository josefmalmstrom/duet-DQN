import pygame
import numpy as np

from ball import Ball
from obstacle_manager import ObstacleManager


BOARD_HEIGHT = 960
BOARD_WIDTH = 540

CIRCLE_RADIUS = 100   # distance between the balls
CIRCLE_WIDTH = 1  # width or grey circle
DIST_TO_BOTTOM = CIRCLE_RADIUS + 15  # dist from ball to bottom of screen
SPIN_STEP = 0.02  # angular step of player balls in radians

NEW_OBS_INTERVAL = 200

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

        self.init_balls()
        self.obstacle_manager = ObstacleManager()
        self.obstacle_manager.new_obstacle()

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
        self.blue_ball.draw(self.screen, BLUE)
        self.red_ball.draw(self.screen, RED)

    def draw_obstacles(self):
        """
        Draws all the current obstacles.
        """
        for obstacle in self.obstacle_manager:
            pygame.draw.rect(self.screen, WHITE, obstacle.get_rect())

    def draw_score(self):
        """
        Draws the score in lower left corner.
        """
        pass

    def move_obstacles(self):
        """
        Moves all obstacles one step.
        """

        for obstacle in self.obstacle_manager:
            obstacle.move()

    def game_loop(self):
        """
        Runs the game.
        """

        quit_game = False
        i = 0
        while not quit_game:

            pygame.time.delay(10)

            # Quit the game if player closed the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

            # Spin the player balls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:

                self.blue_ball.spin_left()
                self.red_ball.spin_left()

            elif keys[pygame.K_RIGHT]:

                self.blue_ball.spin_right()
                self.red_ball.spin_right()

            # Move all obstacles downward
            self.move_obstacles()

            oldest_obstacle = self.obstacle_manager.oldest_obstacle()

            # If an obstacle went out of frame, delete it
            if oldest_obstacle.out_of_frame():
                self.obstacle_manager.remove_obstacle()

            # If it is time, make a new obstacle
            if i % NEW_OBS_INTERVAL == 0:
                self.obstacle_manager.new_obstacle()

            # Draw the game
            self.screen.fill(BLACK)
            self.draw_circle()
            self.draw_balls()
            self.draw_obstacles()
            self.draw_score()
            pygame.display.update()

            # If either ball has collided, quit
            if self.blue_ball.has_collided(oldest_obstacle):
                quit_game = True
            if self.red_ball.has_collided(oldest_obstacle):
                quit_game = True

            i += 1

        pygame.quit()


def main():

    game = DuetGame()
    game.game_loop()


if __name__ == "__main__":
    main()
