import chess, chess.engine
from dotenv import load_dotenv
import os
from time import sleep
from .runtime_test import LogExecutionTime
import random

load_dotenv()
engine_path = os.getenv("ENGINE_PATH")

class UW_Chess:
    def __init__(self, bot_level=10):
        # Set up the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.engine.configure({"Skill Level": bot_level})
        self.board = chess.Board()

    # @LogExecutionTime
    def engin_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        return result.move.uci()

    # @LogExecutionTime
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

    # @LogExecutionTime
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

    # @LogExecutionTime
    # def generate_random_position(self, target_pieces=32):
    #     move_stack = []
    #     legal_moves = []

    #     # Loop until the number of pieces is equal to target_pieces and move_stack has an even number of moves
    #     while len(self.board.piece_map()) > target_pieces or len(move_stack) % 2 != 0:
    #         legal_moves = list(self.board.legal_moves)
    #         move = random.choice(legal_moves)
    #         move_stack.append(self.board.san(move))  # Append the move in Standard Algebraic Notation (SAN)
    #         self.board.push(move)

    #         # Stop if a checkmate or stalemate occurs
    #         if self.board.is_game_over():
    #             break
        
    #     print(f"move: {len(move_stack)}")
    #     print(len(self.board.piece_map()))

    #     return self.board, legal_moves
    def generate_random_position(self, target_pieces=16):
        move_stack = []
        legal_moves = []

        while len(self.board.piece_map()) > target_pieces or len(move_stack) % 2 != 0:
            legal_moves = list(self.board.legal_moves)
            
            # Check if there are no legal moves or the game is over
            if not legal_moves or self.board.is_game_over():
                break
            
            move = random.choice(legal_moves)
            move_stack.append(self.board.san(move))
            self.board.push(move)
        
        print(f"move: {len(move_stack)}")
        print(len(self.board.piece_map()))

        return self.board, legal_moves
