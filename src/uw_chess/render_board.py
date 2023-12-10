import pygame
import chess
import pkg_resources

pygame.init()

class ChessBoard_Render:
    def __init__(self):
        # Constants for the board size
        self.WIDTH = 600
        self.HEIGHT = 600
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = self.WIDTH // self.COLS

        # Set up the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Undr Wolf - Blindfold Chess")

        # Load images
        self.images = self.load_images()

        # Load and set the background image
        self.board_paths = ["./game_assets/chess_board_eazy.png", "./game_assets/chess_board_intermediate.png", "./game_assets/chess_board_hard.png"]

        # Initialize clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Running flag for the game loop
        self.running = True

    def load_images(self):
        pieces = ["R", "N", "B", "Q", "K", "P"]
        colors = ["b", "w"]
        images = {}
        for color in colors:
            for piece in pieces:
                try:
                    path = pkg_resources.resource_filename(__name__, f"game_assets/classic/{color + piece}.png")
                    images[color + piece] = pygame.transform.scale(
                        pygame.image.load(path), 
                        (self.SQUARE_SIZE, self.SQUARE_SIZE))
                except FileNotFoundError:
                    print(f"Error loading image for {color + piece}")
        return images

    def load_background_image(self, board_render=1):
        # Load the background chessboard image
        file_name = pkg_resources.resource_filename(__name__, self.board_paths[board_render])
        # file_name = self.board_paths[board_render]
        try:
            background = pygame.image.load(file_name)
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            return background
        except FileNotFoundError:
            print(f"Error loading background image: {file_name}")
            return pygame.Surface((self.WIDTH, self.HEIGHT))  # Fallback surface

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

    def game_render(self, board, board_render):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return self.running

        self.screen.blit(self.load_background_image((board_render-1)), (0, 0))
        self.draw_pieces(board)
        pygame.display.update()  # Update the parts that have changed
        self.clock.tick(60)

# # Main game loop
# chess_board_render = ChessBoard_Render()
# chess_board = chess.Board()
# while chess_board_render.running:
#     chess_board_render.game_render(chess_board)
