import os
import retro
from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import CnnPolicy
from stable_baselines3.common.vec_env import DummyVecEnv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

retro.data.Integrations.add_custom_path(
    os.path.join(SCRIPT_DIR, "res")
)

env = retro.make('SonicTheHedgehog-Genesis',
                 state='act1.state', inttype=retro.data.Integrations.ALL)

env = DummyVecEnv([lambda: env])

model = PPO(policy=CnnPolicy, env=env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
while True:
    action, _info = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
