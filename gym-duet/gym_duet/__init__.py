from gym.envs.registration import register

register(
    id='duet-v0',
    entry_point='gym_duet.envs:DuetGame',
)
