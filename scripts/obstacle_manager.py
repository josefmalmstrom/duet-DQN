import pygame
import random
from enum import Enum

BOARD_HEIGHT = 960
BOARD_WIDTH = 540

OBS_HEIGHT = 50
OBS_VEL = 2

# Types of obstacles
# (min_left, max_left, min_right, max_right, min_height, max_height)
MID_COORDS = (195, 235, 308, 345, 70, 70)
LEFT_COORDS = (35, 35, 270, 270, 70, 70)
RIGHT_COORDS = (270, 270, 505, 505, 70, 70)


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

        obs_type = self.random_obstacle_type()

        if obs_type == ObstacleType.MID:
            COORDS = MID_COORDS
        elif obs_type == ObstacleType.LEFT:
            COORDS = LEFT_COORDS
        elif obs_type == ObstacleType.RIGHT:
            COORDS = RIGHT_COORDS

        (min_left, max_left, min_right, max_right,
         min_height, max_height) = COORDS

        spawn_x = random.randint(min_left, max_left)
        width = random.randint(min_right, max_right) - spawn_x
        height = random.randint(min_height, max_height)
        spawn_y = 0 - height

        new_obstacle = Obstacle(spawn_x, spawn_y, width, height)
        self.obstacles.append(new_obstacle)

    def random_obstacle_type(self):
        """
        Picks a random obstacle type.
        """
        return random.choice(list(ObstacleType))
        
    def oldest_obstacle(self):
        """
        Returns the oldest obstacle.
        """
        return self.obstacles[0]

    def oldest_out_of_frame(self):
        """
        Checks if the oldest obstacle has gone out of frame.
        """
        return self.obstacles[0].out_of_frame()

    def remove_obstacle(self):
        """
        Removes the oldest obstacle.
        """
        self.obstacles.pop(0)


class ObstacleType(Enum):
    """
    Enum for the different types of obstacles.
    """
    MID = 1
    LEFT = 2
    RIGHT = 3


class Obstacle(object):
    """
    An obstacle in the Duet game.
    """

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.top = self.y
        self.bottom = self.y - height
        self.left = self.x
        self.right = self.x + width

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
        return (self.top - 5 >= BOARD_HEIGHT)

    def get_rect(self):
        """
        Returns the obstacle as a pygame Rect.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
