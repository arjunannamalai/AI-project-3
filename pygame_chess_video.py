import pygame
import random
import chess
import imageio
import os
import time
from chess_ai import ChessAI

# Constants for board dimensions
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK = (100, 100, 100)

# Load piece images
PIECE_IMAGES = {}

def load_piece_images():
    pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    colors = ['w', 'b']
    for color in colors:
        for piece in pieces:
            name = color + piece
            # Use the correct nested assets directory path
            image = pygame.image.load(f"assets/assets/{name}.png")  
            PIECE_IMAGES[name] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen, board):
    colors = [WHITE, GRAY]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            color = 'w' if piece.color == chess.WHITE else 'b'
            name = color + piece.symbol().lower()
            screen.blit(PIECE_IMAGES[name], (col*SQUARE_SIZE, row*SQUARE_SIZE))

def record_frame(screen, frames):
    image_data = pygame.surfarray.array3d(screen)
    image_data = image_data.swapaxes(0, 1)  # Convert to (height, width, 3)
    frames.append(image_data)

def main(use_alpha_beta=True, output_filename="chess_game.mp4"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Update window title to show which algorithm is running with its depth
    if use_alpha_beta:
        algorithm_name = "Alpha-Beta Pruning (Depth 3)"
        depth = 3
        print("Running Alpha-Beta Pruning with depth 3")
    else:
        algorithm_name = "Minimax (Depth 2)"
        depth = 2
        print("Running Minimax with depth 2")
    
    pygame.display.set_caption(f"Chess AI - {algorithm_name}")
    
    load_piece_images()

    board = chess.Board()
    # Use different depths for each algorithm
    ai = ChessAI(depth=depth)
        
    frames = []
    clock = pygame.time.Clock()

    draw_board(screen, board)
    pygame.display.flip()
    record_frame(screen, frames)
    running = True
    move_count = 0
    
    # Maximum number of moves allowed
    max_moves = 300

    start_time = time.time()
    
    while running and not board.is_game_over() and move_count < max_moves:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.wait(10)

        if board.turn == chess.WHITE:
            move = ai.find_best_move(board, use_alpha_beta=use_alpha_beta)
        else:
            move = random.choice(list(board.legal_moves))

        board.push(move)
        move_count += 1

        draw_board(screen, board)
        pygame.display.flip()
        record_frame(screen, frames)
        clock.tick(30)
        
        # Print current move count and game state periodically
        if move_count % 10 == 0:
            print(f"Move {move_count}: {'White' if board.turn else 'Black'} to move")
            elapsed_time = time.time() - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds")
            
            # Check if the game is in check or checkmate
            if board.is_check():
                print(f"{'White' if not board.turn else 'Black'} is in check!")
            if board.is_checkmate():
                print(f"Checkmate! {'White' if not board.turn else 'Black'} wins!")

    pygame.quit()
    
    # Calculate total runtime
    total_time = time.time() - start_time
    print(f"Total runtime: {total_time:.2f} seconds")

    # Make sure the videos directory exists
    os.makedirs("videos", exist_ok=True)
    
    # Save video in the videos directory
    output_path = os.path.join("videos", output_filename)
    imageio.mimsave(output_path, frames, fps=1)
    print(f"\n✅ Video saved as: {output_path}")
    
    # Print more detailed game result information
    if board.is_checkmate():
        result_message = f"🎯 Game Over. Result: {board.result()} - Checkmate! {'White' if board.result() == '1-0' else 'Black'} wins!"
    elif board.is_stalemate():
        result_message = f"🎯 Game Over. Result: {board.result()} - Stalemate!"
    elif board.is_insufficient_material():
        result_message = f"🎯 Game Over. Result: {board.result()} - Draw due to insufficient material!"
    else:
        result_message = f"🎯 Game Over. Result: {board.result()} - Move limit reached!"
        
    print(result_message)
    
    # Return statistics for the README
    return {
        "algorithm": algorithm_name,
        "moves": move_count,
        "time": total_time,
        "result": board.result(),
        "result_message": result_message
    }

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    print("Make sure you have chess piece images in the 'assets/' folder.")
    print("Running game...")
    
    # Run Alpha-Beta Pruning (depth 3)
    alpha_beta_stats = main(use_alpha_beta=True, output_filename="alphabeta_depth3_game.gif")
    
    # Run Minimax (depth 2)
    minimax_stats = main(use_alpha_beta=False, output_filename="minimax_depth2_game.gif")
    
    # Print comparison
    print("\n--- Performance Comparison ---")
    print(f"Alpha-Beta Pruning (Depth 3): {alpha_beta_stats['moves']} moves in {alpha_beta_stats['time']:.2f} seconds")
    print(f"Minimax (Depth 2): {minimax_stats['moves']} moves in {minimax_stats['time']:.2f} seconds")
    print(f"Alpha-Beta Result: {alpha_beta_stats['result_message']}")
    print(f"Minimax Result: {minimax_stats['result_message']}")

