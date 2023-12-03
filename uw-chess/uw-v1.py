from UW_ChessV1 import UW_Chess, STT_move
from WhisperSTT import RecordVoice
import os
from time import sleep
from fastspeech2 import TTS

# from MicrosoftTTS import TTS
tts = TTS()
game = UW_Chess()
stt = RecordVoice()
stt_move = STT_move()

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

if __name__ == "__main__":
    main()