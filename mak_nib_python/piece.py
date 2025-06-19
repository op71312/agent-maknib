import pygame
from constants import SQUARE_SIZE

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                        (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                        self.row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                        SQUARE_SIZE // 3)