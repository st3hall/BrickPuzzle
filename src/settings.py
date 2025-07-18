import pygame
import uuid
import json
import os
from dataclasses import dataclass


#Grid size
COLUMNS = 6
ROWS = 14
CELL_SIZE = 40   #formerly Brick Width
#Brick shape
BRICK_WIDTH = 40
BRICK_HEIGHT = 40
OUTLINE_WIDTH = 1
DEFAULT_FONT = 'arialblack'

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

BACK_GROUND = (64, 64, 64) #Dark Gray

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
        
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        # Create the surface with alpha
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT], pygame.SRCALPHA)
        # Fill with base color
        base_color = brick_data["rgb"]
        self.image.fill(base_color)
        # Store original color
        self.original_color = base_color
        # Create a darker version of the color for the outline
        darker_color = tuple(max(0, c - 40) for c in base_color)
        outline_color = tuple(max(0, c - 120) for c in base_color)
        # Draw the outline
        pygame.draw.rect(self.image, outline_color, self.image.get_rect(), width=1)
        pygame.draw.rect(self.image, darker_color, self.image.get_rect().inflate(-2,-2), width=2)
        
        #These are the starting positions for the bricks, init_x,y are 0,0 from settings set up.
        pos_y = init_y + row * BRICK_HEIGHT 
        pos_x = init_x + column * BRICK_WIDTH 

        #This is just creating the rect for the brick.
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        
        #This stores the previous position of the brick, used for animation.
        self.previous_y = self.rect.y

        #This just creates a tartget position for the brick to move to. This gets used in the update method to move the brick.
        self.target_y = 0
        self.target_x = 0
        
        #Movement parameters
        self.fall_speed = 10
        self.move_speed = 8
        self.death_timer = 0
        self.scale_factor = 1.0
        self.change_color_timer = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.scroll_offset = 0
        
        self.is_dying = False
        self.is_match = False
        self.is_falling = False
        self.is_swapping = False
        self.is_scrolling = False

    #This is how the brick moves to a new position, it sets the row and column and then calculates the target position based on the init_x,y.        
    def move_to_index(self, new_row, new_col):
        self.row = new_row
        self.column = new_col
        #These targets are used in the update method to move the brick.
        self.target_x = init_x + new_col * BRICK_WIDTH
        self.target_y = init_y + (new_row * BRICK_HEIGHT) - self.scroll_offset

    def start_dying(self):
        self.is_dying = True
        self.death_timer = 8  # frames until the brick is removed
        self.scale_factor = 1.0  # used for pop animation
    
    def match_made(self, color):
        self.is_match = True
        self.image.fill(color["rgb"])
        self.change_color_timer = 8
     
    def draw(self, offset, surface):
        # surface.blit(self.image, self.rect)
        translated_rect = self.rect.copy()
        translated_rect.topleft = (self.rect.left, self.rect.top + offset)
        surface.blit(self.image, translated_rect)

    def is_animating(self):
        animating = self.is_dying or self.is_match or self.is_moving()
        #print(f"Moving: Falling:{self.is_falling}, Swapping:{self.is_swapping}")
        #print(f"Animating: {animating}")
        return animating
    
    def is_moving(self):
        #self.is_swapping = self.rect.x != self.target_x
        self.is_falling = self.rect.y < self.target_y #not if moving upward
        
        return self.is_swapping or self.is_falling 
     
    def is_in_match_state(self):
        return self.is_match

    def is_in_dying_state(self):
        return self.is_dying
    
    def update(self):
        dt = self.clock.tick(60)/1000.0
        if self.is_match:
            if self.change_color_timer > 0:
                self.change_color_timer -= 1
                if self.change_color_timer == 0:
                    self.image.fill(self.original_color)
                    self.is_match = False
    
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
                self.is_dying = False
                   
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

            #Once x is aligned, handle vertical movement
            if self.rect.x == self.target_x:               
                #if current.y is larger than target.y, moving up
                    
                if self.rect.y > self.target_y:
                    print(f"Moving Up sprite: {self.row}, {self.column}")
                    self.rect.y -= self.scroll_offset #Velociy is raise rate
                    #After moving up is done, reset vel to 0
                    if self.rect.y < self.target_y:
                        self.rect.y = self.target_y

                #Falling, but with the END target
                #if current.y is less than target.y, moving down
                if self.rect.y < self.target_y:
                    self.velocity_y += self.gravity
                    self.rect.y += self.velocity_y

                    # Clamp to final target
                    if self.rect.y > self.target_y:
                        self.rect.y = max(self.rect.y-self.velocity_y, self.target_y)
                        if self.rect.y == self.target_y:
                            self.velocity_y = 0 



class Screen:
    def __init__(self, manager):
        self.manager = manager
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.score = 0
        self.player_data = PlayerData()
        self.bricks = pygame.sprite.Group()
        self.brick_data = COLORS_LIST
        self.current_brick = None
        self.next_brick = None
        self.score_text = None
        self.preview_text = None
        self.font = pygame.font.SysFont(DEFAULT_FONT, 36)
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


try:
    import sys
    if sys.platform == "emscripten":
        from js import window
        using_browser = True
    else:
        using_browser = False
        window = None
except ImportError:
    using_browser = False
    window = None

class PlayerData:
    def __init__(self):
        self.high_score = 0
        self.puzzles = []
        self.load()

    def load(self):
        if using_browser:
            data_str = window.localStorage.getItem("PlayerData")
        else:
            try:
                with open("player_data.json", "r") as f:
                    data_str = f.read()
            except FileNotFoundError:
                data_str = None

        if data_str:
            data = json.loads(data_str)
            self.high_score = data.get("highScore", 0)
            self.puzzles = data.get("puzzles", [])
        else:
            self.high_score = 0
            self.puzzles = []

    def save(self):
        data = {
            "highScore": self.high_score,
            "puzzles": self.puzzles
        }
        data_str = json.dumps(data)

        if using_browser:
            window.localStorage.setItem("PlayerData", data_str)
        else:
            with open("player_data.json", "w") as f:
                f.write(data_str)

    def update_score(self, score):
        if score > self.high_score:
            self.high_score = score
            self.save()

    def complete_puzzle(self, puzzle_id):
        if puzzle_id not in self.puzzles:
            self.puzzles.append(puzzle_id)
            self.save()

    def reset(self):
        self.high_score = 0
        self.puzzles = []
        self.save()



# # Try to import localStorage from the browser (Pyodide/Pygbag)
# try:
#     from js import localStorage
#     using_browser = True
# except ImportError:
#     using_browser = False
#     localStorage = None  # Optional: define a mock or file-based fallback

# class PlayerData:
#     def __init__(self):
#         self.high_score = 0
#         self.puzzles = []
#         self.load()

#     def load(self):
#         if using_browser:
#             data_str = localStorage.getItem("PlayerData")
#         else:
#             try:
#                 with open("player_data.json", "r") as f:
#                     data_str = f.read()
#             except FileNotFoundError:
#                 data_str = None

#         if data_str:
#             data = json.loads(data_str)
#             self.high_score = data.get("highScore", 0)
#             self.puzzles = data.get("puzzles", [])
#         else:
#             self.high_score = 0
#             self.puzzles = []

#     def save(self):
#         data = {
#             "highScore": self.high_score,
#             "puzzles": self.puzzles
#         }
#         data_str = json.dumps(data)

#         if using_browser:
#             localStorage.setItem("PlayerData", data_str)
#         else:
#             with open("player_data.json", "w") as f:
#                 f.write(data_str)

#     def update_score(self, score):
#         if score > self.high_score:
#             self.high_score = score
#             self.save()

#     def complete_puzzle(self, puzzle_id):
#         if puzzle_id not in self.puzzles:
#             self.puzzles.append(puzzle_id)
#             self.save()

#     def reset(self):
#         self.high_score = 0
#         self.puzzles = []
#         self.save()



# class PlayerData:
#     def __init__(self):
#         self.high_score = 0
#         self.puzzles = []
#         self.load()

#     def load(self):
#         data_str = localStorage.getItem("PlayerData")
#         if data_str:
#             data = json.loads(data_str)
#             self.high_score = data.get("highScore", 0)
#             self.puzzles = data.get("puzzles", [])
#         else:
#             self.high_score = 0
#             self.puzzles = []

#     def save(self):
#         data = {
#             "highScore": self.high_score,
#             "puzzles": self.puzzles
#         }
#         localStorage.setItem("PlayerData", json.dumps(data))

#     def update_score(self, score):
#         if score > self.high_score:
#             self.high_score = score
#             self.save()

#     def complete_puzzle(self, puzzle_id):
#         if puzzle_id not in self.puzzles:
#             self.puzzles.append(puzzle_id)
#             self.save()

#     def reset(self):
#         self.high_score = 0
#         self.puzzles = []
#         self.save()


#Local non online storage testing
# class PlayerData:
#     def __init__(self, storage=None):
#         self.localStorage = storage
#         self.high_score = 0
#         self.puzzles = []
#         self.load()

#     def load(self):
#         data_str = self.localStorage.getItem("PlayerData")
#         if data_str:
#             data = json.loads(data_str)
#             self.high_score = data.get("highScore", 0)
#             self.puzzles = data.get("puzzles", [])
#         else:
#             self.high_score = 0
#             self.puzzles = []

#     def save(self):
#         data = {
#             "highScore": self.high_score,
#             "puzzles": self.puzzles
#         }
#         self.localStorage.setItem("PlayerData", json.dumps(data))

#     def update_score(self, score):
#         if score > self.high_score:
#             self.high_score = score
#             self.save()

#     def complete_puzzle(self, puzzle_id):
#         if puzzle_id not in self.puzzles:
#             self.puzzles.append(puzzle_id)
#             self.save()

#     def reset(self):
#         self.high_score = 0
#         self.puzzles = []
#         self.save()


# class LocalStorage:
#     def __init__(self, filename="local_storage.json"):
#         self.filename = filename
#         self._load()

#     def _load(self):
#         if os.path.exists(self.filename):
#             with open(self.filename, "r") as f:
#                 self.store = json.load(f)
#         else:
#             self.store = {}

#     def _save(self):
#         with open(self.filename, "w") as f:
#             json.dump(self.store, f)

#     def getItem(self, key):
#         return self.store.get(key)

#     def setItem(self, key, value):
#         self.store[key] = value
#         self._save()

#     def removeItem(self, key):
#         if key in self.store:
#             del self.store[key]
#             self._save()
