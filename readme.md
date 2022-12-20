# Tic-tac-toe

This project contains a basic game logic for tic-tac-toe with either
human players, random pick computer player or minimax algorithm computer player.

## Setting up the env

So far game can be played in terminal by setting up the project env for it:
```shell
cd tic-tac-toe
python3 -m venv venv/
source venv/bin/activate
python -m pip install --editable library/
```

After the env is ready, go to frontends lib:
```shell
cd frontends
```

## Playing tic-tac-toe

Then the game can be played in 3 modes:

### Human vs human
```shell
python -m console -X human -O human
```

### Human vs computer with random moves
```shell
python -m console -X human -O random
```

### Human vs computer with minimax algorithm
```shell
python -m console -X human -O minimax
```