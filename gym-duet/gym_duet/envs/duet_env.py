import numpy as np
import gym
from gym import spaces

from gym_duet.envs.duet_backend.ball import Ball
from gym_duet.envs.duet_backend.obstacle_manager import ObstacleManager
from gym_duet.envs.duet_backend.controller import Controller

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


class DuetGame(gym.Env):
    """
    One instance of the duet.py game.
    """

    metadata = {'render.modes': ['human']}

    reward_range = (0, np.inf)
    action_space = spaces.Discrete(3)
    observation_space = spaces.Box(low=0, high=255, shape=(BOARD_WIDTH, BOARD_HEIGHT, 3), dtype=np.uint8)

    def __init__(self, mode="ai", capture=True):

        pygame.init()

        self.mode = mode
        self.capture = capture

        if self.mode == "contr":
            self.controller = Controller()
        elif self.mode == "ai":
            self.action = None

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Duet Game")

        self.score = 0
        self.i = 1

        self._init_balls()
        self.obstacle_manager = ObstacleManager()
        self.obstacle_manager.new_obstacle_set()

        pygame.font.init()
        self.score_font = pygame.font.Font("freesansbold.ttf", 20)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 80)
        self.restart_font = pygame.font.Font("freesansbold.ttf", 20)

    def man_init(self, mode="ai", capture=True):
        """
        For manual initialization after calling gym.make().
        """

        self.mode = mode
        self.capture = capture

        if self.mode == "contr":
            self.controller = Controller()
        elif self.mode == "ai":
            self.action = None

    def reset(self):
        """
        Resets the game.
        """
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Duet Game")

        self.score = 0
        self.i = 1

        self._init_balls()
        self.obstacle_manager = ObstacleManager()
        self.obstacle_manager.new_obstacle_set()

        pygame.font.init()
        self.score_font = pygame.font.Font("freesansbold.ttf", 20)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 80)
        self.restart_font = pygame.font.Font("freesansbold.ttf", 20)

        return self._get_state()

    def step(self, action):
        """
        Performs action (idle, spin clockwise or spin counter-clockwise) in the game
        and returns the resulting (new_state, reward, game_over).
        """

        game_over = False
        reward = 0

        self.action = action

        # Move the player balls
        self._move_balls()

        # Move all obstacles downward
        self._move_obstacles()

        # If an obstacle went out of frame, delete it
        if self.obstacle_manager.oldest_out_of_frame():
            self.obstacle_manager.remove_obstacle_set()
            self.score += 1
            reward = 1

        # If it is time, make a new obstacle
        if self.i % NEW_OBS_INTERVAL == 0:
            self.obstacle_manager.new_obstacle_set()

        # Draw the game
        self.screen.fill(BLACK)
        self._draw_circle()
        self._draw_balls()
        self._draw_obstacles()
        self._draw_score()

        # If either ball has collided, quit
        oldest_obstacle_set = self.obstacle_manager.oldest_obstacle_set()
        for obstacle in oldest_obstacle_set:
            if self.blue_ball.collided_with(obstacle):
                game_over = True
                reward = -100
            if self.red_ball.collided_with(obstacle):
                game_over = True
                reward = -100

        self.i += 1
        self.i = self.i % NEW_OBS_INTERVAL

        state = None
        if self.capture:
            state = self._get_state()

        self._get_state()

        return (state, reward, game_over, {})

    def render(self, mode='human', close=False):
        pygame.display.update()

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

            _, _, game_over, _ = self.step(action=None)

            self.render()

            # Quit the game if player closed the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break

        if game_over:
            quit_game = self._game_over()

        return quit_game

    def state_size(self):
        """
        Returns the shape of the state representation.
        """
        return BOARD_WIDTH*BOARD_HEIGHT

    def nb_actions(self):
        """
        Returns the number of possible actions.
        """
        return 3

    def _get_state(self):
        """
        Returns the current screen as a numpy pixel array.
        """
        screen_pixels = pygame.PixelArray(self.screen)
        state = np.asarray(screen_pixels).T
        screen_pixels.close()

        return state

    def _init_balls(self):
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

    def _move_balls(self):
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

    def _draw_circle(self):
        """
        Draws the gray circle.
        """
        pygame.draw.circle(self.screen, GREY,
                           (BOARD_WIDTH//2, BOARD_HEIGHT - DIST_TO_BOTTOM),
                           CIRCLE_RADIUS, CIRCLE_WIDTH)

    def _draw_balls(self):
        """
        Draws the player balls.
        """
        self.blue_ball.draw(self.screen, BLUE)
        self.red_ball.draw(self.screen, RED)

    def _draw_obstacles(self):
        """
        Draws all the current obstacles.
        """
        for obstacle_set in self.obstacle_manager:
            for obstacle in obstacle_set:
                pygame.draw.rect(self.screen, WHITE, obstacle.get_rect())

    def _draw_score(self):
        """
        Draws the score in lower left corner.
        """
        score_surface = self.score_font.render(str(self.score), False, WHITE)
        self.screen.blit(score_surface, (10, BOARD_HEIGHT-25))

    def _move_obstacles(self):
        """
        Moves all obstacles one step.
        """

        for obstacle_set in self.obstacle_manager:
            for obstacle in obstacle_set:
                obstacle.move()

    def _game_over(self):
        """
        Display Game Over message, and give choice to restart or exit.
        """

        game_over_surface = self.game_over_font.render("Game Over", False, RED)
        self.screen.blit(game_over_surface, (50, BOARD_HEIGHT//2))
        restart_surface = self.restart_font.render("Press ESC to quit or RETURN to restart", False, RED)
        self.screen.blit(restart_surface, (80, BOARD_HEIGHT//2 + 80))
        self.render()

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
