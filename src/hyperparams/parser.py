import yaml

from collections import OrderedDict
from pprint import pprint
from typing import Any, Dict, Tuple
from stable_baselines3.common.utils import constant_fn

from hyperparams.scheduler import linear_schedule


def preprocess_schedules(hyperparams: Dict[str, Any]) -> Dict[str, Any]:
    # Create schedules
    for key in ["learning_rate", "clip_range", "clip_range_vf"]:
        if key not in hyperparams:
            continue
        if isinstance(hyperparams[key], str):
            _schedule, initial_value = hyperparams[key].split("_")
            initial_value = float(initial_value)
            hyperparams[key] = linear_schedule(initial_value)
        elif isinstance(hyperparams[key], (float, int)):
            # Negative value: ignore (ex: for clipping)
            if hyperparams[key] < 0:
                continue
            hyperparams[key] = constant_fn(float(hyperparams[key]))
        else:
            raise ValueError(f"Invalid value for {key}: {hyperparams[key]}")
    return hyperparams


def read_hyperparameters(params_key) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # Load hyperparameters from yaml file
    with open(f"hyperparams/ppo.yml", "r") as f:
        hyperparams_dict = yaml.safe_load(f)
        if params_key in list(hyperparams_dict.keys()):
            hyperparams = hyperparams_dict[params_key]
        else:
            raise ValueError(
                f"Hyperparameters not found for ppo-{params_key}")

    return preprocess_schedules(hyperparams)
