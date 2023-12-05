from UW_ChessV1 import UW_Chess, STT_move
from distil_whisper import RecordVoice
from loading import Loading_status
import os
from time import sleep
from fastspeech2 import TTS
import argparse
import sys
from render_board import ChessBoard_Render



parser = argparse.ArgumentParser(prog="Undr Wolf Chess", 
                                 description="A blindfold chess trainer",
                                 epilog="Prototype POC")

# Difficulty flag
parser.add_argument('-d', '--difficulty', 
                    type=int, 
                    help='Difficulty range 1 - 20', 
                    default=10)

# Group for mutually exclusive render options
parser.add_argument('-r2d', '--render_2d', 
                          action="store_true",
                          help='Board render flag 2D-classic')


args = parser.parse_args()


# from MicrosoftTTS import TTS
tts = TTS()
game = UW_Chess(bot_level=args.difficulty)
stt = RecordVoice()
stt_move = STT_move()
status = Loading_status()

render = ChessBoard_Render()

def clear_screen():
    # Clear the console screen.
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

def main():
    status.status_check()

    running = True
    board = game.board
    game_move = 1
    move_stack = []
    try:
        while not board.is_game_over() and running:
            clear_screen()
            game.score(board)
            print(f"{move_stack}\n")
            print(f"{board}\n")
            if args.render_2d:
                render.game_render(board)
            
            if game_move % 2 == 0:
                engin_move = game.engin_move(board)
                move_stack.append(engin_move)
                tts_formatting = format_response(engin_move)

                tts.speech(tts_formatting)            

                sleep(2)
                game_move += 1
            else: 
                # move = str(input("move: "))
                text = stt.speech_to_text()
                print(text)
                move = stt_move.uci_str(text)
                print(move)
                valid_move, player_move = game.player_move(move, board)
                if valid_move:
                    move_stack.append(player_move)
                    game_move += 1
                else: 
                    tts.speech(player_move)            

    except KeyboardInterrupt:
        print("\nExiting the program gracefully...")
        sleep(2)
        # Perform any necessary cleanup here
        sys.exit(0)
if __name__ == "__main__":
    main()