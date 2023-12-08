# TODO: Legal moves function
# return board.legal_moves.count()

import chess, chess.engine
import re
import os
from time import sleep
from dotenv import load_dotenv
import os

from runtime_test import LogExecutionTime

load_dotenv()

engine_path = os.getenv("engine_path")

class UW_Chess:
    def __init__(self, bot_level=10):
        # Set up the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.engine.configure({"Skill Level": bot_level})
        self.board = chess.Board()

    @LogExecutionTime
    def engin_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        return result.move.uci()

    @LogExecutionTime
    def player_move(self, move, board):
        try:
            board.push_san(str(move))
            player_move = board.peek().uci()
            return True, player_move
        except chess.InvalidMoveError:
            sleep(1.5)
            return False, "Not a valid move, try again"
        except chess.IllegalMoveError:
            sleep(1.5)
            return False, "Not a legal move, try again"

    @LogExecutionTime
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


        