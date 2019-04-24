import numpy as np

import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class ScreenRecorder(object):
    """
    Records the screen of the Duet game as a sequence of pixel arrays.
    """

    def __init__(self):

        self.screens = []

    def record(self, screen):
        """
        Records the current state of the screen as a pixel array.
        """
        screen_pixels = pygame.PixelArray(screen)
        self.screens.append(np.asarray(screen_pixels))
        screen_pixels.close()

    def save_recording(self):
        """
        Saves the recording to disk.
        """
        pass
