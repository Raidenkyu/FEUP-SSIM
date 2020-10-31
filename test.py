import retro
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

retro.data.Integrations.add_custom_path(
    os.path.join(SCRIPT_DIR, "res")
)

env = retro.make('SonicTheHedgehog-Genesis',
                 state='act1.state', inttype=retro.data.Integrations.ALL)

env.reset()

done = False

while True:
    env.render()

    action = env.action_space.sample()
    # action = [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]

    ob, rew, done, info = env.step(action)
    print("Action ", action, "Reward ", rew)
