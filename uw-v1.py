import chess
import chess.engine
import chess.svg
import json
from time import sleep
import os 

with open("./keys.json") as f:
    keys = json.load(f)

# Specify the path to the Stockfish binary
stockfish_path = keys["stockfish_path"]

# Set up the engine
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)



def engin_move(b):
    result = engine.play(b, chess.engine.Limit(time=0.1))
    board = b.push(result.move)
    return board

def player_move(move, b):
    board = b.push_san(str(move))
    return board

def game_score(board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))

    score = info["score"].relative.score()
    if score >0:
        favor = "White"
    else:
        favor = "Black"
    print("score:", score, favor)

def clear_screen():
    # Clear the console screen.
    os.system('cls' if os.name == 'nt' else 'clear')

def main():

    board = chess.Board()
    game_move = 1
    while not board.is_game_over():
        clear_screen()
        game_score(board)
        print("\033[1m" + board + "\033[0m")
        if game_move % 2 == 0:
            engin_move(board)
            sleep(2)
        else: 
            move = str(input("move: "))
            player_move(move, board)
        game_move += 1

if __name__ == "__main__":
    main()