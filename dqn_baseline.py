import gym
import os

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import CnnPolicy  # #, MlpPolicy
from stable_baselines import DQN


def main():

    if not os.path.exists("checkpoints"):
        os.makedirs("checkpoints")
    if not os.path.exists("weights"):
        os.makedirs("weights")
    if not os.path.exists("log"):
        os.makedirs("log")

    env = gym.make('Duet-v0')
    env.man_init(state_rep="pixel", n_repeat_action=20, random_obstacles=True)
    env = DummyVecEnv([lambda: env])

    model = DQN(CnnPolicy,
                env,
                checkpoint_freq=1000,
                checkpoint_path="checkpoints/",
                verbose=1,
                tensorboard_log="log/",
                full_tensorboard_log=False)

    model.learn(total_timesteps=50000000)

    model.save("weights/duet_baseline")

    # Test the trained model
    for i in range(10):
        obs = env.reset()
        acc_reward = 0
        n_steps = 0
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            env.render()
            acc_reward += rewards[0]
            n_steps += 1

        print("Test {} - Steps: {}, Score: {}".format(i + 1, n_steps, acc_reward))


if __name__ == "__main__":
    main()
