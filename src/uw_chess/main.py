# ============================================================================
# main.py
# Main script and game loop
# ============================================================================

from uw_chess_v1 import UW_Chess
# from _stt import RecordVoice
from tts import TTS_move
from loading import Loading_status
from uci_formatting import Formatting
from multiprocessing import Process, Queue
from cli_parser import get_parser
from time import sleep
import os
import sys
from realtime_stt import AudioRecorder, AudioAnalyzer

# Cli argument parser from cli_parser.py
parser  = get_parser()
args    = parser.parse_args()

tts     = TTS_move()
game    = UW_Chess(engine_path=args.engine_path, bot_level=args.difficulty)
# stt     = RecordVoice()
status  = Loading_status()
formatting = Formatting()


# Clear the console screen.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


    
def game_loop(game_queue, rec_queue, recorder):
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


            # Chess engine's turn to move
            if game_move % 2 == 0: # Users moves on uneven numbers and game engin (chess bot) moves on even numbers
                engine_move = game.engine_move(board) # Function returns game engin (chess bot) move s UCI-string
                move_stack.append(engine_move)       # Append move to move_stack
                tts.speech(engine_move)              # Text-to-speech game engin move
                game_move += 1                      # Increment game move
            else: 
                # Player's turn to move
                recorder.process_rec("rec")
                player_making_move = True
                while player_making_move:
                    text = game_queue.get()
                    uci = formatting.uci_str(text)
                    if uci:
                        player_making_move = False

                rec_queue.put('stop')

                
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

def main():
    print("starting")
    
    rec_queue = Queue()  # Queue for raw data to recorder and analyzer
    game_queue = Queue()  # Queue for processed data to game loop
    
    recorder = AudioRecorder(rec_queue)
    analyzer = AudioAnalyzer(rec_queue, game_queue)

    p1 = Process(target=analyzer.process_analyze, args=('analyze',))
    p2 = Process(target=recorder.process_rec, args=('rec1',))
    p3 = Process(target=game_loop, args=(game_queue, rec_queue, recorder))  # Pass the game_queue to game_loop
    
    p1.start()
    p2.start()
    p3.start()

    try:
        # Wait for the processes to finish (or handle them as needed)
        p1.join()
        p2.join()
        p3.join()

    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")

        p1.terminate()
        p2.terminate()
        p3.terminate()
        
        p1.join()
        p2.join()
        p3.join()
        print("Processes terminated successfully.")

if __name__ == "__main__":
    main()