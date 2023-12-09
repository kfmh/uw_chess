import re
from runtime_test import LogExecutionTime

class formatting:
    def __init__(self):
        self.board_x = ['a','b','c','d','e','f','g','h']
        self.board_y = ['1','2','3','4','5','6','7','8']
        self.promotion  = {"knight": "n", "queen": "q", "bishop": "b", "pawn": "p"}


    @LogExecutionTime
    def check_format(self, string):
        # Pattern: letter (a-h), digit (1-8), letter (a-h), digit (1-8)
        pattern = r'^[a-h][1-8][a-h][1-8]$'
        return bool(re.match(pattern, string))

    @LogExecutionTime
    def uci_str(self, words:list):
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