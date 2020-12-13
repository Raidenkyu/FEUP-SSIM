import sys

from environment import load_environment
from train import train_agent
from test_sonic import test_agent

if len(sys.argv) < 2:
    print('Error: arguments missing.')
    print('Usage: python3 src <auto|cpu>  <integer>.')
    exit()

video_folder = 'logs/videos/'
video_length = 10000000
model_name = "ppo_sonic"
device = sys.argv[1]
timesteps = int(sys.argv[2])
params_key = "sonic"

env = load_environment()
model = train_agent(env, timesteps, device)
test_agent(env, model)
env.close
