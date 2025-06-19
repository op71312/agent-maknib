import pygame
import copy
from constants import WIDTH, HEIGHT, WHITE, BLACK, RED, BLUE, ROWS, COLS, SQUARE_SIZE
from piece import Piece
from ai import MakNibAI
import time
import sys

class Board:
    def __init__(self, ai_difficulty=None):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.selected_piece = None
        self.turn = RED
        self.valid_moves = []
        self.red_score = 0
        self.blue_score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_over = False
        self.start_time = time.time()
        self.ai = MakNibAI(ai_difficulty) if ai_difficulty else None
        self.human_color = RED
        self.initialize_pieces()

    def initialize_pieces(self):
        # ตั้งค่าตำแหน่งเริ่มต้นของหมาก
        # หมากฝ่ายแดง (ผู้เล่น)
        for col in range(8):
            self.board[0][col] = Piece(0, col, RED)
            self.board[7][col] = Piece(7, col, BLUE)

    def draw_squares(self, screen):
        if screen is None:  # Skip drawing if no screen
            return
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, 
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(screen)

    def draw_scores(self, screen):
        red_pieces = sum(piece.color == RED for row in self.board for piece in row if piece)
        blue_pieces = sum(piece.color == BLUE for row in self.board for piece in row if piece)
        red_text = self.font.render(f'Red: {red_pieces}', True, RED)
        blue_text = self.font.render(f'Blue: {blue_pieces}', True, BLUE)
        screen.blit(red_text, (10, 10))
        screen.blit(blue_text, (WIDTH - 110, 10))

    def draw_valid_moves(self, screen):
        transparent_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        transparent_surface.fill((0, 255, 0, 128))
        for move in self.valid_moves:
            row, col = move
            screen.blit(transparent_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def move_piece(self, piece, row, col, screen):
        # Store old position
        old_row = piece.row
        old_col = piece.col
        
        # Update piece position
        piece.row = row
        piece.col = col
        self.board[old_row][old_col] = None
        self.board[row][col] = piece
        
        # Only check captures and update display if screen exists
        self.check_for_capture(piece, row, col, screen)

    def get_valid_moves(self, piece):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            for i in range(1, ROWS):
                new_row = piece.row + d[0] * i
                new_col = piece.col + d[1] * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    if self.board[new_row][new_col] is None:
                        moves.append((new_row, new_col))
                    else:
                        break
                else:
                    break
        return moves

    def check_for_capture(self, piece, row, col, screen):
        directions = [(0, 1), (1, 0)]  # แนวนอนและแนวตั้ง
        captured = []
        
        for d in directions:
            line_pieces = []
            positions = []
            
            # เช็คไปทางขวา/ล่าง
            for i in range(1, ROWS):
                new_row = row + d[0] * i
                new_col = col + d[1] * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    current_piece = self.board[new_row][new_col]
                    if current_piece is None:
                        break
                    line_pieces.append(current_piece)
                    positions.append((new_row, new_col))
                else:
                    break

            # เช็คไปทางซ้าย/บน
            temp_pieces = []
            temp_positions = []
            for i in range(1, ROWS):
                new_row = row - d[0] * i
                new_col = col - d[1] * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    current_piece = self.board[new_row][new_col]
                    if current_piece is None:
                        break
                    temp_pieces.insert(0, current_piece)
                    temp_positions.insert(0, (new_row, new_col))
                else:
                    break

            # รวมหมากและตำแหน่งทั้งหมด
            all_pieces = temp_pieces + [piece] + line_pieces
            all_positions = temp_positions + [(row, col)] + positions

            # ถ้ามีหมากน้อยกว่า 3 ตัว ไม่สามารถจับได้
            if len(all_pieces) < 3:
                continue

            # รูปแบบที่ 1: หมากหนึ่งตัวหนีบเข้ากลางหมากสองตัวของฝ่ายตรงข้าม
            captured_type_1 = []
            for i in range(1, len(all_pieces) - 1):
                if (all_pieces[i-1].color == all_pieces[i+1].color and 
                    all_pieces[i-1].color != piece.color and 
                    all_pieces[i].color == piece.color):
                    captured_type_1.append(all_positions[i-1])
                    captured_type_1.append(all_positions[i+1])

            # รูปแบบที่ 2: หมากสองตัวหนีบทั้งซ้ายและขวาของหมากฝ่ายตรงข้าม
            captured_type_2 = []
            same_color_indices = []
            for i, p in enumerate(all_pieces):
                if p.color == piece.color:
                    same_color_indices.append(i)

            if len(same_color_indices) >= 2:
                for i in range(len(same_color_indices) - 1):
                    start_idx = same_color_indices[i]
                    end_idx = same_color_indices[i + 1]
                    if end_idx - start_idx > 1:
                        for idx in range(start_idx + 1, end_idx):
                            middle_piece = all_pieces[idx]
                            if middle_piece.color != piece.color:
                                captured_type_2.append(all_positions[idx])

            captured = captured_type_1 + captured_type_2

            captured_count = 0
            for pos_row, pos_col in set(captured):
                self.board[pos_row][pos_col] = None
                captured_count += 1

            if captured_count > 0:
                if piece.color == RED:
                    self.red_score += captured_count
                else:
                    self.blue_score += captured_count
                if screen is not None:
                    self.update(screen)
                pygame.display.flip()

    def select_piece(self, row, col):
        piece = self.board[row][col]
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        return False

    def change_turn(self):
        self.turn = BLUE if self.turn == RED else RED

    def update(self, screen):
        if screen is None:  # Skip updates if no screen
            return
        self.draw_squares(screen)
        self.draw_pieces(screen)
        self.draw_scores(screen)
        if self.selected_piece:
            self.draw_valid_moves(screen)
        pygame.display.update()

    def check_for_win(self, screen):
        red_pieces = sum(piece.color == RED for row in self.board for piece in row if piece)
        blue_pieces = sum(piece.color == BLUE for row in self.board for piece in row if piece)

        # รูปแบบที่ 1: หนีบกินหมากฝ่ายตรงข้ามจนหมด
        if red_pieces == 0:
            self.game_over = True
            self.display_winner(BLUE, screen)
        elif blue_pieces == 0:
            self.game_over = True
            self.display_winner(RED, screen)

        # รูปแบบที่ 2: ทำให้ผู้เล่นฝ่ายตรงข้ามจนมุม
        red_moves = sum(len(self.get_valid_moves(piece)) for row in self.board for piece in row if piece and piece.color == RED)
        blue_moves = sum(len(self.get_valid_moves(piece)) for row in self.board for piece in row if piece and piece.color == BLUE)

        if red_moves == 0:
            self.game_over = True
            self.display_winner(BLUE, screen)
        elif blue_moves == 0:
            self.game_over = True
            self.display_winner(RED, screen)

        # รูปแบบที่ 3: ทำให้ตัวหมากผู้เล่นฝ่ายตรงข้ามเหลือน้อยที่สุด
        if time.time() - self.start_time > 600:  # 10 นาที
            self.game_over = True
            if red_pieces > blue_pieces:
                self.display_winner(RED, screen)
            elif blue_pieces > red_pieces:
                self.display_winner(BLUE, screen)
            else:
                self.display_winner(None, screen)

    def display_winner(self, winner_color, screen):
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 74)
        if winner_color == RED:
            text = font.render('Red Wins!', True, RED)
        elif winner_color == BLUE:
            text = font.render('Blue Wins!', True, BLUE)
        else:
            text = font.render('Draw!', True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    def simulate_move(self, piece, new_row, new_col, screen):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        new_board.turn = self.turn
        new_board.red_score = self.red_score
        new_board.blue_score = self.blue_score
        new_board.selected_piece = None
        new_board.valid_moves = []
        new_board.game_over = self.game_over
        new_board.start_time = self.start_time
        new_board.font = self.font  # ไม่คัดลอกวัตถุ pygame.font.Font
        new_board.move_piece(new_board.board[piece.row][piece.col], new_row, new_col, screen)
        new_board.change_turn()  # เพิ่มการเปลี่ยนเทิร์นหลังจากที่จำลองการเดินหมากเสร็จ
        return new_board

    def can_capture(self, board, row, col, color):
        # จำลองการตรวจสอบการกินจาก check_for_capture
        return self.count_potential_captures(board, row, col, color) > 0

    def count_potential_captures(self, board, row, col, color):
        directions = [(0, 1), (1, 0)]
        total_captures = 0
        
        for d in directions:
            pieces_in_line = []
            for i in range(-7, 8):  # ตรวจสอบทั้งแถว/คอลัมน์
                new_row = row + d[0] * i
                new_col = col + d[1] * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    piece = board.board[new_row][new_col]
                    if piece:
                        pieces_in_line.append((piece.color, (new_row, new_col)))
            
            # ตรวจสอบรูปแบบการกิน
            if len(pieces_in_line) >= 3:
                for i in range(len(pieces_in_line)-2):
                    if (pieces_in_line[i][0] == pieces_in_line[i+2][0] != color and
                        pieces_in_line[i+1][0] != color):
                        total_captures += 1
        
        return total_captures

    def minimax(self, board, depth, is_maximizing, ai_color):
        if depth == 0:
            return self.evaluate_board(board, ai_color)
        
        scores = []
        current_color = ai_color if is_maximizing else (RED if ai_color == BLUE else BLUE)
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece and piece.color == current_color:
                    moves = board.get_valid_moves(piece)
                    for move_row, move_col in moves:
                        test_board = self.simulate_move(board, piece, move_row, move_col)
                        score = self.minimax(test_board, depth-1, not is_maximizing, ai_color)
                        scores.append(score)
        
        if not scores:
            return 0
        
        return max(scores) if is_maximizing else min(scores)

def initialize_board(difficulty):
    board = Board(difficulty)
    return board