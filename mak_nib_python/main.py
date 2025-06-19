import pygame
import sys
import time
import asyncio
from board import Board, initialize_board
from ai import MakNibAI
from utils import draw_menu
from piece import Piece
from constants import WIDTH, HEIGHT, WHITE, BLACK, RED, BLUE, ROWS, COLS, SQUARE_SIZE

# Initialize pygame with hardware acceleration
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("หมากหนีบ (Mak Nib)")

async def main():
    clock = pygame.time.Clock()
    FPS = 60
    difficulty = None
    
    # Menu loop
    while difficulty is None:
        screen.fill(WHITE)  # เคลียร์หน้าจอก่อน
        easy_button, medium_button, hard_button = draw_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    difficulty = 'easy'
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = 'medium'
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = 'hard'
        
        await asyncio.sleep(0)  # ให้ asyncio ทำงานต่อได้
    
    # Initialize board with selected difficulty
    board = initialize_board(difficulty)
    board_background = pygame.Surface((WIDTH, HEIGHT))
    board.draw_squares(board_background)
    
    # Main game loop
    running = True
    last_update = time.time()
    UPDATE_INTERVAL = 1 / FPS
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == RED:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                
                if board.selected_piece:
                    if (row, col) in board.valid_moves:
                        board.move_piece(board.selected_piece, row, col, screen)
                        board.change_turn()
                    board.selected_piece = None
                    board.valid_moves = []
                else:
                    board.select_piece(row, col)
        
        if board.turn == BLUE and not board.game_over:
            start_time = time.time()
            ai_move = board.ai.get_move(board, BLUE, screen)
            print(f"Bot thinking time: {time.time() - start_time:.2f} seconds")
            
            if ai_move:
                piece, (row, col) = ai_move
                board.move_piece(piece, row, col, screen)
                board.change_turn()
        
        if current_time - last_update >= UPDATE_INTERVAL:
            screen.blit(board_background, (0, 0))
            board.draw_pieces(screen)
            if board.selected_piece:
                board.draw_valid_moves(screen)
            board.draw_scores(screen)
            board.check_for_win(screen)
            pygame.display.flip()
            last_update = current_time
        
        clock.tick(FPS)
        await asyncio.sleep(0)  # ให้ asyncio ทำงานต่อได้
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
