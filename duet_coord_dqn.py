from __future__ import division
import argparse
import os

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
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
        return observation.astype('uint8')  # saves storage in experience memory

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
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    # print(model.summary())

    return model


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['train', 'test'], default='train')
    parser.add_argument('--weights', type=str, default=None)
    args = parser.parse_args()

    # Get the environment and extract the number of actions.
    env = gym.make('duet-v0')
    nb_actions = env.nb_actions()

    model = build_model(nb_actions)

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=500000, window_length=WINDOW_LENGTH)
    processor = DuetProcessor()

    # Select a policy. We use eps-greedy action selection, which means that a random action is selected
    # with probability eps. We anneal eps from 1.0 to 0.1 over the course of 1M steps. This is done so that
    # the agent initially explores the environment (high eps) and then gradually sticks to what it knows
    # (low eps). We also set a dedicated eps value that is used during testing. Note that we set it to 0.05
    # so that the agent still performs some random actions. This ensures that the agent cannot get stuck.
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                                  nb_steps=10000)

    dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
                   processor=processor, nb_steps_warmup=50000, gamma=.99, target_model_update=10000,
                   train_interval=4, delta_clip=1.)
    dqn.compile(Adam(lr=.00025), metrics=['mae'])

    if args.mode == 'train':
        # Okay, now it's time to learn something! We capture the interrupt exception so that training
        # can be prematurely aborted. Notice that now you can use the built-in Keras callbacks!

        if not os.path.exists("log"):
            os.makedirs("log")
        if not os.path.exists("weights"):
            os.makedirs("weights")

        weights_filename = 'weights/dqn_duet_weights.h5f'
        checkpoint_weights_filename = 'weights/dqn_duet_weights_{step}.h5f'
        log_filename = 'log/dqn_duet_log.json'

        callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=250000)]
        callbacks += [FileLogger(log_filename, interval=100)]
        dqn.fit(env, callbacks=callbacks, nb_steps=1750000, log_interval=10000, visualize=False, action_repetition=5)

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
