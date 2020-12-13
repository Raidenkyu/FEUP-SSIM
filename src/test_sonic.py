import sys
from environment import video_length
from stable_baselines3 import PPO

from environment import load_environment
from train import model_name


def load_agent(env, device):
    try:
        model = PPO.load(path='models/' + model_name, env=env, device=device)
        print("Existent model loaded.")
    except:
        print("No saved model found. Train one first.")

    return model


def test_agent(env, model):
    obs = env.reset()
    for _ in range(video_length + 1):
        action, _info = model.predict(obs)
        obs, _rewards, _dones, _info = env.step(action)
        env.render()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print('Error: argument missing.')
        print('Usage: python3 src <auto|cpu>.')
        exit()

    device = sys.argv[1]

    env = load_environment()
    model = load_agent(env, device)
    test_agent(env, model)
    env.close()
