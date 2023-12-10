from .UW_ChessV1 import UW_Chess
from .STT import RecordVoice
from .TTS import TTS_move
from .render_board import ChessBoard_Render
from .loading import Loading_status
from time import sleep
import os
import argparse
import sys
import asyncio


parser = argparse.ArgumentParser(prog="Undr Wolf Chess", 
                                 description="A blindfold chess trainer",
                                 epilog="Prototype POC")

# Difficulty flag
parser.add_argument('-d', 
                    '--difficulty', 
                    type=int, 
                    help='Difficulty range 1 - 20', 
                    default=10)

# Render 2d board flag
parser.add_argument('-r2d', 
                    '--render_2d', 
                    action="store_true",
                    help='Board render flag 2D-classic')
                    
# Render 2d board flag
parser.add_argument('-rb', 
                    '--random_board', 
                    type=int,
                    help='Type and integer 2 - 32 required peaces',
                    default=32)

# Board render difficulty
parser.add_argument('-cd', 
                    '--coordinate_difficulty', 
                    type=int,
                    help='Easy=1, Intermediate=2, Hard=3. Default = Intermediate ',
                    default=1)

args = parser.parse_args()

tts     = TTS_move()
game    = UW_Chess(bot_level=args.difficulty)
stt     = RecordVoice()
status  = Loading_status()
render = ChessBoard_Render()

# Clear the console screen.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_response(engin_move):
    inserts = '. '
    positions = [1, 3, 5]
    formatting = engin_move
    for i, position in enumerate(sorted(positions)):
        # Adjust position for the already inserted characters
        adjusted_position = position + i
        formatting = formatting[:adjusted_position] + inserts + formatting[adjusted_position:]

    return formatting.upper()

async def player_STT_move():
    audio = stt.listen()
    recording, text = stt.analyze(audio)
    return recording, text
    
async def main():
    status.status_check()

    move_stack = []
    if args.random_board:
        board, move_stack = game.generate_random_position(args.random_board)
        print(board)
    else:
        board = game.board
        print(board)
    running = True
    # render.draw_board()
    game_move = 1
    try:
        while not board.is_game_over() and running:
            clear_screen()
            print(game_move)
            game.score(board)
            print(f"{move_stack}\n")
            print(f"{board}\n")

            # Render pygame chess board
            if args.render_2d:
                render.game_render(board, args.coordinate_difficulty)
            

            if game_move % 2 == 0:
                # Chess boat makes a move
                engin_move = game.engin_move(board)
                move_stack.append(engin_move)

                tts.speech(engin_move)            
                game_move += 1
            else: 
                # User makes a move

                recording = True # Set audio recoding condition to True
                    
                while recording:
                    
                    audio = await stt.listen() # Record audio returns audio object

                    recording, text = await stt.analyze(audio) 
                    if not recording:
                        player_move = text
                        break

                print(f"Rec {recording} Move: {player_move}")

                print(player_move)
                valid_move, player_move = game.player_move(player_move, board)
                print(player_move)
                if valid_move:
                    move_stack.append(player_move)
                    game_move += 1
                else: 
                    tts.speech(player_move)            

    except KeyboardInterrupt:
        print("\nExiting program")
        sleep(1)
        sys.exit(0)

def main_wrapper():
    asyncio.run(main())

if __name__ == "__main__":
    main_wrapper()