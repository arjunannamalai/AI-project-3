import os
import requests
from PIL import Image
import io

def download_chess_pieces():
    """Download high-quality chess piece images from a reliable source."""
    
    # Create directories if they don't exist
    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/assets", exist_ok=True)
    
    # Source URLs for chess pieces (directly using PNG versions from Chess.com)
    piece_urls = {
        # White pieces
        "wp": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wp.png",
        "wr": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wr.png",
        "wn": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wn.png",
        "wb": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wb.png",
        "wq": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wq.png",
        "wk": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wk.png",
        
        # Black pieces
        "bp": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bp.png",
        "br": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/br.png",
        "bn": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bn.png",
        "bb": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bb.png",
        "bq": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bq.png",
        "bk": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bk.png",
    }
    
    # Alternatively, if Chess.com images don't work, use these from Wikimedia
    backup_urls = {
        # White pieces
        "wp": "https://upload.wikimedia.org/wikipedia/commons/0/04/Chess_plt60.png",
        "wr": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Chess_rlt60.png",
        "wn": "https://upload.wikimedia.org/wikipedia/commons/2/28/Chess_nlt60.png",
        "wb": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Chess_blt60.png",
        "wq": "https://upload.wikimedia.org/wikipedia/commons/4/49/Chess_qlt60.png",
        "wk": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Chess_klt60.png",
        
        # Black pieces
        "bp": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Chess_pdt60.png",
        "br": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Chess_rdt60.png",
        "bn": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Chess_ndt60.png",
        "bb": "https://upload.wikimedia.org/wikipedia/commons/8/81/Chess_bdt60.png",
        "bq": "https://upload.wikimedia.org/wikipedia/commons/a/af/Chess_qdt60.png",
        "bk": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Chess_kdt60.png",
    }
    
    # Size for the chess pieces
    piece_size = 64
    
    # Download each piece
    for piece_name, url in piece_urls.items():
        try:
            # Request the PNG image
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to download {piece_name} from primary source, trying backup...")
                backup_url = backup_urls.get(piece_name)
                if backup_url:
                    response = requests.get(backup_url)
                    if response.status_code != 200:
                        print(f"Failed to download {piece_name} from backup source as well.")
                        continue
                else:
                    continue
            
            # Process and resize the image
            img = Image.open(io.BytesIO(response.content))
            
            # Handle transparency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize the image
            img = img.resize((piece_size, piece_size), Image.LANCZOS)
            
            # Save the image to both locations
            img.save(f"assets/{piece_name}.png")
            img.save(f"assets/assets/{piece_name}.png")
            
            print(f"Downloaded and processed {piece_name}.png")
                
        except Exception as e:
            print(f"Error processing {piece_name}: {str(e)}")
    
    print("Chess piece download complete!")

if __name__ == "__main__":
    print("Downloading high-quality chess piece images...")
    download_chess_pieces()
