# Duet DQN - Applying Deep Q-learning to a popular mobile game

Using [keras-rl](https://github.com/keras-rl/keras-rl) to train DQN agents on [gym-duet](https://github.com/josefmal/gym-duet), an Open-AI gym implementation of the popular mobile game Duet, by Kumobius, available [here](https://www.duetgame.com/).

## Installation

The code is written for Python 3.5. To get started, first install [gym-duet](https://github.com/josefmal/gym-duet).

Then clone this repo:
```
git clone https://github.com/josefmal/duet-game-AI.git
```
And install the requirements
```
pip install -r requirements.txt
```

## Usage
Play the game manually by running:
```
python duet.py
```
Train a DQN agent on a coordinate representation of the state by using the script ```duet_coord_dqn.py```. Display its options by running:
```
python duet_coord_dqn.py -h
```

Train a DQN agent on a pixel representation of the state by using the script ```duet_pixel_dqn.py```. Display its options by running:
```
python duet_pixel_dqn.py -h
```



To be removed:

To run DQN training on gcloud:
```
xvfb-run -s "-screen 0 1600x900x16" -a /home/josefmal/duet-venv/bin/python duet_dqn.py

```
To download files from gcloud:
```
gcloud compute scp --recurse josef.malmstrom@duet-machine-vm:/home/josefmal/duet-game-AI/weights . --zone "us-west1-b"
```

Path to gym environments:
``` 
/home/josefmal/venvs/duet-venv/lib/python3.6/site-packages/gym/envs

```

Follow instructions here to register a custom gym environment:
https://github.com/openai/gym/wiki/Environments
