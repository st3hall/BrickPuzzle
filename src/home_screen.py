import pygame
from settings import*
import math
from puzzle_grids import*

class HomeScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.game_screen_started = False
        self.puzzle_screen_started = False
        self.color_shift = 0
        self.selected_option = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_screen_started = True
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_LSHIFT:
                    self.puzzle_screen_started = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.selected_option = handle_mouse_click(event.pos)

    
    def update(self):
            self.color_shift += 1  # Increment to animate color
            if self.game_screen_started:
                from game_screen import GameScreen
                self.manager.set_screen(GameScreen(self.manager))
            
            if self.puzzle_screen_started :
                from puzzle_screen import PuzzleScreen
                self.manager.set_screen(PuzzleScreen(self.manager))

    def draw(self, screen):
        # Create a smooth color transition using sine waves
        r = int((math.sin(self.color_shift * 0.02) + 1) * 127.5)
        g = int((math.sin(self.color_shift * 0.02 + 2) + 1) * 127.5)
        b = int((math.sin(self.color_shift * 0.02 + 4) + 1) * 127.5)
        screen.fill((r, g, b))

        font = pygame.font.SysFont(DEFAULT_FONT, 74)
        text = font.render("Home Screen", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont(DEFAULT_FONT, 36)
        text = font.render("Press Enter to Start Endless Mode", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(text, text_rect)

        text = font.render("Press L Shift to Start Puzzle Mode", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        screen.blit(text, text_rect)

        text = font.render("Press Escape to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        screen.blit(text, text_rect)
        
        draw_dropdown(screen)





# Dropdown variables
options = [str(i) for i in range(1, len(puzzle_dict) + 1)]
option_height = 15
option_width = 100
dropdown_rect = pygame.Rect(WINDOW_WIDTH // 2 - option_width/2, WINDOW_HEIGHT // 2 +250, option_width, 20)
dropdown_open = False
selected_option = None

def draw_dropdown(screen):
    font = pygame.font.SysFont(None, 14)
    pygame.draw.rect(screen, DG['rgb'], dropdown_rect)
    text = font.render(selected_option if selected_option else "Select a level", True, BK['rgb'])
    screen.blit(text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

    if dropdown_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(
                dropdown_rect.x,
                dropdown_rect.y - (i + 1) * option_height,  # ✅ expanding upward
                dropdown_rect.width,
                option_height
            )

            pygame.draw.rect(screen, DG['rgb'] if option == selected_option else W['rgb'], option_rect)
            text_surface = font.render(option, True, BK['rgb'])
            text_rect = text_surface.get_rect(center=option_rect.center)
            screen.blit(text_surface, text_rect)


def handle_mouse_click(pos):
    global dropdown_open, selected_option
    if dropdown_rect.collidepoint(pos):
        dropdown_open = not dropdown_open
    elif dropdown_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(
                dropdown_rect.x,
                dropdown_rect.y - (i + 1) * option_height,
                dropdown_rect.width,
                option_height
            )
            if option_rect.collidepoint(pos):
                selected_option = option
                dropdown_open = False
                break
        else:
            dropdown_open = False
    return selected_option
