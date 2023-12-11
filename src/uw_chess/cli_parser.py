# ============================================================================
# cli_parser.py
# Argument parser library
# ============================================================================

import argparse

def get_parser():
    # Argument parser setup for command-line options
    parser = argparse.ArgumentParser(prog="Undr Wolf Chess", 
                                    description="A blindfold chess trainer",
                                    epilog="Prototype POC")

    # Argument for specifying the path to the chess engine
    parser.add_argument('-p', 
                        '--engine_path', 
                        type=str, 
                        help='The path to preferred chess engine')

    # Argument for setting the difficulty level
    parser.add_argument('-d', 
                        '--difficulty', 
                        type=int, 
                        help='Difficulty range 1 - 20', 
                        default=10)

    # Flag for enabling 2D board rendering
    parser.add_argument('-r2d', 
                        '--render_2d', 
                        action="store_true",
                        help='Board render flag 2D-classic')

    # Argument for setting up a random board with specified number of pieces
    parser.add_argument('-rb', 
                        '--random_board', 
                        type=int,
                        help='Type and integer 2 - 32 required peaces',
                        default=32)

    # Argument for setting the coordinate difficulty
    parser.add_argument('-cd', 
                        '--coordinate_difficulty', 
                        type=int,
                        help='Easy=1, Intermediate=2, Hard=3. Default = Intermediate ',
                        default=1)

    return parser 