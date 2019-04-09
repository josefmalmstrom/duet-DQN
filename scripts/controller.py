from enum import Enum

BOARD_WIDTH = 540
CIRCLE_RADIUS = 100   # distance from either ball to center

ALIGN_TOL = 2


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
        self.curr_obstacle_set = None
        self.count = 0

    def get_controll(self, obstacle_sets, red_pos, blue_pos):
        """
        Returns the calculated controll input.
        """

        self.red_x, self.red_y = red_pos
        self.blue_x, self.blue_y = blue_pos

        if self.curr_obstacle_set is None:
            self.curr_obstacle_set = obstacle_sets[0]

        if self.curr_obstacle_avoided():
            self.curr_obstacle_set = obstacle_sets[1]

        self.determine_action()

        return self.calculate_controlls()

    def curr_obstacle_avoided(self):
        """
        Determines if the current obstacle has been avoided.
        """

        for obstacle in self.curr_obstacle_set:
            if max(self.red_y, self.blue_y) > obstacle.get_top():
                return False

        return True

    def determine_action(self):
        """
        Determines the next action (align vertical, align horiontal, spin left
        or spin right) based on the set of obstacle sets on the board.
        """

        # Must be a double-obstacle
        if len(self.curr_obstacle_set) == 2:
            self.action = Action.ALIGN_VERTICAL
            return

        red_collision_course = False
        blue_collision_course = False
        for obstacle in self.curr_obstacle_set:

            left, right = obstacle.x_span()

            if self.red_x in range(left, right+1):
                red_collision_course = True

            if self.blue_x in range(left, right+1):
                blue_collision_course = True

        if red_collision_course and blue_collision_course:

            obstacle = self.curr_obstacle_set[0]
            left, right = obstacle.x_span()

            # Must be a right-obstacle
            if right >= BOARD_WIDTH//2 + CIRCLE_RADIUS:
                self.action = Action.SPIN_RIGHT
                return

            # Must be a left-obstacle
            if left <= BOARD_WIDTH//2 - CIRCLE_RADIUS:
                self.action == Action.SPIN_LEFT
                return

            # Must be a mid-obstacle
            self.action = Action.ALIGN_HORISONTAL
            return

        if red_collision_course:

            if self.action == Action.ALIGN_VERTICAL:
                self.action = Action.SPIN_LEFT
                return

            if self.red_y - obstacle.get_bottom() > 2.5*CIRCLE_RADIUS:
                self.action = Action.IDLE
                return

            if self.red_x < self.blue_x:
                self.action = Action.SPIN_LEFT
                return
            self.action = Action.SPIN_RIGHT
            return

        if blue_collision_course:

            if self.action == Action.ALIGN_VERTICAL:
                self.action = Action.SPIN_LEFT
                return

            if self.blue_y - obstacle.get_bottom() > 2.5*CIRCLE_RADIUS:
                self.action = Action.IDLE
                return

            if self.blue_x < self.red_x:
                self.action = Action.SPIN_LEFT
                return
            self.action = Action.SPIN_RIGHT
            return

        self.action = Action.IDLE
        return

    def calculate_controlls(self):
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

        if self.action == Action.ALIGN_HORISONTAL:

            if abs(self.red_y - self.blue_y) <= ALIGN_TOL:
                self.action = Action.IDLE
                return 0

            # Red is to the left and ...
            if self.red_x < self.blue_x:
                if self.red_y > self.blue_y:
                    return 1  # below
                return -1  # above

            # Blue is to the left and ...
            if self.blue_y > self.red_y:
                return 1  # below
            return -1  # above

        if self.action == Action.ALIGN_VERTICAL:

            if abs(self.red_x - self.blue_x) <= ALIGN_TOL:
                self.action = Action.IDLE
                return 0

            # Red is above and ...
            if self.red_y < self.blue_y:
                if self.red_x < self.blue_x:
                    return 1  # left
                return -1  # right

            # Blue is above and ...
            if self.blue_x < self.red_x:
                return 1  # left
            return -1  # right
