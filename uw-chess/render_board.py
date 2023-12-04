import pygame
import chess
import sys


# Initialize Pygame
pygame.init()

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
                row = sq // 8
                self.screen.blit(images[key], pygame.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))


    def init_board(self, board):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_board()
            self.draw_pieces(board)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

