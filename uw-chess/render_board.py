import pygame
import chess

from runtime_test import LogExecutionTime

pygame.init()


class ChessBoard_Render:
    def __init__(self):
        # Constants for the board size
        self.WIDTH  = 600
        self.HEIGHT = 600
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS
        self.clock = pygame.time.Clock()
        # Board color Colors
        self.WHITE = (218, 255, 238)
        self.BLACK = (43, 100, 62)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Undr Wolf - Blindfold Chess")
        self.images = self.load_images()

        self.board_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.initialize_board_surface()

    # Load images
    @LogExecutionTime
    def load_images(self):
        pieces = ["R", "N", "B", "Q", "K", "P"]
        colors = ["b", "w"]
        images = {}
        for color in colors:
            for piece in pieces:
                try:
                    images[color + piece] = pygame.transform.scale(
                        pygame.image.load(f"./game_assets/classic/{color + piece}.png"), 
                        (self.SQUARE_SIZE, self.SQUARE_SIZE))
                except FileNotFoundError:
                    print(f"Error loading image for {color + piece}")
        return images

    @LogExecutionTime
    def initialize_board_surface(self):
        self.board_surface.fill(self.BLACK)
        for row in range(self.ROWS):
            for col in range(row % 2, self.COLS, 2):
                pygame.draw.rect(self.board_surface, self.WHITE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    @LogExecutionTime
    def draw_pieces(self, board):
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                color = 'w' if piece.color == chess.WHITE else 'b'
                key = color + piece.symbol().upper()
                column = sq % 8
                row = 7 - (sq // 8)
                self.screen.blit(self.images[key], 
                                 pygame.Rect(column * self.SQUARE_SIZE, 
                                             row * self.SQUARE_SIZE, 
                                             self.SQUARE_SIZE, 
                                             self.SQUARE_SIZE))

    @LogExecutionTime
    def draw_board(self):
        self.screen.blit(self.board_surface, (0, 0))

    @LogExecutionTime
    def game_render(self, board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return running
             
        self.draw_board()
        self.draw_pieces(board)
        pygame.display.flip()
        self.clock.tick(60)