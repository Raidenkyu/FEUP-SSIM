import os
import sys
import numpy as np
import time
import optuna

from optuna.integration.skopt import SkoptSampler
from optuna.pruners import BasePruner, MedianPruner, SuccessiveHalvingPruner
from optuna.samplers import BaseSampler, RandomSampler, TPESampler

from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import CnnPolicy

from torch import nn as nn
from typing import Any, Dict

from hyperparams.scheduler import linear_schedule
from hyperparams.parser import read_hyperparameters
from environment import load_environment

seed = 0
n_startup_trials = 1000
n_evaluations = 1
n_trials = 1000
n_jobs = 1

sampler_name = "tpe"
pruner_name = "median"

n_timesteps = 0
device = 'auto'


def ppo_params(trial: optuna.Trial) -> Dict[str, Any]:
    batch_size = trial.suggest_categorical(
        "batch_size", [8, 16, 32, 64, 128, 256])
    n_steps = trial.suggest_categorical(
        "n_steps", [8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    gamma = trial.suggest_categorical(
        "gamma", [0.9, 0.95, 0.98, 0.99, 0.995, 0.999, 0.9999])
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1)
    lr_schedule = "constant"
    # lr_schedule = trial.suggest_categorical('lr_schedule', ['linear', 'constant'])
    ent_coef = trial.suggest_loguniform("ent_coef", 0.00000001, 0.1)
    clip_range = trial.suggest_categorical("clip_range", [0.1, 0.2, 0.3, 0.4])
    n_epochs = trial.suggest_categorical("n_epochs", [1, 5, 10, 20])
    gae_lambda = trial.suggest_categorical(
        "gae_lambda", [0.8, 0.9, 0.92, 0.95, 0.98, 0.99, 1.0])
    max_grad_norm = trial.suggest_categorical(
        "max_grad_norm", [0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 5])
    vf_coef = trial.suggest_uniform("vf_coef", 0, 1)
    net_arch = trial.suggest_categorical("net_arch", ["small", "medium"])
    sde_sample_freq = trial.suggest_categorical(
        "sde_sample_freq", [-1, 8, 16, 32, 64, 128, 256])
    ortho_init = False
    # ortho_init = trial.suggest_categorical('ortho_init', [False, True])

    if batch_size > n_steps:
        batch_size = n_steps

    if lr_schedule == "linear":
        learning_rate = linear_schedule(learning_rate)

    net_arch = {
        "small": [dict(pi=[64, 64], vf=[64, 64])],
        "medium": [dict(pi=[256, 256], vf=[256, 256])],
    }[net_arch]


    return {
        "n_steps": n_steps,
        "batch_size": batch_size,
        "gamma": gamma,
        "learning_rate": learning_rate,
        "ent_coef": ent_coef,
        "clip_range": clip_range,
        "n_epochs": n_epochs,
        "gae_lambda": gae_lambda,
        "max_grad_norm": max_grad_norm,
        "vf_coef": vf_coef,
        "sde_sample_freq": sde_sample_freq,
        "policy_kwargs": dict(
            ortho_init=ortho_init,
        ),
    }


def create_sampler(sampler_method: str) -> BaseSampler:
    # n_warmup_steps: Disable pruner until the trial reaches the given number of step.
    if sampler_method == "random":
        sampler = RandomSampler(seed=seed)
    elif sampler_method == "tpe":
        # TODO: try with multivariate=True
        sampler = TPESampler(
            n_startup_trials=n_startup_trials, seed=seed)
    elif sampler_method == "skopt":
        # cf https://scikit-optimize.github.io/#skopt.Optimizer
        # GP: gaussian process
        # Gradient boosted regression: GBRT
        sampler = SkoptSampler(
            skopt_kwargs={"base_estimator": "GP", "acq_func": "gp_hedge"})
    else:
        raise ValueError(f"Unknown sampler: {sampler_method}")
    return sampler


def create_pruner(pruner_method: str) -> BasePruner:
    if pruner_method == "halving":
        pruner = SuccessiveHalvingPruner(
            min_resource=1, reduction_factor=4, min_early_stopping_rate=0)
    elif pruner_method == "median":
        pruner = MedianPruner(
            n_startup_trials=n_startup_trials, n_warmup_steps=n_evaluations // 3)
    elif pruner_method == "none":
        # Do not prune
        pruner = MedianPruner(
            n_startup_trials=n_trials, n_warmup_steps=n_evaluations)
    else:
        raise ValueError(f"Unknown pruner: {pruner_method}")
    return pruner


def optimize_agent(trial):
    """ Train the model and optimise
        Optuna maximises the negative log likelihood, so we
        need to negate the reward here
    """
    hyperparams = ppo_params(trial)
    env = load_environment()

    model = PPO(policy=CnnPolicy, env=env, verbose=1,
                device=device, **hyperparams)
    model.learn(n_timesteps)

    rewards = []
    n_episodes, reward_sum = 0, 0.0

    obs = env.reset()
    while n_episodes < 4:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        reward_sum += reward

        if done:
            rewards.append(reward_sum)
            reward_sum = 0.0
            n_episodes += 1
            obs = env.reset()

    last_reward = np.mean(rewards)
    trial.report(last_reward, n_episodes)

    env.close()
    return last_reward


def hyperparameters_optimization() -> None:
    sampler = create_sampler(sampler_name)
    pruner = create_pruner(pruner_name)

    print(f"Sampler: {sampler_name} - Pruner: {pruner_name}")

    global study_name
    global study_storage

    study_name = "optimizer_study"
    study_storage = "study_storage"

    study = optuna.create_study(
        sampler=sampler,
        pruner=pruner,
        storage=None,
        study_name=study_name,
        load_if_exists=True,
        direction="maximize",
    )

    try:
        study.optimize(optimize_agent, n_trials=n_trials,
                       n_jobs=n_jobs)
    except KeyboardInterrupt:
        pass

    print("Number of finished trials: ", len(study.trials))

    print("Best trial:")
    trial = study.best_trial

    print("Value: ", trial.value)

    print("Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")

    report_name = (
        f"report_sonic_{n_trials}-trials-{n_timesteps}"
        f"-{sampler_name}-{pruner_name}_{int(time.time())}.csv"
    )

    log_path = os.path.join("logs/reports", report_name)

    print(f"Writing report to {log_path}")

    # Write report
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    study.trials_dataframe().to_csv(log_path)


def optimizer(dev, timesteps):
    global device
    global n_timesteps

    device = dev
    n_timesteps = timesteps
    hyperparameters_optimization()


if __name__ == "__main__":
    device = sys.argv[1]
    n_timesteps = int(sys.argv[2])
    hyperparameters_optimization()
