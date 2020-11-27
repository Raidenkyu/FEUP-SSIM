import os
import retro
from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import CnnPolicy
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

retro.data.Integrations.add_custom_path(
    os.path.join(SCRIPT_DIR, "res")
)

env = retro.make('SonicTheHedgehog-Genesis',
                 state='act1.state', inttype=retro.data.Integrations.ALL)

video_folder = 'logs/videos/'
video_length = 10000000

env = DummyVecEnv([lambda: env])

env = VecVideoRecorder(env, video_folder,
                       record_video_trigger=lambda x: x == 0, video_length=video_length,
                       name_prefix="test-sonic")

model = PPO(policy=CnnPolicy, env=env, verbose=1, device='cpu')
model.learn(total_timesteps=10000)

obs = env.reset()
for _ in range(video_length + 1):
    action, _info = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

env.close()
