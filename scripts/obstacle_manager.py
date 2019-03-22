import pygame
from enum import Enum

BOARD_HEIGHT = 960
BOARD_WIDTH = 540

INNER_LEFT_EDGE = BOARD_WIDTH//2 - 70
INNER_RIGHT_EDGE = BOARD_WIDTH//2 + 70

OBS_HEIGHT = 50
OBS_VEL = 1

# Types of obstacles (min_x, max_x, max_height)
MID_COORDS = (200, 340, 80)


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

        obs_type = ObstacleType.MID  # TODO

        if obs_type == ObstacleType.MID:
            COORDS = MID_COORDS

        spawn_x = COORDS[0]
        spawn_y = 0 - COORDS[2]
        width = COORDS[1] - COORDS[0]
        height = COORDS[2]

        new_obstacle = Obstacle(spawn_x, spawn_y, width, height)
        self.obstacles.append(new_obstacle)

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
    MID = 1


class Obstacle(object):
    """
    An obstacle in the Duet game.
    """

    count = 1

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.top = self.y
        self.bottom = self.y - height
        self.left = self.x
        self.right = self.x + width

        self.id = Obstacle.count
        Obstacle.count += 1

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
        return (self.top - 5 == BOARD_HEIGHT)

    def get_rect(self):
        """
        Returns the obstacle as a pygame Rect.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):

        return "Object #" + str(self.id)
