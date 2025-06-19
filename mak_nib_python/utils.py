import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, RED, BLUE

def draw_menu(screen):
    # วาดพื้นหลังสีขาว
    screen.fill(WHITE)
    
    # สร้างฟอนต์
    font = pygame.font.SysFont(None, 74)
    
    # วาดข้อความหัวเรื่อง
    title_text = font.render('Select Difficulty', True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # สร้างปุ่มด้วยสี่เหลี่ยมผืนผ้า
    button_width = 200
    button_height = 50
    spacing = 20
    
    easy_button = pygame.Rect((WIDTH - button_width) // 2, 
                             HEIGHT // 2 - button_height - spacing,
                             button_width, button_height)
    medium_button = pygame.Rect((WIDTH - button_width) // 2,
                               HEIGHT // 2,
                               button_width, button_height)
    hard_button = pygame.Rect((WIDTH - button_width) // 2,
                             HEIGHT // 2 + button_height + spacing,
                             button_width, button_height)
    
    # วาดปุ่ม
    for button in [easy_button, medium_button, hard_button]:
        pygame.draw.rect(screen, RED, button)
        pygame.draw.rect(screen, BLACK, button, 2)  # เพิ่มเส้นขอบ
    
    # วาดข้อความบนปุ่ม
    button_font = pygame.font.SysFont(None, 50)
    
    easy_text = button_font.render('Easy', True, WHITE)
    medium_text = button_font.render('Medium', True, WHITE)
    hard_text = button_font.render('Hard', True, WHITE)
    
    for button, text in [(easy_button, easy_text),
                        (medium_button, medium_text),
                        (hard_button, hard_text)]:
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)
    
    return easy_button, medium_button, hard_button