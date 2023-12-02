import chess
import chess.engine
import chess.svg
import json
from time import sleep
import os 

# Specify the path to the Stockfish binary
with open("./keys.json") as f:
    keys = json.load(f)
stockfish_path = keys["stockfish_path"]

# TODO: Legal moves function
# return board.legal_moves.count()

class UW_Chess:
    def __init__(self):
        # Set up the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.board = chess.Board()

    def engin_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        return result.move.uci()

    def player_move(self, move, board):
        try:
            board.push_san(str(move))
            player_move = board.peek().uci()
            return True, player_move
        except chess.InvalidMoveError:
            print("Invalid move, try again")
            sleep(1.5)
            return False

    def score(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(time=0.1))

        # Centipawn Score
        score = info["score"].relative.score()
        if score >0:
            favor = "White"
        else:
            favor = "Black"
        print("score:", score, favor)
        return score

def clear_screen():
    # Clear the console screen.
    os.system('cls' if os.name == 'nt' else 'clear')
