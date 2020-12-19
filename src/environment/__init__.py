import os
import retro
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

from environment.sonic_wrapper import SonicEnvWrapper


video_folder = 'logs/videos/'
video_length = 10000000


def load_environment():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    retro.data.Integrations.add_custom_path(
        os.path.join(SCRIPT_DIR, "../../res")
    )

    env = retro.make('SonicTheHedgehog-Genesis',
                     state='act1.state', inttype=retro.data.Integrations.ALL)

    env = SonicEnvWrapper(env)

    env = DummyVecEnv([lambda: env])

    env = VecVideoRecorder(env, video_folder,
                           record_video_trigger=lambda x: x == 0, video_length=video_length,
                           name_prefix="test-sonic")

    return env
