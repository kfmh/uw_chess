from UW_ChessV1 import UW_Chess, STT_move
# from WhisperSTT import RecordVoice
from distil_whisper import RecordVoice
from loading import Loading_status
import os
from time import sleep
from fastspeech2 import TTS
import argparse
import pygame
import chess
import sys


# Initialize Pygame
pygame.init()
# Create the parser
difficulty = argparse.ArgumentParser(description="Bot Difficulty (1-20)")

# Add arguments
difficulty.add_argument('-d', '--difficulty', type=int, help='Difficulty range 1 - 20')

# Parse the arguments
args = difficulty.parse_args()

# from MicrosoftTTS import TTS
tts = TTS()
game = UW_Chess(bot_level=args.difficulty)
stt = RecordVoice()
stt_move = STT_move()
status = Loading_status()


class ChessBoard_Render:
    def __init__(self):
    # Constants for the board size
        self.WIDTH = 400
        self.HEIGHT = 400
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS

        # Colors
        self.WHITE = (218, 255, 238)
        self.BLACK = (43, 100, 62)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")

    # Load images
    def load_images(self):
        pieces = ["R", "N", "B", "Q", "K", "P"]
        colors = ["b", "w"]
        images = {}
        for color in colors:
            for piece in pieces:
                images[color + piece] = pygame.transform.scale(pygame.image.load(f"./game_assets/{color + piece}.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE))
        return images

    def draw_board(self):
        self.screen.fill(self.BLACK)
        for row in range(self.ROWS):
            for col in range(row % 2, self.ROWS, 2):
                pygame.draw.rect(self.screen, self.WHITE, (row * self.SQUARE_SIZE, col * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self, board):
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            images = self.load_images()
            if piece:
                color = 'w' if piece.color == chess.WHITE else 'b'
                key = color + piece.symbol().upper()
                column = sq % 8
                row = 7 - (sq // 8)
                self.screen.blit(images[key], pygame.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

border_render = ChessBoard_Render()

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

    clock = pygame.time.Clock()
    running = True

    board = game.board
    game_move = 1
    move_stack = []
    while not board.is_game_over() or running:
        clear_screen()
        game.score(board)
        print(f"{move_stack}\n")
        print(f"{board}\n")
        border_render.draw_board()
        border_render.draw_pieces(board)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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