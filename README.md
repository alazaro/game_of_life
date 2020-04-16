# Game Of Life
A PyGame version of Conway's Game of Life

## Installation

Needs Python >= 3.8

Create a virtual environment
```
$ python -m venv .venv
$ pip install -r requirements.txt
```

## Run the game

```
python src/game.py
```

## Configuration

Mostly self explanatory. Just modify the Config object in `src/game.py`

- seed: can be used to always execute the same scenario
- alive_cells_at_start: defines how many cells will be alive after the Big Bang
- rules: Rules of the game. More alternatives can be found at https://catagolue.appspot.com/rules. Supports B/S format. The original GoL is B3S23

## Key bindings

- `R` restarts the game
- `S` start/stop the game
- `=` increase the maximum fps
- `-` decrease the maximum fps
- `ESC` close the game

## TODO

- Add predefined patterns
- Toggle cells with the mouse
- Use numpy/scipy
