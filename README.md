# FEUP-SSIM
The source code of a project, developed in the SSIM course, to build, test, study and improve a reinforcement learning agent to complete the first level of Sonic The Hedgehog. This experimental setup uses stable baselines 3 implementation of the algorithm PPO and Gym Retro to generate the environment that emulates the original SEGA Mega Drive game under-the-hood.

DISCLAIMER: It is recommend to run this project in a Linux-based operating system for better stability.

## Requirements
* `python 3.8`
* `pip 20.3`

## Install dependencies
Run in the root of the repository:
```shell
pip install -r requirements.txt
```

## Run the complete experimental setup
To run the complete pipeline, with both train test. In the first argument is specified if the simulation will run only with CPU, with CUDA (both CPU and GPU, Nvidia specific) or auto (to run with CUDA if detected, otherwise CPU). The second argument is the number of timesteps. If no agent is found in the directory `models/` a new onde will be created, otherwise the existent model will be loaded a resume training.

Run in the root of the repository:
```shell
python src <auto|cpu|cuda> <number>
```

Example:
```shell
python src auto 200000
```

## Run only the train
To run the train but not the test. In the first argument is specified if the simulation will run only with CPU, with CUDA (both CPU and GPU, Nvidia specific) or auto (to run with CUDA if detected, otherwise CPU). The second argument is the number of timesteps. If no agent is found in the directory `models/` a new onde will be created, otherwise the existent model will be loaded a resume training.

Run in the root of the repository:
```shell
python src/train.py <auto|cpu|cuda> <number>
```

Example:
```shell
python src/train.py auto 200000
```

## Run only the test
To run a test of a previously trained agent, so it must exist in the directory `models/`. In the first argument is specified if the simulation will run only with CPU, with CUDA (both CPU and GPU, Nvidia specific) or auto (to run with CUDA if detected, otherwise CPU).

Run in the root of the repository:
```shell
python src/test_sonic.py <auto|cpu|cuda>
```

Example:
```shell
python src/test_sonic.py auto
```

## Run the optimizer
To run the optimizer. In the first argument is specified if the simulation will run only with CPU, with CUDA (both CPU and GPU, Nvidia specific) or auto (to run with CUDA if detected, otherwise CPU). The second argument is the number of timesteps. To stop, press "CTRL+C" (this changes for other operating systems than Linux) and a report with the hyperparameters and their values will be presented in a csv file located under `logs/reports/`.

Run in the root of the repository:
```shell
python src/optimizer.py <auto|cpu|cuda> <number>
```

Example:
```shell
python src/optimizer.py auto 200000
```

## Authors
* Fernando Jorge Alves
* João Carlos Maduro