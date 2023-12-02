# import chess
# import chess.engine
# import chess.svg
# import json
# from time import sleep
# import os 

# with open("./keys.json") as f:
#     keys = json.load(f)

# # Specify the path to the Stockfish binary
# stockfish_path = keys["stockfish_path"]

# # Set up the engine
# engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)



# def engin_move(b):
#     result = engine.play(b, chess.engine.Limit(time=0.1))
#     board = b.push(result.move)
#     return board

# def player_move(move, b):
#     board = b.push_san(str(move))
#     return board

# def game_score(board):
#     info = engine.analyse(board, chess.engine.Limit(time=0.1))

#     score = info["score"].relative.score()
#     if score >0:
#         favor = "White"
#     else:
#         favor = "Black"
#     print("score:", score, favor)

# def clear_screen():
#     # Clear the console screen.
#     os.system('cls' if os.name == 'nt' else 'clear')

# def main():

#     board = chess.Board()
#     game_move = 1
#     while not board.is_game_over():
#         clear_screen()
#         game_score(board)
#         print(board)
#         if game_move % 2 == 0:
#             engin_move(board)
#             sleep(2)
#         else: 
#             move = str(input("move: "))
#             player_move(move, board)
#         game_move += 1

# if __name__ == "__main__":
    # main()

from UW_ChessV1 import UW_Chess
import os
from time import sleep
game = UW_Chess()

def clear_screen():
    # Clear the console screen.
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    board = game.board
    game_move = 1
    move_stack = []
    while not board.is_game_over():
        clear_screen()
        game.score(board)
        print(f"{move_stack}\n")
        print(f"{board}\n")
        if game_move % 2 == 0:
            engin_move = game.engin_move(board)
            move_stack.append(engin_move)
            sleep(2)
            game_move += 1
        else: 
            move = str(input("move: "))
            valid_move, player_move = game.player_move(move, board)
            move_stack.append(player_move)
            if valid_move:
                game_move += 1
            else: pass

if __name__ == "__main__":
    main()