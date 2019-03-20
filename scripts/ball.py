

class Ball(object):
    """
    Player ball in the Duet game.
    """

    def __init__(self, start_pose):

        self.x = start_pose(0)
        self.y = start_pose(1)

    def spin_left(self):
        pass

    def spin_right(self):
        pass
