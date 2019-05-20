import gym

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


env = gym.make('Duet-v0')
env = DummyVecEnv([lambda: env])

model = DQN(MlpPolicy, env, verbose=1, tensorboard_log="log/", full_tensorboard_log=True)
model.learn(total_timesteps=25000)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
