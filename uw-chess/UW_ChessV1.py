# TODO: Legal moves function
# return board.legal_moves.count()

import chess, chess.engine
import re
import os
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

engine_path = os.getenv("engine_path")

class UW_Chess:
    def __init__(self):
        # Set up the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
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
            return False, "None"
        except chess.IllegalMoveError:
            error = "Not legal move, try again" 
            print(error)
            sleep(1.5)
            return False, "Not legal move, try again"


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


class STT_move:
    def __init__(self):
        self.board_x = ['a','b','c','d','e','f','g','h']
        self.board_y = ['1','2','3','4','5','6','7','8']

    def uci_str(self, words:list):
        try:
            word_list = re.split('[,. ]', words["text"])
            uci_move = ''
            for i in word_list:
                for l in list(i):
                    if l in self.board_y:
                        uci_move += i
            return uci_move.lower()
        except KeyError: 
            return 'try again'