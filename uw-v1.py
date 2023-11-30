import chess
import chess.engine
import chess.svg
import json
from time import sleep

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
    return chess.svg.board(board, size=400)

# Game loop

def new_game():

    board = chess.Board()
    game_move = 1
    while not board.is_game_over():
        if game_move % 2 == 0:
            engin_move(board)
        else: 
            move = str(input())
            player_move(move, board)
        game_move += 1
        game_score(board)
        sleep(2)

