from .runtime_test import LogExecutionTime
from dotenv import load_dotenv
from time import sleep
import chess, chess.engine
import os
import random

class UW_Chess:
    """
    A class to manage a game of chess with an engine.

    This class creates a chess game environment where a player can interact with a chess engine. It allows
    for engine moves, player moves, evaluation of the board state, and generation of random positions. 
    The engine's difficulty can be adjusted.

    Attributes:
        engine (chess.engine.SimpleEngine): The chess engine for making moves and evaluations.
        board (chess.Board): The current state of the chess game.
    """

    def __init__(self, engine_path, bot_level=10):
        """
        Initializes the UW_Chess class with a specified engine path and bot level.

        Args:
            engine_path (str): Path to the chess engine executable.
            bot_level (int, optional): Skill level of the engine. Defaults to 10.
        """
        # Set up the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.engine.configure({"Skill Level": bot_level})
        self.board = chess.Board()

    @LogExecutionTime
    def engine_move(self, board):
        """
        Calculates and makes a move for the engine.

        Args:
            board (chess.Board): The current state of the chess game.

        Returns:
            str: The move made by the engine in UCI notation.
        """
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        return result.move.uci()

    @LogExecutionTime
    def player_move(self, move, board):
        """
        Processes and executes a move made by the player.

        Args:
            move (str): The move in SAN notation.
            board (chess.Board): The current state of the chess game.

        Returns:
            tuple: A tuple containing a boolean indicating success, and the move in UCI notation or an error message.
        """
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
        """
        Analyzes the current board position and returns the score.

        Args:
            board (chess.Board): The current state of the chess game.

        Returns:
            int: The score of the current board state in centipawns.
        """
        info = self.engine.analyse(board, chess.engine.Limit(time=0.1))

        # Centipawn Score
        score = info["score"].relative.score()
        if score > 0:
            favor = "White"
        else:
            favor = "Black"
        print("score:", score, favor)
        return score

    @LogExecutionTime
    def generate_random_position(self, target_pieces=16):
        """
        Generates a random position on the board.

        Args:
            target_pieces (int, optional): The target number of pieces on the board. Defaults to 16.

        Returns:
            tuple: A tuple containing the current board state and a list of legal moves.
        """
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
