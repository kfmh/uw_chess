import pygame
import chess


pygame.init()


class ChessBoard_Render:
    def __init__(self):
    # Constants for the board size
        self.WIDTH = 400
        self.HEIGHT = 400
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS
        self.clock = pygame.time.Clock()
        # Colors
        self.WHITE = (218, 255, 238)
        self.BLACK = (43, 100, 62)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Undr Wolf - Blindfold Chess")
        self.images = self.load_images()

    # Load images
    def load_images(self):
        pieces = ["R", "N", "B", "Q", "K", "P"]
        colors = ["b", "w"]
        images = {}
        for color in colors:
            for piece in pieces:
                try:
                    images[color + piece] = pygame.transform.scale(
                        pygame.image.load(f"./game_assets/{color + piece}.png"), 
                        (self.SQUARE_SIZE, self.SQUARE_SIZE))
                except FileNotFoundError:
                    print(f"Error loading image for {color + piece}")
        return images

    def draw_board(self):
        self.screen.fill(self.BLACK)
        for row in range(self.ROWS):
            for col in range(row % 2, self.ROWS, 2):
                pygame.draw.rect(self.screen, self.WHITE, (row * self.SQUARE_SIZE, col * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

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