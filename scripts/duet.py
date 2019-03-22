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

        pygame.font.init()
        self.score_font = pygame.font.Font("freesansbold.ttf", 20)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 80)
        self.restart_font = pygame.font.Font("freesansbold.ttf", 20)

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

    def draw_score(self, score):
        """
        Draws the score in lower left corner.
        """
        score_surface = self.score_font.render(str(score), False, WHITE)
        self.screen.blit(score_surface, (10, BOARD_HEIGHT-25))

    def move_obstacles(self):
        """
        Moves all obstacles one step.
        """

        for obstacle in self.obstacle_manager:
            obstacle.move()

    def game_over(self):
        """
        Display Game Over message, and give choice to restart or exit.
        """

        game_over_surface = self.game_over_font.render("Game Over", False, RED)
        self.screen.blit(game_over_surface, (50, BOARD_HEIGHT//2))
        restart_surface = self.restart_font.render(
            "Press ESC to quit or RETURN to restart", False, RED)
        self.screen.blit(restart_surface, (80, BOARD_HEIGHT//2 + 80))
        pygame.display.update()

        quit_game = False
        restart = False
        while not (quit_game or restart):
            pygame.time.delay(10)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                quit_game = True
            elif keys[pygame.K_RETURN]:
                restart = True

            # Quit the game if player closed the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

        return quit_game

    def game_loop(self):
        """
        Runs the game.
        """

        quit_game = False
        game_over = False
        i = 1
        score = 0
        while not (game_over or quit_game):

            pygame.time.delay(10)

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

            # If an obstacle went out of frame, delete it
            if self.obstacle_manager.oldest_out_of_frame():
                self.obstacle_manager.remove_obstacle()
                score += 1

            # If it is time, make a new obstacle
            if i % NEW_OBS_INTERVAL == 0:
                self.obstacle_manager.new_obstacle()

            # Draw the game
            self.screen.fill(BLACK)
            self.draw_circle()
            self.draw_balls()
            self.draw_obstacles()
            self.draw_score(score)
            pygame.display.update()

            # If either ball has collided, quit
            oldest_obstacle = self.obstacle_manager.oldest_obstacle()
            if self.blue_ball.has_collided(oldest_obstacle):
                game_over = True
            if self.red_ball.has_collided(oldest_obstacle):
                game_over = True

            # Quit the game if player closed the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

            i += 1
            i = i % 2000

        if game_over:
            quit_game = self.game_over()

        return quit_game


def main():

    quit_game = False
    while not quit_game:
        game = DuetGame()
        quit_game = game.game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()
