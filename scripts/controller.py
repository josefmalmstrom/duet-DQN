from enum import Enum

ALIGN_TOL = 2
NEW_ACTION_TIME = 10


class Action(Enum):
    """
    Enum for the different controller actions.
    """
    IDLE = 1
    SPIN_LEFT = 2
    SPIN_RIGHT = 3
    ALIGN_VERTICAL = 4
    ALIGN_HORISONTAL = 5


class Controller(object):
    """
    A simplistic controller for the duet.py game.
    """
    def __init__(self):

        self.action = Action.IDLE
        self.count = 0

    def get_controll(self, obstacle_sets, red_pos, blue_pos):

        self.count += 1
        if self.count == NEW_ACTION_TIME:
            self.determine_action(obstacle_sets, red_pos, blue_pos)
            self.count = 0

        return self.calculate_controlls(red_pos, blue_pos)

    def find_closest_obstacle(self, obstacle_sets, red_pos, blue_pos):
        """
        Determines the obstacle to be avoided.
        """

        red_x, red_y = red_pos
        blue_x, blue_y = blue_pos

        closest_found = False
        i = 0
        while not closest_found:
            closest_obstacle_set = obstacle_sets[i]
            for obstacle in closest_obstacle_set:
                if obstacle.get_top() < max(red_y, blue_y):
                    closest_found = True
                    break

            if i == len(closest_obstacle_set) - 1:
                closest_found = True

            i += 1

        return closest_obstacle_set

    def determine_action(self, obstacle_sets, red_pos, blue_pos):
        """
        Determines the next action (align vertical, align horiontal, spin left
        or spin right) based on the set of obstacle sets on the board.
        """
        red_x, red_y = red_pos
        blue_x, blue_y = blue_pos

        closest_obstacle_set = self.find_closest_obstacle(obstacle_sets, red_pos, blue_pos)

        red_collision_course = False
        blue_collision_course = False
        for obstacle in closest_obstacle_set:

            left, right = obstacle.x_span()

            if red_x in range(left, right+1):
                red_collision_course = True

            if blue_x in range(left, right+1):
                blue_collision_course = True

        if red_collision_course and blue_collision_course:

            # Probably a mid-obstacle
            if abs(red_x - blue_x) < abs(red_y - blue_y):
                self.action = Action.ALIGN_HORISONTAL
                return

            # Probably a double-obstacle
            self.action = Action.ALIGN_VERTICAL
            return

        if red_collision_course:
            if red_x < blue_x:
                self.action = Action.SPIN_LEFT
                return
            self.action = Action.SPIN_RIGHT
            return

        if blue_collision_course:
            if blue_x < red_x:
                self.action = Action.SPIN_LEFT
                return
            self.action = Action.SPIN_RIGHT
            return

    def calculate_controlls(self, red_pos, blue_pos):
        """
        Calculates appropriate controll output based on current desired action.
        Spin left = -1
        Stay idle = 0
        Spin right = 1
        """
        if self.action == Action.IDLE:
            return 0
        if self.action == Action.SPIN_LEFT:
            return -1
        if self.action == Action.SPIN_RIGHT:
            return 1

        red_x, red_y = red_pos
        blue_x, blue_y = blue_pos
        if self.action == Action.ALIGN_HORISONTAL:

            if abs(red_y - blue_y) <= ALIGN_TOL:
                self.action = Action.IDLE
                return 0

            # Red is to the left and ...
            if red_x < blue_x:
                if red_y > blue_y:
                    return 1  # below
                return -1  # above

            # Blue is to the left and ...
            if blue_y > red_y:
                return 1  # below
            return -1  # above

        if self.action == Action.ALIGN_VERTICAL:

            if abs(red_x - blue_x) <= ALIGN_TOL:
                self.action = Action.IDLE
                return 0

            # Red is above and ...
            if red_y < blue_y:
                if red_x < blue_x:
                    return 1  # left
                return -1  # right

            # Blue is above and ...
            if blue_x < red_x:
                return 1  # left
            return -1  # right
