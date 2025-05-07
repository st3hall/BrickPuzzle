import pygame
import uuid
import json

#Grid size
COLUMNS = 6
ROWS = 14
CELL_SIZE = 40   #formerly Brick Width
#Brick shape
BRICK_WIDTH = 40
BRICK_HEIGHT = 40
OUTLINE_WIDTH = 1

GAME_WIDTH = COLUMNS * CELL_SIZE
GAME_HEIGHT = ROWS * CELL_SIZE

def center(width, height):
    y = height / 2 
    x = width / 2
    return x,y

center_of_field_x, center_of_field_y = center(GAME_WIDTH, GAME_HEIGHT)

#Side bar size
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

#Window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

center_of_window_x, center_of_window_y, = center(WINDOW_WIDTH, WINDOW_HEIGHT)

init_x = center_of_window_x - (BRICK_WIDTH * COLUMNS / 2)
init_y = center_of_window_y - (BRICK_HEIGHT * ROWS / 2)


#Game inital speed settings
START_SPEED = 800
MOVE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

#Colors

Y = {"name": "YELLOW", "hex": "#fed86dff", "abbr": "Y", "rgb": (254, 216, 109), "value": 1}
R = {"name": "RED", "hex": "#de6568ff", "abbr": "R", "rgb": (222, 101, 104), "value": 2}
B = {"name": "BLUE", "hex": "#6f9fe9ff", "abbr": "B", "rgb": (111, 159, 233), "value": 3}
G = {"name": "GREEN", "hex": "#94c47fff", "abbr": "G", "rgb": (148, 196, 127), "value": 4}
L = {"name": "LIGHT_GRAY", "hex": "#d0e0e3ff", "abbr": "L", "rgb": (208, 224, 227), "value": 5}
P = {"name": "PURPLE", "hex": "#8e7dc1ff", "abbr": "P", "rgb": (142, 125, 193), "value": 6}
W = {"name": "WHITE", "hex": "#ffffffff", "abbr": "W", "rgb": (255, 255, 255), "value": 7}
DG = {"name": "DARK_GREY", "hex": "#595959ff", "abbr": "DG", "rgb": (89, 89, 89), "value": 8}
BK = {"name": "BLACK", "hex": "#000000ff", "abbr": "BK", "rgb": (0, 0, 0), "value": 9}
EMPTY = {"name": "EMPTY", "hex": "#525252", "abbr": "EM", "rgb": (82, 82, 82, 50), "value": 0}  # Black for now
MATCH_MADE = {"name": "MATCH_MADE", "hex": "#FBFFB9", "abbr": "MM", "rgb": (251, 255, 185), "value": 10}  # White for now

COLORS_LIST = [Y, R, B, G, L, P,EMPTY]

#MATCH_MADE = pygame.draw.line(screen,)

CURSOR_DIMS = [(center_of_field_x + (BRICK_WIDTH/4), center_of_field_y),(center_of_field_x, center_of_field_y),(center_of_field_x, center_of_field_y + BRICK_HEIGHT),(center_of_field_x + (BRICK_WIDTH/4), center_of_field_y + BRICK_HEIGHT)]

class Brick(pygame.sprite.Sprite):
    def __init__(self, brick_data, row, column):
        super().__init__()
        self.brick_data = brick_data
        self.row = row
        self.column = column
        self.id = uuid.uuid4()

        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT], pygame.SRCALPHA)
        self.image.fill(brick_data["rgb"])
        self.original_color = brick_data["rgb"]

        pos_y = init_y + row * BRICK_HEIGHT #init_x,y is 0,0
        pos_x = init_x + column * BRICK_WIDTH

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

        self.target_y = pos_y
        self.target_x = pos_x
        
        self.fall_speed = 8
        self.move_speed = 8

        self.is_dying = False
        self.death_timer = 0
        self.scale_factor = 1.0
        self.is_match = False
        self.change_color_timer = 0
            
    def move_to_index(self, new_row, new_col):
        self.row = new_row
        self.column = new_col
        self.target_x = init_x + new_col * BRICK_WIDTH
        self.target_y = init_y + new_row * BRICK_HEIGHT

    def start_dying(self):
        self.is_dying = True
        self.death_timer = 15  # frames until the brick is removed
        self.scale_factor = 1.0  # used for pop animation
    
    def match_made(self, color):
        self.is_match = True
        self.image.fill(color["rgb"])
        self.change_color_timer = 15
     
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_in_match_state(self):
        return self.is_match

    def is_in_dying_state(self):
        return self.is_dying
    
    def update(self):
        if self.is_match:
            if self.change_color_timer > 0:
                self.change_color_timer -= 1
                if self.change_color_timer == 0:
                    self.image.fill(self.original_color)
    
        if self.is_dying:
            self.death_timer -= 1
            self.scale_factor -= 0.05
            if self.scale_factor < 0:
                self.scale_factor = 0

            w = int(BRICK_WIDTH * self.scale_factor)
            h = int(BRICK_HEIGHT * self.scale_factor)
            if w <= 0 or h <= 0:
                w, h = 1, 1  # prevent crash

            old_center = self.rect.center
            self.image = pygame.transform.scale(
                pygame.Surface([w, h], pygame.SRCALPHA), (w, h)
            )
            self.image.fill(self.brick_data["rgb"])
            self.rect = self.image.get_rect(center=old_center)

            if self.death_timer <= 0:
                self.kill()  # Remove from all groups
                
        else:
            # Move in the x direction first
            if self.rect.x < self.target_x:
                self.rect.x += self.move_speed
                if self.rect.x > self.target_x:
                    self.rect.x = self.target_x
            elif self.rect.x > self.target_x:
                self.rect.x -= self.move_speed
                if self.rect.x < self.target_x:
                    self.rect.x = self.target_x

            # Only move in the y direction if the x position is correct
            if self.rect.x == self.target_x:
                if self.rect.y < self.target_y:
                    self.rect.y += self.fall_speed
                    if self.rect.y > self.target_y:
                        self.rect.y = self.target_y
                elif self.rect.y > self.target_y:
                    self.rect.y -= self.fall_speed
                    if self.rect.y < self.target_y:
                        self.rect.y = self.target_y



