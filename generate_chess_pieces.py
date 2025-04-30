import os
import pygame

# Initialize pygame
pygame.init()

# Create the assets directory if it doesn't exist
os.makedirs("assets", exist_ok=True)
os.makedirs("assets/assets", exist_ok=True)  # Ensure nested directory exists for compatibility

# Define piece colors
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
BACKGROUND = (0, 0, 0, 0)  # Transparent background

# Define piece size
PIECE_SIZE = 64

# Function to draw a pawn
def draw_pawn(surface, color):
    # Base
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4)
    # Top
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 - 10), PIECE_SIZE//6)
    # Neck
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 5, PIECE_SIZE//2 - 5, 10, 15))

# Function to draw a rook
def draw_rook(surface, color):
    # Base
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 15, PIECE_SIZE//2, 30, 20))
    # Body
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 10, PIECE_SIZE//2 - 15, 20, 25))
    # Top castellations
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 15, PIECE_SIZE//2 - 25, 8, 10))
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 4, PIECE_SIZE//2 - 25, 8, 10))
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 + 7, PIECE_SIZE//2 - 25, 8, 10))

# Function to draw a knight
def draw_knight(surface, color):
    # Base
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4)
    # Body
    points = [
        (PIECE_SIZE//2 - 10, PIECE_SIZE//2),
        (PIECE_SIZE//2 - 5, PIECE_SIZE//2 - 15),
        (PIECE_SIZE//2, PIECE_SIZE//2 - 25),
        (PIECE_SIZE//2 + 10, PIECE_SIZE//2 - 20),
        (PIECE_SIZE//2 + 15, PIECE_SIZE//2 - 10),
        (PIECE_SIZE//2 + 10, PIECE_SIZE//2 + 5),
        (PIECE_SIZE//2, PIECE_SIZE//2 + 5)
    ]
    pygame.draw.polygon(surface, color, points)

# Function to draw a bishop
def draw_bishop(surface, color):
    # Base
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4)
    # Body
    pygame.draw.polygon(surface, color, [
        (PIECE_SIZE//2 - 8, PIECE_SIZE//2 + 5),
        (PIECE_SIZE//2, PIECE_SIZE//2 - 25),
        (PIECE_SIZE//2 + 8, PIECE_SIZE//2 + 5)
    ])
    # Top
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 - 25), 5)

# Function to draw a queen
def draw_queen(surface, color):
    # Base
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4)
    # Body
    pygame.draw.polygon(surface, color, [
        (PIECE_SIZE//2 - 15, PIECE_SIZE//2 + 5),
        (PIECE_SIZE//2, PIECE_SIZE//2 - 20),
        (PIECE_SIZE//2 + 15, PIECE_SIZE//2 + 5)
    ])
    # Crown points
    points = []
    for i in range(5):
        angle = i * (2 * 3.14159 / 5)
        x = PIECE_SIZE//2 + 12 * pygame.math.Vector2(0, -1).rotate_rad(angle).x
        y = PIECE_SIZE//2 - 25 + 12 * pygame.math.Vector2(0, -1).rotate_rad(angle).y
        points.append((x, y))
    
    pygame.draw.polygon(surface, color, points)

# Function to draw a king
def draw_king(surface, color):
    # Base
    pygame.draw.circle(surface, color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4)
    # Body
    pygame.draw.polygon(surface, color, [
        (PIECE_SIZE//2 - 12, PIECE_SIZE//2 + 5),
        (PIECE_SIZE//2, PIECE_SIZE//2 - 20),
        (PIECE_SIZE//2 + 12, PIECE_SIZE//2 + 5)
    ])
    # Cross
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 3, PIECE_SIZE//2 - 35, 6, 20))
    pygame.draw.rect(surface, color, (PIECE_SIZE//2 - 10, PIECE_SIZE//2 - 28, 20, 6))

# Function to generate a chess piece image
def create_piece(color, piece_type, filename):
    surface = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
    surface.fill(BACKGROUND)  # Transparent background
    
    # Draw the appropriate piece
    if piece_type == 'P':
        draw_pawn(surface, color)
    elif piece_type == 'R':
        draw_rook(surface, color)
    elif piece_type == 'N':
        draw_knight(surface, color)
    elif piece_type == 'B':
        draw_bishop(surface, color)
    elif piece_type == 'Q':
        draw_queen(surface, color)
    elif piece_type == 'K':
        draw_king(surface, color)
    
    # Add outline for better visibility
    outline_color = (20, 20, 20) if color == WHITE else (70, 70, 70)
    pygame.draw.circle(surface, outline_color, (PIECE_SIZE//2, PIECE_SIZE//2 + 15), PIECE_SIZE//4, 2)
    
    # Save to file in both locations
    pygame.image.save(surface, filename)
    nested_filename = filename.replace('assets/', 'assets/assets/')
    pygame.image.save(surface, nested_filename)
    
    print(f"Created {filename}")

# Create pieces
pieces = [
    # White pieces
    (WHITE, 'P', 'assets/wp.png'),  # Pawn
    (WHITE, 'R', 'assets/wr.png'),  # Rook
    (WHITE, 'N', 'assets/wn.png'),  # Knight
    (WHITE, 'B', 'assets/wb.png'),  # Bishop
    (WHITE, 'Q', 'assets/wq.png'),  # Queen
    (WHITE, 'K', 'assets/wk.png'),  # King
    
    # Black pieces
    (BLACK, 'P', 'assets/bp.png'),  # Pawn
    (BLACK, 'R', 'assets/br.png'),  # Rook
    (BLACK, 'N', 'assets/bn.png'),  # Knight
    (BLACK, 'B', 'assets/bb.png'),  # Bishop
    (BLACK, 'Q', 'assets/bq.png'),  # Queen
    (BLACK, 'K', 'assets/bk.png'),  # King
]

# Generate all piece images
for color, symbol, filename in pieces:
    create_piece(color, symbol, filename)

print("All chess piece images generated in the assets directory with distinct shapes.")