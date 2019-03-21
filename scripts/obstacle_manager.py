import pygame
from enum import Enum

BOARD_HEIGHT = 960
BOARD_WIDTH = 540

INNER_LEFT_EDGE = BOARD_WIDTH//2 - 70
INNER_RIGHT_EDGE = BOARD_WIDTH//2 + 70

OBS_HEIGHT = 50

OBS_VEL = 1


class ObstacleManager(object):
    """
    Generates and manages obstacles for the Duet game.
    """

    def __init__(self):

        self.obstacles = []

    def __iter__(self):

        return iter(self.obstacles)

    def new_obstacle(self):
        """
        Generates a new obstacle.
        """

        spawn_x = INNER_LEFT_EDGE
        spawn_y = 0 - OBS_HEIGHT
        width = INNER_RIGHT_EDGE - INNER_LEFT_EDGE
        height = OBS_HEIGHT
        obs_type = Type.MID

        new_obstacle = Obstacle(spawn_x, spawn_y, width, height, obs_type)
        self.obstacles.append(new_obstacle)

    def oldest_obstacle(self):
        """
        Returns the oldest obstacle.
        """
        return self.obstacles[0]

    def remove_obstacle(self):
        """
        Removes the oldest obstacle.
        """
        self.obstacles.pop(0)


class Type(Enum):
    MID = 1


class Obstacle(object):
    """
    An obstacle in the Duet game.
    """

    def __init__(self, x, y, width, height, obs_type):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.top = self.y
        self.bottom = self.y - height
        self.left = self.x
        self.right = self.x + width

        self.obs_type = obs_type

    def move(self):
        """
        Moves the obstacle down, towards the player.
        """

        self.y += OBS_VEL
        self.top += OBS_VEL
        self.bottom += OBS_VEL

    def out_of_frame(self):
        """
        Checks if the obstacle has left the game board.
        """
        return (self.top >= BOARD_HEIGHT)

    def get_rect(self):
        """
        Returns the obstacle as a pygame Rect.
        """

        return pygame.Rect(self.x, self.y, self.width, self.height)
