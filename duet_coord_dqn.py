from __future__ import division
import argparse
import os

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

import gym
import gym_duet


INPUT_SHAPE = (12,)
WINDOW_LENGTH = 4


class DuetProcessor(Processor):

    def process_observation(self, observation):
        """
        Processes one observation of the state (1D coord array)
        """

        assert observation.shape == INPUT_SHAPE

        return observation

    def process_state_batch(self, batch):

        return batch


def build_model(nb_actions):
    """
    Builds the DQN model.
    """

    # Next, we build our model. We use the same model that was described by Mnih et al. (2015).
    input_shape = (WINDOW_LENGTH,) + INPUT_SHAPE
    model = Sequential()

    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    # print(model.summary())

    return model


if __name__ == "__main__":

    ANNEAL_STEPS = 1e6
    WARMUP_STEPS = 50e3

    START_EPS = 1.0
    END_EPS = 0.1

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['train', 'test'], default='train')
    parser.add_argument('--weights', type=str, default=None)
    args = parser.parse_args()

    # Get the environment and extract the number of actions.
    env = gym.make('duet-v0')
    env.man_init(state_rep="coord")  # use coordinate state representation instead of pixels
    nb_actions = env.nb_actions()

    # Build the network
    model = build_model(nb_actions)

    # Initialize the memory and state processor
    memory = SequentialMemory(limit=int(1e6), window_length=WINDOW_LENGTH)
    processor = DuetProcessor()

    # If starting from weights, reconfigure paramaters
    if args.weights is not None:
        START_EPS = 0.1
        WARMUP_STEPS = 10e3

    # Choose policy
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=START_EPS, value_min=END_EPS, value_test=.05,
                                  nb_steps=ANNEAL_STEPS)

    # Compile the agent
    dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
                   processor=processor, nb_steps_warmup=WARMUP_STEPS, gamma=.99, target_model_update=10000,
                   train_interval=4, delta_clip=1., batch_size=128)
    dqn.compile(Adam(lr=2.5e-4), metrics=['mae'])

    if args.mode == 'train':

        if args.weights is not None:
            dqn.load_weights(args.weights)

        if not os.path.exists("log"):
            os.makedirs("log")
        if not os.path.exists("weights"):
            os.makedirs("weights")

        weights_filename = 'weights/dqn_duet_weights.h5f'
        checkpoint_weights_filename = 'weights/dqn_duet_weights_{step}.h5f'
        log_filename = 'log/dqn_duet_log.json'

        callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=100e3)]
        callbacks += [FileLogger(log_filename, interval=100)]
        dqn.fit(env, callbacks=callbacks, nb_steps=50e6, log_interval=10000, visualize=False, action_repetition=20)

        # After training is done, we save the final weights one more time.
        dqn.save_weights(weights_filename, overwrite=True)

        # Finally, evaluate our algorithm for 10 episodes.
        dqn.test(env, nb_episodes=10, visualize=True)

    elif args.mode == 'test':
        weights_filename = 'weights/dqn_duet_weights.h5f'
        if args.weights:
            weights_filename = args.weights
        dqn.load_weights(weights_filename)
        dqn.test(env, nb_episodes=10, visualize=True)
