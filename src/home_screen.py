import pygame
from settings import*
import math

class HomeScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.game_started = False
        self.color_shift = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_started = True
                if event.key == pygame.K_ESCAPE:
                    quit()

    
    def update(self):
            self.color_shift += 1  # Increment to animate color
            if self.game_started:
                from game_screen import GameScreen
                self.manager.set_screen(GameScreen(self.manager))

    def draw(self, screen):
        # Create a smooth color transition using sine waves
        r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        screen.fill((r, g, b))

        font = pygame.font.Font(None, 74)
        text = font.render("Home Screen", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(text, text_rect)

        text = font.render("Press Escape to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        screen.blit(text, text_rect)