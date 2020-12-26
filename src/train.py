import sys
from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import CnnPolicy

from hyperparams.parser import read_hyperparameters
from environment import load_environment

params_key = "sonic"
model_name = "ppo_sonic"


def train_agent(env, timesteps, device):
    try:
        model = PPO.load(path='models/' + model_name, env=env, device=device)
        print("Existent model loaded.")
    except:
        hyperparams = read_hyperparameters(params_key)
        model = PPO(env=env, verbose=1, device=device, **hyperparams)
        print("No saved model found. Creating a new one.")

    model.learn(total_timesteps=timesteps)

    model.save('models/' + model_name)

    return model


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: arguments missing.')
        print('Usage: python3 src <auto|cpu>  <integer>.')
        exit()

    device = sys.argv[1]
    timesteps = int(sys.argv[2])

    env = load_environment(video_name="train")
    model = train_agent(env, timesteps, device)
    env.close()
