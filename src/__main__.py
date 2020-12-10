import os
import sys
import retro
from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import CnnPolicy
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

if len(sys.argv) < 2:
    print('Error: arguments missing.')
    print('Usage: python3 src <auto|cpu>  <integer>.')
    exit()

video_folder = 'logs/videos/'
video_length = 10000000
model_name = "ppo_sonic"
device = sys.argv[1]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

retro.data.Integrations.add_custom_path(
    os.path.join(SCRIPT_DIR, "../res")
)

env = retro.make('SonicTheHedgehog-Genesis',
                 state='act1.state', inttype=retro.data.Integrations.ALL)

env = DummyVecEnv([lambda: env])

env = VecVideoRecorder(env, video_folder,
                       record_video_trigger=lambda x: x == 0, video_length=video_length,
                       name_prefix="test-sonic")

try:
    model = PPO.load(path='models/' + model_name, env=env, device=device)
    print("Existent model loaded.")
except:
    model = PPO(policy=CnnPolicy, env=env, verbose=1, device=device)
    print("No saved model found. Creating a new one.")

model.learn(total_timesteps=int(sys.argv[2]))

model.save('models/' + model_name)

obs = env.reset()
for _ in range(video_length + 1):
    action, _info = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

env.close()
