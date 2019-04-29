# Duet - A popular mobile game implemented in Python

This is a mockup version of the game Duet by Kumobius, available [here](https://www.duetgame.com/).

## Getting started

The game is written for Python 3.5. Install the game by cloning this repository
```
git clone https://github.com/josefmal/duet-game-AI.git
```
Install the requirements
```
pip install -r requirements.txt
```
Install the gym-duet module
```
cd gym-duet
pip install -e .
```
Start the game by running
```
python duet.py
```

To run DQN training on gcloud:
```
xvfb-run -s "-screen 0 1600x900x16" -a home/josefmal/duet-venv/bin/python duet_dqn.py

```
