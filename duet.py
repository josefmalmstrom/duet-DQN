import argparse
import numpy as np
import os

from duet_backend.ball import Ball
from duet_backend.obstacle_manager import ObstacleManager
from duet_backend.controller import Controller

import contextlib
with contextlib.redirect_stdout(None):
    import pygame


BOARD_HEIGHT = 960
BOARD_WIDTH = 540

CIRCLE_RADIUS = 100   # distance from either ball to center
CIRCLE_WIDTH = 1  # width of grey circle
DIST_TO_BOTTOM = CIRCLE_RADIUS + 15  # dist from ball to bottom of screen
SPIN_STEP = 0.0224  # angular step of player balls in radians

NEW_OBS_INTERVAL = 140

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (169, 169, 169)


class DuetGame(object):
    """
    One instance of the duet.py game.
    """

    def __init__(self, mode="ai", capture=True):

        pygame.init()

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Duet Game")

        self.init_balls()
        self.obstacle_manager = ObstacleManager()
        self.obstacle_manager.new_obstacle_set()

        pygame.font.init()
        self.score_font = pygame.font.Font("freesansbold.ttf", 20)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 80)
        self.restart_font = pygame.font.Font("freesansbold.ttf", 20)

        self.score = 0
        self.i = 1

        self.mode = mode
        self.capture = capture

        if self.mode == "contr":
            self.controller = Controller()
        elif self.mode == "ai":
            self.action = None

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

    def move_balls(self):
        """
        Applies controlls to the player balls.
        """

        if self.mode == "man":

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:

                self.blue_ball.spin_left()
                self.red_ball.spin_left()

            elif keys[pygame.K_RIGHT]:

                self.blue_ball.spin_right()
                self.red_ball.spin_right()

        elif self.mode == "contr":

            controll = self.controller.get_controll(self.obstacle_manager.get_obstacles(),
                                                    self.red_ball.position(), self.blue_ball.position())
            if controll == -1:
                self.blue_ball.spin_left()
                self.red_ball.spin_left()
            elif controll == 1:
                self.blue_ball.spin_right()
                self.red_ball.spin_right()

        elif self.mode == "ai":

            if self.action == 1:
                self.blue_ball.spin_left()
                self.red_ball.spin_left()
            elif self.action == 2:
                self.blue_ball.spin_right()
                self.red_ball.spin_right()

        else:
            raise ValueError("Invalid game mode '{}'".format(self.mode))

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
        for obstacle_set in self.obstacle_manager:
            for obstacle in obstacle_set:
                pygame.draw.rect(self.screen, WHITE, obstacle.get_rect())

    def draw_score(self):
        """
        Draws the score in lower left corner.
        """
        score_surface = self.score_font.render(str(self.score), False, WHITE)
        self.screen.blit(score_surface, (10, BOARD_HEIGHT-25))

    def move_obstacles(self):
        """
        Moves all obstacles one step.
        """

        for obstacle_set in self.obstacle_manager:
            for obstacle in obstacle_set:
                obstacle.move()

    def game_over(self):
        """
        Display Game Over message, and give choice to restart or exit.
        """

        game_over_surface = self.game_over_font.render("Game Over", False, RED)
        self.screen.blit(game_over_surface, (50, BOARD_HEIGHT//2))
        restart_surface = self.restart_font.render("Press ESC to quit or RETURN to restart", False, RED)
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

    def state_size(self):
        """
        Returns the shape of the state representation.
        """
        return BOARD_WIDTH*BOARD_HEIGHT

    def action_size(self):
        """
        Returns the shape of the action representation.
        """
        return 3

    def get_screen_state(self):
        """
        Returns the current screen as a numpy pixel array.
        """
        screen_pixels = pygame.PixelArray(self.screen)
        new_state = np.asarray(screen_pixels).flatten()
        screen_pixels.close()

        return new_state

    def game_loop(self):
        """
        Runs the game.
        """

        quit_game = False
        game_over = False
        self.i = 1
        self.score = 0
        while not (game_over or quit_game):

            pygame.time.delay(10)

            _, _, game_over = self.step(action=None)

            # Quit the game if player closed the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

        if game_over:
            quit_game = self.game_over()

        return quit_game

    def step(self, action):
        """
        Performs action (idle, spin clockwise or spin counter-clockwise) in the game
        and returns the resulting (new_state, reward, game_over).
        """

        game_over = False

        self.action = action

        # Move the player balls
        self.move_balls()

        # Move all obstacles downward
        self.move_obstacles()

        # If an obstacle went out of frame, delete it
        if self.obstacle_manager.oldest_out_of_frame():
            self.obstacle_manager.remove_obstacle_set()
            self.score += 1

        # If it is time, make a new obstacle
        if self.i % NEW_OBS_INTERVAL == 0:
            self.obstacle_manager.new_obstacle_set()

        # Draw the game
        self.screen.fill(BLACK)
        self.draw_circle()
        self.draw_balls()
        self.draw_obstacles()
        self.draw_score()
        pygame.display.update()

        # If either ball has collided, quit
        oldest_obstacle_set = self.obstacle_manager.oldest_obstacle_set()
        for obstacle in oldest_obstacle_set:
            if self.blue_ball.collided_with(obstacle):
                game_over = True
            if self.red_ball.collided_with(obstacle):
                game_over = True

        self.i += 1
        self.i = self.i % NEW_OBS_INTERVAL

        new_state = None
        if self.capture:
            new_state = self.get_screen_state()

        reward = self.score if game_over else 0

        return (new_state, reward, game_over)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, choices=["man", "contr", "ai"],
                        default="man", help="mode of operation for the game")
    args = parser.parse_args()

    quit_game = False
    while not quit_game:
        os.system("clear")
        game = DuetGame(args.mode, False)
        quit_game = game.game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()
