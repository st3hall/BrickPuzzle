import pygame
from settings import*
from game_screen import GameScreen
import math

class PauseScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.color_shift = 0
        self.game_paused = True

        font_small = pygame.font.Font(None, 36)
        button_width = 300
        button_height = 50
        center_x = (WINDOW_WIDTH - button_width) // 2
        button_y_start = 200
        

        self.buttons = [
            Button((center_x, button_y_start, button_width, button_height), "Return Home", self.return_home, font_small, (0, 100, 200), (0, 150, 255)),
            Button((center_x, button_y_start + 70, button_width, button_height), "Puzzle Select", self.start_puzzle_select, font_small, (0, 100, 200), (0, 150, 255)),
            Button((center_x, button_y_start + 140, button_width, button_height), "Resume", self.resume_game, font_small, (200, 0, 0), (255, 0, 0)),
            Button((center_x, button_y_start + 210, button_width, button_height), "Quit", self.quit_game, font_small, (200, 0, 0), (255, 0, 0))
        ]
    
    def resume_game(self):
        self.game_paused = False

    def return_home(self):
        from home_screen_buttons import HomeScreen
        self.manager.set_screen(HomeScreen(self.manager))
    
    def start_puzzle_select(self):
        from puzzle_select_screen import PuzzleSelectScreen
        self.manager.set_screen(PuzzleSelectScreen(self.manager))

    def quit_game(self):
        pygame.quit()
        exit()

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(event.pos)

    def update(self):
        self.color_shift += 1
        if not self.game_paused:         
            self.manager.set_screen(self.manager.previous_screen)

    def draw(self, screen):
        r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        screen.fill((r, g, b))

        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Bricks", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        for button in self.buttons:
            button.draw(screen)

class Button:
    def __init__(self, rect, text, action, font, base_color, hover_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()

    # def handle_events(self, events):
    #     for event in events:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 from home_screen import HomeScreen
    #                 self.manager.set_screen(HomeScreen(self.manager))
            
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RETURN:
    #                 self.game_paused = False

