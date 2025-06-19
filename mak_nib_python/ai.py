import random
from copy import deepcopy
from constants import RED, BLUE, ROWS, COLS

class MakNibAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.max_depth = {
            'easy': 0,
            'medium': 3,
            'hard': 5
        }[difficulty]
        self.transposition_table = {}

    def get_move(self, board, color, screen):
        if self.difficulty == 'easy':
            return self.get_easy_move(board, color)
        elif self.difficulty == 'medium':
            return self.get_medium_move(board, color, screen, show_moves=False)
        else:
            return self.get_hard_move(board, color, screen, show_moves=False)

    def get_easy_move(self, board, color):
        all_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    moves = board.get_valid_moves(piece)
                    for move in moves:
                        all_moves.append((piece, move))
        return random.choice(all_moves) if all_moves else None

    def get_medium_move(self, board, color, screen, show_moves=True):
        # Add show_moves parameter to control visualization
        best_move = None
        best_score = float('-inf')
        
        for move in self.get_possible_moves(board, color):
            new_board = deepcopy(board)
            # Only update display if show_moves is True
            self.make_move(new_board, move, color, screen if show_moves else None)
            score = self.minimax(new_board, self.max_depth - 1, False, color, screen if show_moves else None)
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def get_hard_move(self, board, color, screen, show_moves=True):
        board_hash = hash(str(board.board))

        best_score = float('-inf')
        best_move = None
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    moves = board.get_valid_moves(piece)
                    # จัดลำดับการเคลื่อนไหวโดยการประเมินคะแนนก่อน
                    moves.sort(key=lambda move: self.evaluate_move(board, piece, move[0], move[1], color), reverse=True)
                    for move_row, move_col in moves:
                        test_board = board.simulate_move(piece, move_row, move_col, screen if show_moves else None)
                        score = self.iterative_deepening(test_board, color, screen if show_moves else None)
                        if score > best_score:
                            best_score = score
                            best_move = (piece, (move_row, move_col))
        
        return best_move

    def iterative_deepening(self, board, color, screen):
        best_score = float('-inf')
        for depth in range(1, self.max_depth + 1):
            score = self.alpha_beta(board, depth, float('-inf'), float('inf'), True, color, screen)
            if score > best_score:
                best_score = score
        return best_score

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing, ai_color, screen):
        board_hash = hash(str(board.board))
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        if depth == 0 or board.game_over:
            score = self.evaluate_board(board, ai_color)
            self.transposition_table[board_hash] = score
            return score
        
        best_score = float('-inf') if is_maximizing else float('inf')
        current_color = ai_color if is_maximizing else (RED if ai_color == BLUE else BLUE)
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece and piece.color == current_color:
                    moves = board.get_valid_moves(piece)
                    for move_row, move_col in moves:
                        test_board = board.simulate_move(piece, move_row, move_col, screen)
                        score = self.alpha_beta(test_board, depth - 1, alpha, beta, not is_maximizing, ai_color, screen)
                        
                        if is_maximizing:
                            best_score = max(best_score, score)
                            alpha = max(alpha, best_score)
                        else:
                            best_score = min(best_score, score)
                            beta = min(beta, best_score)
                        
                        # Alpha-Beta Pruning
                        if beta <= alpha:
                            break

        self.transposition_table[board_hash] = best_score
        return best_score

    def evaluate_move(self, board, piece, new_row, new_col, color):
        score = 0
        if board.can_capture(board, new_row, new_col, color):
            score += 10
        if not board.can_capture(board, new_row, new_col, RED if color == BLUE else BLUE):
            score += 5
        return score

    def evaluate_board(self, board, color):
        score = 0
        
        # คะแนนจากจำนวนหมาก
        red_pieces = sum(piece.color == RED for row in board.board for piece in row if piece)
        blue_pieces = sum(piece.color == BLUE for row in board.board for piece in row if piece)
        score += blue_pieces - red_pieces if color == BLUE else red_pieces - blue_pieces
        
        # คะแนนจากการควบคุมตำแหน่ง (กลาง)
        score += self.evaluate_position(board, color)
        
        # คะแนนจากการจับหมาก
        score += self.evaluate_captures(board, color)
        
        return score

    def evaluate_position(self, board, color):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece:
                    # ตำแหน่งกลางมีค่ามากกว่าตำแหน่งขอบ
                    if piece.color == color:
                        if row in [3, 4] and col in [3, 4]:  # ตำแหน่งกลาง
                            score += 2
                        elif row in [0, 7] or col in [0, 7]:  # ขอบ
                            score -= 1
        return score

    def evaluate_captures(self, board, color):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    # เพิ่มคะแนนถ้าสามารถจับหมากฝ่ายตรงข้ามได้
                    moves = board.get_valid_moves(piece)
                    for move_row, move_col in moves:
                        if board.can_capture(board, move_row, move_col, color):
                            score += 10
        return score
