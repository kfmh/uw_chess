from UW_ChessV1 import UW_Chess
from STT import RecordVoice
from loading import Loading_status
import os
from time import sleep
import argparse
import sys
from render_board import ChessBoard_Render
from TTS import TTS_move
import asyncio


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
tts = TTS_move()
game = UW_Chess(bot_level=args.difficulty)
stt = RecordVoice()
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

async def player_STT_move():
    audio = stt.listen()
    recording, text = stt.analyze(audio)
    return recording, text
    
async def main():
    status.status_check()

    running = True
    board = game.board
    render.draw_board()
    game_move = 1
    move_stack = []
    try:
        while not board.is_game_over() and running:
            clear_screen()
            print(game_move)
            game.score(board)
            print(f"{move_stack}\n")
            print(f"{board}\n")
            if args.render_2d:
                render.game_render(board)
            
            if game_move % 2 == 0:
                engin_move = game.engin_move(board)
                move_stack.append(engin_move)

                tts.speech(engin_move)            

                sleep(0.5)
                game_move += 1
            else: 
                recording = True

                # while recording:
                #     recording, player_move = await player_STT_move()
                #     print(f"Rec {recording} Move: {player_move}")
                    
                while recording:
                    audio = stt.listen()
                    recording, text = await stt.analyze(audio)
                    if recording != True:
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
        # Perform any necessary cleanup here
        sys.exit(0)
if __name__ == "__main__":
    asyncio.run(main())