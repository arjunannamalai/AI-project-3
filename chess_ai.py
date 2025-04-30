import chess
import random

class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth

    def evaluate(self, board):
        # Basic evaluation based on piece material
        material_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        eval_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                eval_score += material_values.get(piece.piece_type, 0) * (1 if piece.color == chess.WHITE else -1)
        return eval_score

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, False)
                max_eval = max(max_eval, eval)
                board.pop()
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, True)
                min_eval = min(min_eval, eval)
                board.pop()
            return min_eval
            
    def alpha_beta_pruning(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)
            
        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta_pruning(board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                board.pop()
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta_pruning(board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                board.pop()
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def find_best_move(self, board, use_alpha_beta=True):
        best_move = None
        best_value = float('-inf')
        
        for move in board.legal_moves:
            board.push(move)
            if use_alpha_beta:
                move_value = self.alpha_beta_pruning(board, self.depth, float('-inf'), float('inf'), False)
            else:
                move_value = self.minimax(board, self.depth, False)
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
            board.pop()

        return best_move
