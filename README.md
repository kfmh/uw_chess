<h1 align="center">Undr Wolf<br>♖ Voice-Controlled Blindfold Chess ♖</h1>
Undr Wolf is a chess game designed for players seeking to enhance their skills in blindfold chess. This project utilizes ASCII and classic2D for chessboard rendering, text-to-speech and speech-to-text to create a chess game that can be entirely navigated through voice commands. Current testing uses Stockfish chess-engine as chess bot and to evaluate game score.

#### Follow the journey on https://www.youtube.com/@UndrWolf

![Image Alt text](/project_images/2023-12-04_gameplay.png "POC")


## Requierements 
The chess bot is dependet on using a chess endgin with a universal chess interface. 
We recomend Stockfish https://stockfishchess.org/

## Installation Mac/Linux
1. From terminal create a directory
```bash
mkdir <directory_name>
cd <directory_name>
``` 
3. Create and activate an environment
```bash
# Python environment
python3 -m venv <enviroment_neme>
source <enviroment_neme>/bin/activate
```
```bash
# Anaconda environment
conda create -n <enviroment_neme>
conda activate <enviroment_neme>
```
4. Install uw_chess package
```bash
# Pip install package directly from main branch
pip install git+https://github.com/kfmh/uw_chess.git
```

## Usage
Command line parsing.
| Long Flag | Short Flag | Default | Description |
|----------|----------|----------|----------|
| --engine_path           | -p   | None | File path to chess engin |
| --difficulty            | -d   | 10   | Chess bot difficulty range 1-20, default range 1-20. |
| --render_2d             | -r2d | Off  | Boolian flag, turns on 2D board render |
| --coordinate_difficulty | -cd  | 1    | Chess board coordinate visabilty. eazy=1, intermediate=2, hard=3. |
| --random_board          | -rb  | 32   | Generate random board setup, with specified numeber of pieace's in play |


Start program
```bash
# Run program
# example: uw_chess -engine_path path/stockfish/16/bin/stockfish
uw_chess --engine_path <file Path string> --render_2d 
```

Quit program: ctrl + c



## Documentation


