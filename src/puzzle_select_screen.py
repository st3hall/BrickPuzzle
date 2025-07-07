import pygame
import math
from settings import *  
from puzzle_grids import *

class PuzzleSelectScreen(Screen):
    def __init__(self, manager, puzzles_per_row=6):
        super().__init__(manager)
        self.color_shift = 0
        self.total_puzzles = len(puzzle_dict)
        self.puzzles_per_row = puzzles_per_row
        self.buttons = []

        font_small = pygame.font.SysFont(DEFAULT_FONT, 24)
        button_width = 50
        button_height = 50
        padding = 10
     
        total_width = self.puzzles_per_row * (button_width + padding) - padding
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 150

        for i in range(self.total_puzzles):
            row = i // self.puzzles_per_row
            col = i % self.puzzles_per_row
            x = start_x + col * (button_width + padding)
            y = start_y + row * (button_height + padding)
            puzzle_id = i + 1
            self.buttons.append(
                Button(
                    (x, y, button_width, button_height),
                    f"{puzzle_id}",
                    lambda pid=puzzle_id: self.load_puzzle(pid),
                    font_small,
                    B['rgb'],
                    tuple(min(255, c + 30) for c in B['rgb'])
                )
            )
        
        center_x = WINDOW_WIDTH // 2

        self.buttons.append(
            Button(
                ((center_x - 50) , 520, 100, button_height),
                  "Back", 
                  self.return_home, 
                  font_small, 
                  G['rgb'], 
                  tuple(min(255, c + 30) for c in G['rgb'])
            )
        )
           

    def return_home(self):
        from home_screen_buttons import HomeScreen
        self.manager.set_screen(HomeScreen(self.manager))

    def load_puzzle(self, puzzle_id):
        print(f"Puzzle #: {puzzle_id}")
        from puzzle_screen import PuzzleScreen
        self.manager.set_screen(PuzzleScreen(self.manager, puzzle_id))

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

        title_font = pygame.font.SysFont(DEFAULT_FONT, 48)
        title_text = title_font.render("Select a Puzzle", True, L['rgb'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
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
