import pygame
from settings import*
from game_screen import GameScreen
import math

class PauseScreen(Screen):
    def __init__(self, manager):
        self.manager = manager
        self.game_paused = True
        self.color_shift = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from home_screen import HomeScreen
                    self.manager.set_screen(HomeScreen(self.manager))
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_paused = False
    
    def update(self):
        self.color_shift += 1
        if not self.game_paused:         
            self.manager.set_screen(self.manager.previous_screen)

    def draw(self, screen):  
        r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        screen.fill((r, g, b))    

        font = pygame.font.Font(None, 74)
        text = font.render("Pause Screen", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect)
        
        font = pygame.font.Font(None, 36)
        text = font.render("Press Escape to Home", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect.move(0, 50))

        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect.move(0, 100))
