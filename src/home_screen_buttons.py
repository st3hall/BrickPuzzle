import pygame
from settings import*
import math

class HomeScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.color_shift = 0

        font_small = pygame.font.SysFont(DEFAULT_FONT, 24)
        button_width = 300
        button_height = 50
        center_x = (WINDOW_WIDTH - button_width) // 2
        button_y_start = 200
        

        self.buttons = [
            Button((center_x, button_y_start, button_width, button_height), "Start Endless Mode", self.start_game, font_small, B['rgb'], tuple(min(255, c + 30) for c in B['rgb'])),
            Button((center_x, button_y_start + 70, button_width, button_height), "Start Puzzle Mode", self.start_puzzle_select, font_small, B['rgb'], tuple(min(255, c + 30) for c in B['rgb'])),
            Button((center_x, button_y_start + 140, button_width, button_height), "Quit", self.quit_game, font_small, R['rgb'], tuple(min(255, c + 30) for c in R['rgb'])),
            Button((center_x, button_y_start + 240, button_width, button_height), "How To Play", self.how_to, font_small, R['rgb'], tuple(min(255, c + 30) for c in R['rgb']))
        ]

    def start_game(self):
        from game_screen import GameScreen
        self.manager.set_screen(GameScreen(self.manager))
    
    def start_puzzle_select(self):
        from puzzle_select_screen import PuzzleSelectScreen
        self.manager.set_screen(PuzzleSelectScreen(self.manager))
    
    def how_to(self):
        from how_to_screen import HowToScreen
        self.manager.set_screen(HowToScreen(self.manager))

    # def start_puzzle(self):
    #     from puzzle_screen import PuzzleScreen
    #     self.manager.set_screen(PuzzleScreen(self.manager, puzzle_id))

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

    def draw(self, screen):
        # r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        # g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        # b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        # screen.fill((r, g, b))

        screen.fill((BACK_GROUND))

        title_font = pygame.font.SysFont(DEFAULT_FONT, 60)
        title_text = title_font.render("Bricks", True, L['rgb'])
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
        text_surf = self.font.render(self.text, True, L['rgb'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()
