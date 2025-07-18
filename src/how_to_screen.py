import pygame
from settings import*
from game_screen import GameScreen
import math

class HowToScreen(Screen):
    def __init__(self, manager, player_data):
        super().__init__(manager)
        self.color_shift = 0
        self.game_paused = True
        self.player_data = player_data

        font_small = pygame.font.SysFont(DEFAULT_FONT, 24)
        button_width = 300
        button_height = 50
        center_x = (WINDOW_WIDTH - button_width) // 2
        button_y_start = 200

        self.buttons = [
            Button((center_x, button_y_start + 240, button_width, button_height), "Back", self.return_home, font_small, G['rgb'], tuple(min(255, c + 30) for c in G['rgb'])),
            Button((center_x, button_y_start + 310, button_width, button_height), "Reset Data", self.reset_data, font_small, R['rgb'], tuple(min(255, c + 30) for c in R['rgb']))
        ]
    
    def resume_game(self):
        self.game_paused = False

    def return_home(self):
        from home_screen_buttons import HomeScreen
        self.manager.set_screen(HomeScreen(self.manager, self.player_data))
    
    def start_puzzle_select(self):
        from puzzle_select_screen import PuzzleSelectScreen
        self.manager.set_screen(PuzzleSelectScreen(self.manager, self.player_data))

    def quit_game(self):
        pygame.quit()
        exit()

    def reset_data(self):
        self.player_data.reset()
        print("Data Reset")

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
        # r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        # g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        # b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        # screen.fill((r, g, b))
        screen.fill((BACK_GROUND))

        title_font = pygame.font.SysFont(DEFAULT_FONT, 60)
        title_text = title_font.render("How To Play", True, L['rgb'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))

        credits_font = pygame.font.SysFont(DEFAULT_FONT, 12)
        credits_text = credits_font.render("Steven Hall 2025 | stevenhall1986@yahoo.com", True, L['rgb'])
        credits_rect = credits_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT -60))

        # Body text lines
        body_font = pygame.font.SysFont(DEFAULT_FONT, 14)
        instructions = [
            "Move with W, A, S, D.",
            "You can only swap bricks horizontally.",
            "W or ↑ or 8 : UP"  , 
            "S or ↓ or 5 : DOWN", 
            "A or ← or 4 : LEFT", 
            "D or → or 6 : RIGHT",
            "SPACEBAR - SWAP",
            "ESC - Pause"
        ]

        # Starting position for body text (left-aligned)
        body_x = WINDOW_WIDTH //2
        body_y = title_rect.bottom + 20  # space below the title

        # Render and position each line
        for line in instructions:
            line_surface = body_font.render(line, True, L['rgb'])
            line_rect = line_surface.get_rect(center=(body_x, body_y))
            screen.blit(line_surface, line_rect)
            body_y += line_surface.get_height() + 10  # spacing between lines

        # Draw the title last (or first, depending on layering)
        screen.blit(title_text, title_rect)
        screen.blit(credits_text, credits_rect)

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

    # def handle_events(self, events):
    #     for event in events:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 from home_screen import HomeScreen
    #                 self.manager.set_screen(HomeScreen(self.manager))
            
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RETURN:
    #                 self.game_paused = False

