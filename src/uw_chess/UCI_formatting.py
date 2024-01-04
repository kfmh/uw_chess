# ============================================================================
# uci_formatting.py
# logging the time it takes to run functions
# ============================================================================

from runtime_test import LogExecutionTime
import re

class Formatting:
    """
    A class for handling and validating chess move formatting.

    This class provides functionality to check the format of chess moves and convert them to 
    Universal Chess Interface (UCI) format. It supports basic validation of moves and handles 
    move promotion.

    Attributes:
        board_x (list): List of letters representing the x-axis on a chessboard.
        board_y (list): List of numbers representing the y-axis on a chessboard.
        promotion (dict): Dictionary mapping chess piece names to their respective UCI notation.
    """

    def __init__(self):
        self.board_x = ['a','b','c','d','e','f','g','h']
        self.board_y = ['1','2','3','4','5','6','7','8']
        self.promotion  = {"king": "k", "queen": "q", "knight": "n", "bishop": "b", "pawn": "p"}

    @LogExecutionTime
    def check_format(self, string):
        """
        Validates the format of a chess move string.

        This method uses a regular expression to ensure the move string follows the standard 
        format: a letter (a-h) followed by a digit (1-8), repeated twice.

        Args:
            string (str): The chess move string to validate.

        Returns:
            bool: True if the string matches the required format, False otherwise.
        """
        # Pattern: letter (a-h), digit (1-8), letter (a-h), digit (1-8)
        pattern = r'^[a-h][1-8][a-h][1-8]$'
        return bool(re.match(pattern, string))

    @LogExecutionTime
    def uci_str(self, words:list):
        """
        Takes a string and splits on "," "." or " ".
        Then converts list of words into UCI-string formatted chess move.

        This method processes a list of words, attempting to construct a UCI-compliant chess move.
        It accounts for move promotions and validates the final move format.

        Args:
            words (list): A list of words representing the move and possibly a promotion.

        Returns:
            str or False: The UCI formatted move if successful, False otherwise.
        """
        try:
            word_list = re.split('[,. ]', words)
            uci_move = ''
            for i in word_list:
                if len(uci_move) == 4 and i in self.promotion:
                    uci_move += self.promotion[i]
                for l in list(i):
                    if l in self.board_y:
                        uci_move += i
            print(f"uci formatting: {uci_move}")
            if self.check_format(uci_move.lower()):
                return uci_move.lower()
            else: 
                return False
        except KeyError: 
            return False
