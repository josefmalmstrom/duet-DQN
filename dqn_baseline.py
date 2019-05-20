import gym
import os

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

import tensorflow as tf


def main():

    if not os.path.exists("checkpoints"):
        os.makedirs("checkpoints")
    if not os.path.exists("weights"):
        os.makedirs("weights")
    if not os.path.exists("log"):
        os.makedirs("log")

    with tf.Session() as sess:
        env = gym.make('Duet-v0')
        env.man_init(state_rep="coord", n_repeat_action=20)
        env = DummyVecEnv([lambda: env])

        model = DQN(MlpPolicy(sess=sess, ob_space=env.observation_space, ac_space=env.action_space, n_env=1, n_steps=100, n_batch=100),
                    env,
                    checkpoint_freq=1000,
                    checkpoint_path="checkpoints/",
                    verbose=1,
                    tensorboard_log="log/",
                    full_tensorboard_log=False)

        model.learn(total_timesteps=1000)

        model.save("weights/duet_baseline")

        for i in range(10):
            obs = env.reset()
            acc_reward = 0
            n_steps = 0
            dones = False
            while not dones:
                action, _states = model.predict(obs)
                obs, rewards, dones, info = env.step(action)
                env.render()
                acc_reward += rewards[0]
                n_steps += 1

            print("Test {} - Steps: {}, Score: {}".format(i + 1, n_steps, acc_reward))


if __name__ == "__main__":
    main()
