import pygame

BOARD_WIDTH = 960
BOARD_HEIGHT = 540

OUTER_LEFT_EDGE = 10
INNER_LEFT_EDGE = 50

OUTER_RIGHT_EDGE = BOARD_WIDTH - 10
INNER_RIGHT_EDGE = BOARD_WIDTH - 50

OBSTACLE_TYPES = {1: (OUTER_LEFT_EDGE, 1)}

class ObstacleManager(object):
    """
    Generates and manages obstacles for the Duet game.
    """

    def __init__(self):
        pass


class Obstacle(object):
    """
    An obstacle in the Duet game.
    """

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)
