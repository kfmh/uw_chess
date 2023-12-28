# ============================================================================
# main.py
# Main script and game loop
# ============================================================================

from uw_chess_v1 import UW_Chess
from stt import RecordVoice
from tts import TTS_move
from render_board import ChessBoard_Render
from loading import Loading_status
from cli_parser import get_parser
from time import sleep
import os
import sys
import asyncio

# Cli argument parser from cli_parser.py
parser  = get_parser()
args    = parser.parse_args()

tts     = TTS_move()
game    = UW_Chess(engine_path=args.engine_path, bot_level=args.difficulty)
stt     = RecordVoice()
status  = Loading_status()
render  = ChessBoard_Render()


# Clear the console screen.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# =================================================================
# TODO fix STT event-loop so that it is continuously recording
async def player_STT_move():
    audio = stt.listen()
    recording, text = stt.analyze(audio)
    return recording, text
# TODO fix STT event-loop so that it is continuously recording
# =================================================================
    
async def main():
    """
    The main function that runs the chess game loop. It handles game state, moves,
    and interactions between different components like TTS, STT, and the chess engine.
    """
    # When using models with api-inference
    # status.status_check() # check status of api-inference endpoints

    move_stack = [] # stores list of move made during the game

    # condition for using random generated board setup or beginning game setup
    if args.random_board:
        board, move_stack = game.generate_random_position(args.random_board)
        print(board)
    else:
        board = game.board
        print(board)
    
    running = True # is game still running
    game_move = 1  # White moves on uneven numbers and black moves on even numbers
    try:
        while not board.is_game_over() and running: # Will break if check mate or if player exits game
            # command-line ASCII rendering 
            clear_screen()
            print(game_move) 
            game.score(board)
            print(f"{move_stack}\n")
            print(f"{board}\n")
            
            # Condition for rending 2D board
            if args.render_2d:
                render.game_render(board, args.coordinate_difficulty)


            # Chess engine's turn to move
            if game_move % 2 == 0: # Users moves on uneven numbers and game engin (chess bot) moves on even numbers
                engine_move = game.engine_move(board) # Function returns game engin (chess bot) move s UCI-string
                move_stack.append(engine_move)       # Append move to move_stack
                tts.speech(engine_move)              # Text-to-speech game engin move
                game_move += 1                      # Increment game move
            else: 
                # Player's turn to move
                recording = True                    # Set STT recording true
                
                # =================================================================
                # TODO fix STT event-loop so that it is continuously recording
                while recording:
                    audio = await stt.listen()      
                    recording, text = await stt.analyze(audio)
                    if not recording:
                        player_move = text
                        break
                # TODO fix STT event-loop so that it is continuously recording
                # =================================================================

                valid_move, player_move = game.player_move(player_move, board) # update board with users move
                if valid_move:
                    move_stack.append(player_move)
                    game_move += 1
                else: 
                    tts.speech(player_move)   # text to speech with error message 

    except KeyboardInterrupt:
        # Quit game event cleanup 
        print("\nExiting program")
        sleep(1)
        sys.exit(0)

def main_wrapper():
    # Wrapper function for the main async function.
    asyncio.run(main())

if __name__ == "__main__":
    main_wrapper()
