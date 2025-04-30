# main.py

import chess
import random
from chess_ai import ChessAI

def play_game(use_alpha_beta=True):
    board = chess.Board()
    ai = ChessAI(depth=3)

    print(f"Starting game with {'Alpha-Beta' if use_alpha_beta else 'Minimax'} AI\n")

    while not board.is_game_over():
        print(board)
        print("\n")

        if board.turn == chess.WHITE:
            print("White's move (AI):")
            move = ai.find_best_move(board, use_alpha_beta=use_alpha_beta)
        else:
            print("Black's move (Random):")
            move = random.choice(list(board.legal_moves))
            print(f"Random selected move: {move}")

        board.push(move)

    print("\nGame Over")
    print("Result:", board.result())

# Run both games to compare
if __name__ == "__main__":
    #print("=== GAME 1: Minimax AI ===")
    #play_game(use_alpha_beta=False)

    print("\n\n=== GAME 2: Alpha-Beta AI ===")
    play_game(use_alpha_beta=True)
