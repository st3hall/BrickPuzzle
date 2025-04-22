import pygame

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
EMPTY = {"name": "EMPTY", "hex": "#525252", "abbr": "EM", "rgb": (82, 82, 82), "value": 0}  # Black for now
MATCH_MADE = {"name": "MATCH_MADE", "hex": "#FBFFB9", "abbr": "MM", "rgb": (251, 255, 185), "value": 10}  # White for now

COLORS_LIST = [Y, R, B, G, L, P,EMPTY]

#MATCH_MADE = pygame.draw.line(screen,)

CURSOR_DIMS = [(center_of_field_x + (BRICK_WIDTH/4), center_of_field_y),(center_of_field_x, center_of_field_y),(center_of_field_x, center_of_field_y + BRICK_HEIGHT),(center_of_field_x + (BRICK_WIDTH/4), center_of_field_y + BRICK_HEIGHT)]
