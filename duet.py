import argparse
import os

import gym
# import gym_duet

import contextlib
with contextlib.redirect_stdout(None):
    import pygame


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, choices=["man", "contr", "ai"],
                        default="man", help="mode of operation for the game")
    args = parser.parse_args()

    quit_game = False
    while not quit_game:
        os.system("clear")
        game = gym.make("Duet-v0")
        game.man_init(mode=args.mode, capture=False, n_repeat_action=1)
        quit_game = game.game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()
