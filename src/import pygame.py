import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))

# Define constants for brick dimensions
BRICK_WIDTH = 40
BRICK_HEIGHT = 40

# Define the initial player position
player_pos = pygame.Vector2(400, 300)  # Starting at the center of the screen

# Define the clock for managing frame rate
clock = pygame.time.Clock()

def render_grid(field):
    # Placeholder function for rendering the grid
    pass

def draw_cursor(pos_x, pos_y, width, height):
    points_left = [(pos_x, pos_y), (pos_x - width, pos_y), (pos_x - width, pos_y + height), (pos_x, pos_y + height)]
    points_right = [(pos_x, pos_y), (pos_x + width, pos_y), (pos_x + width, pos_y + height), (pos_x, pos_y + height)]
    pygame.draw.lines(screen, DARK_GREY, True, points_left, 4)
    pygame.draw.lines(screen, DARK_GREY, True, points_right, 4)

def main():
    run = True
    move_delay = 200  # Delay in milliseconds
    last_move_time = pygame.time.get_ticks()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        screen.fill("black")
                
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > move_delay:
            if keys[pygame.K_w]:
                player_pos.y -= BRICK_HEIGHT
                last_move_time = current_time
            if keys[pygame.K_s]:
                player_pos.y += BRICK_HEIGHT
                last_move_time = current_time
            if keys[pygame.K_a]:
                player_pos.x -= BRICK_WIDTH
                last_move_time = current_time
            if keys[pygame.K_d]:
                player_pos.x += BRICK_WIDTH
                last_move_time = current_time

        render_grid(field_grid)
        draw_cursor(player_pos.x, player_pos.y, BRICK_WIDTH, BRICK_HEIGHT)
        pygame.display.flip()      
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

pygame.quit()


import random


YELLOW = {"hex": "#fed86dff", "abbr": "Y"}
RED = {"hex": "#de6568ff", "abbr": "R"}
BLUE = {"hex": "#6f9fe9ff", "abbr": "B"}
GREEN = {"hex": "#94c47fff", "abbr": "G"}
LIGHT_GRAY = {"hex": "#d0e0e3ff", "abbr": "LG"}
PURPLE = {"hex": "#8e7dc1ff", "abbr": "P"}
WHITE = {"hex": "#ffffffff", "abbr": "W"}
DARK_GREY = {"hex": "#595959", "abbr": "DG"}




COLORS_LIST = [YELLOW, RED, BLUE, GREEN, LIGHT_GRAY, PURPLE

rows = 5  # Example number of rows
columns = 5  # Example number of columns

temp = []
field = []

for row in range(rows):
    temp_row = []
    field_row = []
    for column in range(columns):
        brick_color = COLORS_LIST[random.randrange(0, len(COLORS_LIST))]
        temp_row.append(brick_color)
        field_row.append(brick_color)
    temp.append(temp_row)
    field.append(field_row)

# Convert temp array to abbreviated form
temp_abbreviated = []
for row in temp:
    temp_row_abbreviated = [color_dict[color] for color in row]
    temp_abbreviated.append(temp_row_abbreviated)

# Print the abbreviated array
for row in temp_abbreviated:
    print(row)


import random

rows = 5  # Example number of rows
columns = 5  # Example number of columns

temp = []
field = []

for row in range(rows):
    temp_row = []
    field_row = []
    for column in range(columns):
        brick_color = COLORS_LIST[random.randrange(0, len(COLORS_LIST))]
        temp_row.append(brick_color["abbr"])
        field_row.append(brick_color["abbr"])
    temp.append(temp_row)
    field.append(field_row)

# Print the abbreviated array
for row in temp:
    print(row)

# Define your color dictionary
colors = {
    "#fed86dff": "Y",
    "#de6568ff": "R",
    "#6f9fe9ff": "B",
    "#94c47fff": "G",
    "#d0e0e3ff": "LG",
    "#8e7dc1ff": "P",
    "#ffffffff": "W",
    "#595959": "DG"
}

def get_color_abbr(hex_code):
    return colors.get(hex_code, "Unknown")

def cursor_input(field, cursor_index_x, cursor_index_y):
    cursor_L_hex = field[int(cursor_index_y)][int(cursor_index_x) - 1]
    cursor_R_hex = field[int(cursor_index_y)][int(cursor_index_x)]
    
    cursor_L_abbr = get_color_abbr(cursor_L_hex)
    cursor_R_abbr = get_color_abbr(cursor_R_hex)
    
    return cursor_L_abbr, cursor_R_abbr

def another_function(field, cursor_index_x, cursor_index_y):
    cursor_L_abbr, cursor_R_abbr = cursor_input(field, cursor_index_x, cursor_index_y)
    print(f"Cursor Left: {cursor_L_abbr}, Cursor Right: {cursor_R_abbr}")

# Example usage
field = [
    ["#fed86dff", "#de6568ff", "#6f9fe9ff"],
    ["#94c47fff", "#d0e0e3ff", "#8e7dc1ff"],
    ["#ffffffff", "#595959", "#fed86dff"]
]
cursor_index_x = 1
cursor_index_y = 1
another_function(field, cursor_index_x, cursor_index_y)

def seek_for_empty(field, temp, rows, columns):
    for row in range(1, rows):
        for column in range(columns):
            if field[row][column] == "":
                for r in range(row, 0, -1):
                    temp[r][column] = field[r-1][column]
                temp[0][column] = ""
    return temp

[['', '', '', '', '', ''], 
 [{...}, {...}, {...}, {...}, {...}, {...}], 
 [{...}, {...}, {...}, {...}, {...}, {...}], 
 [{...}, {...}, 'W', 'W', 'W', {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}]]

 
 
 


def seek_for_empty(field, temp, rows, columns):
    for row in range(1, rows):
        for column in range(columns):
            if field[row][column] == BK:
                for r in range(row, 0, -1):
                    temp[r][column] = field[r-1][column]
                temp[0][column] = ""  # Leaves the uppermost cell empty
    return temp

def seek_for_match(field, temp, rows, columns):
    for row in range(rows):
        for column in range(columns):
            if column + 2 < columns:
                if field[row][column] != BK and field[row][column+1] != BK and field[row][column+2] != BK:
                    if field[row][column] == field[row][column+1] == field[row][column+2]:
                        temp[row][column] = W
                        temp[row][column+1] = W
                        temp[row][column+2] = W

            if row + 2 < rows:
                if field[row][column] != BK and field[row+1][column] != BK and field[row+2][column] != BK:
                    if field[row][column] == field[row+1][column] == field[row+2][column]:
                        temp[row][column] = W
                        temp[row+1][column] = W
                        temp[row+2][column] = W
    return temp

def clear_matches(field, temp, rows, columns):
    for row in range(rows):
        for column in range(columns):
            if field[row][column] == W:
                temp[row][column] = BK
    return temp

def write_from_temp(field, temp):
    for row in range(len(field)):
        for column in range(len(field[row])):
            field[row][column] = temp[row][column]
    return field

def update_grid(field, rows, columns):
    temp = [row[:] for row in field]  # Create a copy of the field
    temp = seek_for_match(field, temp, rows, columns)
    temp = clear_matches(field, temp, rows, columns)
    temp = seek_for_empty(field, temp, rows, columns)
    field = write_from_temp(field, temp)
    return field


def seek_for_empty(field, temp, rows, columns):
    for row in range(rows-1, 0, -1):  # Start from the second to last row and go upwards
        for column in range(columns):
            if field[row][column] == EMPTY:
                for r in range(row, 0, -1):  # Start from the current row and go upwards
                    if r-1 >= 0:  # Ensure r-1 is within bounds
                        temp[r][column] = field[r-1][column]
                    else:
                        temp[r][column] = EMPTY  # Handle the top row case
    return temp
def seek_for_match(field, temp, rows, columns):
    for row in range(rows-1, 0, -1):  # Start from the second to last row and go upwards
        for column in range(columns):
            # Check for horizontal match
            if column + 2 < columns:
                if field[row][column] == field[row][column+1] == field[row][column+2]:  # Horizontal match
                    if field[row][column] != EMPTY and field[row][column+1] != EMPTY and field[row][column+2] != EMPTY:  # Not blanks
                        # Mark the match in temp
                        temp[row][column] = MATCH_MADE
                        temp[row][column+1] = MATCH_MADE
                        temp[row][column+2] = MATCH_MADE
                        
            # Check for vertical match
            if row + 2 < rows:
                if field[row][column] == field[row+1][column] == field[row+2][column]:  # Vertical match
                    if field[row][column] != EMPTY and field[row+1][column] != EMPTY and field[row+2][column] != EMPTY:  # Not blanks
                        # Mark the match in temp
                        temp[row][column] = MATCH_MADE
                        temp[row+1][column] = MATCH_MADE
                        temp[row+2][column] = MATCH_MADE

    return temp


[['EM', 'L', 'P', 'EM', 'B', 'R'], 
 ['Y', 'R', 'P', 'B', 'B', 'EM'], 
 ['L', 'P', 'G', 'R', 'Y', 'P'], 
 ['EM', 'L', 'G', 'Y', 'EM', 'G'], 
 ['G', 'EM', 'R', 'B', 'B', 'L'], 
 ['Y', 'B', 'G', 'P', 'B', 'R'], 
 ['Y', 'R', 'B', 'Y', 'B', 'EM'], 
 ['L', 'L', 'EM', 'L', 'P', 'L'], 
 ['L', 'Y', 'G', 'G', 'L', 'Y'], 
 ['R', 'L', 'P', 'Y', 'L', 'B'], 
 ['R', 'Y', 'Y', 'EM', 'G', 'R'], 
 ['R', 'B', 'EM', 'P', 'L', 'B'], 
 ['Y', 'EM', 'L', 'B', 'EM', 'L'], 
 ['B', 'G', 'Y', 'R', 'R', 'L']]


 def seek_for_empty(field, temp, rows, columns):
    for row in range(rows-1, -1, -1):  # Start from the last row and go upwards, including row 0
        for column in range(columns):
            if field[row][column] == EMPTY:
                for r in range(row, 0, -1):  # Move the entire column down
                    temp[r][column] = field[r-1][column]
                temp[0][column] = EMPTY

    # Additional check to ensure bricks don't disappear
    for row in range(rows):
        for column in range(columns):
            if temp[row][column] != EMPTY and row < rows - 1 and temp[row + 1][column] == EMPTY:
                temp[row + 1][column] = temp[row][column]
                temp[row][column] = EMPTY

    return temp


def seek_for_horizontal_match(field, temp, rows, columns):
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if column + 2 < columns:
                if field[row][column] != EMPTY and row + 1 < rows and field[row+1][column] != EMPTY and field[row][column] != MATCH_MADE:
                    if field[row][column] == field[row][column+1] == field[row][column+2]:
                        temp[row][column] = MATCH_MADE
                        temp[row][column+1] = MATCH_MADE
                        temp[row][column+2] = MATCH_MADE
                
    return temp


def get_grid_data(field=None, temp=None, sprite_grid=None, match_matrix=None):
    field_export = []
    temp_export = []
    sprite_export = []
    match_matrix_export = []

    if field is None:
        field = []
    if temp is None:
        temp = []
    if sprite_grid is None:
        sprite_grid = []
    if match_matrix is None:
        match_matrix = []

    for row in range(len(field)):
        field_row = []
        temp_row = []
        sprite_row = []
        match_row = []
        for column in range(len(field[row])):
            field_row.append(field[row][column]['abbr'])
            temp_row.append(temp[row][column]['abbr'])

            # Ensure match_matrix has the same dimensions as field
            if row < len(match_matrix) and column < len(match_matrix[row]):
                match = match_matrix[row][column]
                if match == True:
                    match_row.append('T')
                else:
                    match_row.append('F')
            else:
                match_row.append('F')  # Default value if match_matrix is out of range

            sprite = sprite_grid[row][column]   
            if sprite is None:
                sprite_row.append('NA')
            else:
                try:
                    sprite_row.append(sprite.brick_data['abbr'])
                except AttributeError as e:
                    print(f"Error: {e}")
                    sprite_row.append('NA')

        field_export.append(field_row)
        temp_export.append(temp_row)
        sprite_export.append(sprite_row)
        match_matrix_export.append(match_row)

    return field_export, temp_export, sprite_export, match_matrix_export

def check_for_matches(field, temp, rows, columns):
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]
    
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if field[row][column]['abbr'] != 'EM':
                # Check for horizontal matches
                horizontal_match_length = 1
                while column + horizontal_match_length < columns and field[row][column]['abbr'] == field[row][column + horizontal_match_length]['abbr']:
                    horizontal_match_length += 1
                if horizontal_match_length >= 3:
                    for i in range(horizontal_match_length):
                        temp[row][column + i]['abbr'] = 'MM'
                        match_matrix[row][column + i] = True
                    print(f"Horizontal Match of {horizontal_match_length} at row {row}, starting column {column}")

                # Check for vertical matches
                vertical_match_length = 1
                while row - vertical_match_length >= 0 and field[row][column]['abbr'] == field[row - vertical_match_length][column]['abbr']:
                    vertical_match_length += 1
                if vertical_match_length >= 3:
                    for i in range(vertical_match_length):
                        temp[row - i][column]['abbr'] = 'MM'
                        match_matrix[row - i][column] = True
                    print(f"Vertical Match of {vertical_match_length} at column {column}, starting row {row}")

    return match_matrix

def check_for_matches(field, temp, rows, columns):
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]

    
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if column + 2 < columns:
                if field[row][column]['abbr'] != 'EM':
                    match_length = 1
                    while column + match_length < columns and field[row][column]['abbr'] == field[row][column + match_length]['abbr']:
                        match_length += 1
                    if match_length >= 3:
                        for i in range(match_length):
                            temp[row][column + i]['abbr'] = 'MM'
                            match_matrix[row][column + i] = True
                        print(f"Horizontal Match of {match_length} at row {row}, starting column {column}")

    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if row >= 2:
                if field[row][column]['abbr'] != 'EM':
                    match_length = 1
                    while row - match_length >= 0 and field[row][column]['abbr'] == field[row - match_length][column]['abbr']:
                        match_length += 1
                    if match_length >= 3:
                        for i in range(match_length):
                            temp[row - i][column]['abbr'] = 'MM'
                            match_matrix[row - i][column] = True
                        print(f"Vertical Match of {match_length} at column {column}, starting row {row}")
    return match_matrix


    run = True
class GameScreen:
    def __init__(self, manager):
        self.manager = manager
        self.move_delay = 150
        self.cursor_index_y = ROWS // 2
        self.cursor_index_x = COLUMNS // 2
        self.last_move_time = pygame.time.get_ticks()
        self.cursor_swap_done = False
        self.swap_occurred = False
        self.operation_flags = ["Match", "Empty", "Clear"]
        self.operation_cycle = 0

        self.field, self.temp, self.sprite_grid, self.all_bricks = initial_run(
            ROWS, COLUMNS, COLORS_LIST, [], [], []
        )

        self.field = update_grid(self.field, self.temp, ROWS, COLUMNS, "Match", False)
        self.field, self.sprite_grid = sync_temp_to_sprites(self.field, self.temp, self.sprite_grid, "Clear", False)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.cursor_swap_done:
                    self.temp = cursor_swap_input(self.field, self.temp, self.cursor_index_x, self.cursor_index_y)
                    self.cursor_swap_done = True
                    self.swap_occurred = True
                elif event.key == pygame.K_ESCAPE:
                    self.manager.set_screen(PauseScreen(self.manager))

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.cursor_swap_done = False

    def update(self):
        operation_flag = self.operation_flags[self.operation_cycle % len(self.operation_flags)]

        keys = pygame.key.get_pressed()
        self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
            keys, player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay
        )

        if self.swap_occurred:
            self.swap_occurred = False

        self.temp = update_grid(self.field, self.temp, ROWS, COLUMNS, operation_flag, self.swap_occurred)
        self.field, self.sprite_grid, _ = sync_temp_to_sprites(self.field, self.temp, self.sprite_grid, operation_flag, self.swap_occurred)

        if operation_flag == 'Clear':
            pygame.time.wait(10)

        self.operation_cycle += 1

    def draw(self, surface):
        surface.blit(background, (-center_of_window_x, -center_of_field_y))
        render_sprites(self.sprite_grid)
        draw_cursor(player_pos.x, player_pos.y, BRICK_WIDTH, BRICK_HEIGHT)


class GameScreen:
    def __init__(self, manager):
        self.manager = manager
        self.player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.cursor_swap_done = False
        self.matches_found = False
        self.match_made = False
        self.all_bricks = pygame.sprite.Group()
        self.background = pygame.image.load('images/hill-country-braun-sunrise.jpg')

        self.move_delay = 150
        self.cursor_index_y = ROWS // 2
        self.cursor_index_x = COLUMNS // 2
        self.last_move_time = pygame.time.get_ticks()

        # Initialize your game field
        self.field, self.temp, self.sprite_grid, _ = initial_run(
            ROWS, COLUMNS, COLORS_LIST, [], [], []
        )


import pygame
import math
from settings import *

class HomeScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.game_started = False
        self.color_shift = 0  # Used to animate color changes

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

        font = pygame.font.SysFont(DEFAULT_FONT, 74)
        text = font.render("Home Screen", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont(DEFAULT_FONT, 36)
        text = font.render("Press Enter to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(text, text_rect)

        text = font.render("Press Escape to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        screen.blit(text, text_rect)



def update(self):
    keys = pygame.key.get_pressed()
    self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
        keys, self.player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay
    )

    if self.state == "waiting_for_input":
        # Wait for player to press space (handled in handle_events)
        pass

    elif self.state == "animating":
        self.all_animations_complete = all(
            not sprite.is_animating()
            for row in self.sprite_grid
            for sprite in row if sprite
        )
        if self.all_animations_complete:
            self.state = "resolving_matches"

    elif self.state == "resolving_matches":
        operation_flag = self.operation_flags[self.operation_cycle % len(self.operation_flags)]
        self.temp = update_grid(self.field, self.temp, ROWS, COLUMNS, operation_flag, self.swap_occurred)
        self.field, self.sprite_grid = sync_temp_to_sprites(
            self.field, self.temp, self.sprite_grid, operation_flag, self.swap_occurred, self.all_bricks
        )

        if operation_flag == 'Clear':
            pygame.time.wait(10)

        self.operation_cycle += 1
        self.swap_occurred = False
        self.state = "animating"




def update(self):    
    keys = pygame.key.get_pressed()
    self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
        keys, self.player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay
    )

    if self.state == "animating":
        self.all_animations_complete = update_sprites(self.sprite_grid)
        if self.all_animations_complete:
            self.state = "resolving"

    elif self.state == "resolving":
        operation_flag = self.operation_flags[self.operation_cycle % len(self.operation_flags)]
        self.temp = update_grid(self.field, self.temp, ROWS, COLUMNS, operation_flag, self.swap_occurred)
        self.field, self.sprite_grid = sync_temp_to_sprites(
            self.field, self.temp, self.sprite_grid, operation_flag, self.swap_occurred, self.all_bricks
        )
        self.operation_cycle += 1
        self.swap_occurred = False
        self.state = "animating"

                    self.temp = update_grid(self.field, self.temp, ROWS, COLUMNS, operation_flag, self.swap_occurred)

def update(self):
    keys = pygame.key.get_pressed()
    self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
        keys, self.player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay
    )

    if self.state == "resolving":
        operation_flag = self.operation_flags[self.operation_cycle % len(self.operation_flags)]
        self.temp = update_grid(self.field, self.temp, ROWS, COLUMNS, operation_flag, self.swap_occurred)
        self.field, self.sprite_grid = sync_temp_to_sprites(
            self.field, self.temp, self.sprite_grid, operation_flag, self.swap_occurred, self.all_bricks
        )
        self.swap_occurred = False
        self.next_state = "animating"  # Delay the state change

    elif self.state == "animating":
        self.all_animations_complete = update_sprites(self.sprite_grid)
        if self.all_animations_complete:
            self.next_state = "resolving"
            self.operation_cycle += 1

    # Apply state change after update logic
    if hasattr(self, 'next_state'):
        self.state = self.next_state
        del self.next_state



def check_for_matches(field, temp, rows, columns):
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]

    for row in range(rows-1, -1, -1):
        column = 0
        while column < columns:
            if field[row][column]['abbr'] != 'EM':
                # Check for horizontal matches
                horizontal_match_length = 1
                while (column + horizontal_match_length < columns and
                       field[row][column]['abbr'] == field[row][column + horizontal_match_length]['abbr']):
                    horizontal_match_length += 1
                if horizontal_match_length >= 3:
                    for i in range(horizontal_match_length):
                        match_matrix[row][column + i] = True
                    print(f"Horizontal Match of {horizontal_match_length} at row {row}, starting column {column}")
                    column += horizontal_match_length  # Skip matched cells
                    continue  # Skip vertical check for these cells

            column += 1  # Move to next column

    for column in range(columns):
        row = rows - 1
        while row >= 0:
            if field[row][column]['abbr'] != 'EM':
                vertical_match_length = 1
                while (row - vertical_match_length >= 0 and
                       field[row][column]['abbr'] == field[row - vertical_match_length][column]['abbr']):
                    vertical_match_length += 1
                if vertical_match_length >= 3:
                    for i in range(vertical_match_length):
                        match_matrix[row - i][column] = True
                    print(f"Vertical Match of {vertical_match_length} at column {column}, starting row {row}")
                    row -= vertical_match_length  # Skip matched cells
                    continue
            row -= 1

    return match_matrix


Keep if doesnt work:
def check_for_matches(field, temp, rows, columns):
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]
    
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if field[row][column]['abbr'] != 'EM':
                # Check for horizontal matches
                horizontal_match_length = 1
                while column + horizontal_match_length < columns and field[row][column]['abbr'] == field[row][column + horizontal_match_length]['abbr']:
                    horizontal_match_length += 1
                if horizontal_match_length >= 3:
                    for i in range(horizontal_match_length):
                        #temp[row][column + i]['abbr'] = 'MM'
                        match_matrix[row][column + i] = True
                    print(f"Horizontal Match of {horizontal_match_length} at row {row}, starting column {column}")

                # Check for vertical matches
                vertical_match_length = 1
                while row - vertical_match_length >= 0 and field[row][column]['abbr'] == field[row - vertical_match_length][column]['abbr']:
                    vertical_match_length += 1
                if vertical_match_length >= 3:
                    for i in range(vertical_match_length):
                        #temp[row - i][column]['abbr'] = 'MM'
                        match_matrix[row - i][column] = True
                    print(f"Vertical Match of {vertical_match_length} at column {column}, starting row {row}")

    return match_matrix

    # Initialize these in your sprite class
self.velocity_y = 0
self.gravity = 0.5  # Adjust this value to control acceleration

# In your update method
if self.rect.x == self.target_x:
    if self.rect.y < self.target_y:
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.y > self.target_y:
            self.rect.y = self.target_y
            self.velocity_y = 0  # Reset when landing
    
    elif self.rect.y > self.target_y:
        self.velocity_y += self.gravity
        self.rect.y -= self.velocity_y
        if self.rect.y < self.target_y:
            self.rect.y = self.target_y
            self.velocity_y = 0  # Reset when landing


            # Set final_target_y only once when fall starts
            if self.final_target_y is None or self.rect.y < self.target_y:
                self.final_target_y = self.target_y

            # Apply gravity
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # Clamp to final target
            if self.rect.y >= self.final_target_y:
                self.rect.y = self.final_target_y
                self.velocity_y = 0
                self.final_target_y = None  # Reset for next fall

def seek_for_empty(field, rows, columns):
    new_positions = []  # To store (old_row, column, new_row) for each moved brick

    for column in range(columns):
        empty_rows = []  # Stack of empty row indices in this column

        # First pass: collect empty positions
        for row in range(rows - 1, -1, -1):
            if field[row][column]['abbr'] == 'EM':
                empty_rows.append(row)

        # Second pass: move bricks down into empty positions
        for row in range(rows - 1, -1, -1):
            if field[row][column]['abbr'] != 'EM' and empty_rows and row < empty_rows[-1]:
                new_row = empty_rows.pop()
                field[new_row][column] = field[row][column]
                field[row][column] = EMPTY
                new_positions.append((row, column, new_row))

    return field, new_positions

    def seek_for_empty(field, temp, rows, columns):
    for row in range(rows-1, -1, -1):  # Start from the last row and go upwards, including row 0w
        for column in range(columns):
            if field[row][column]['abbr'] == 'EM':
                for r in range(row, 0, -1):  # Move the entire column down
                    temp[r][column] = field[r-1][column]
                temp[0][column] = EMPTY  # Set the top cell to EMPTY there will not be an id added...atleast not yet.
    return temp


#Scoring with matches:
def check_for_matches(field, temp, rows, columns):
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]
    score = 0

    for row in range(rows-1, -1, -1):
        column = 0
        while column < columns:
            if field[row][column]['abbr'] != 'EM':
                horizontal_match_length = 1
                while (column + horizontal_match_length < columns and
                       field[row][column]['abbr'] == field[row][column + horizontal_match_length]['abbr']):
                    horizontal_match_length += 1
                if horizontal_match_length >= 3:
                    for i in range(horizontal_match_length):
                        match_matrix[row][column + i] = True
                    score += 10 * horizontal_match_length + 5 * max(0, horizontal_match_length - 3)
                    print(f"Horizontal Match of {horizontal_match_length} at row {row}, starting column {column}")
                    column += horizontal_match_length
                    continue
            column += 1

    for column in range(columns):
        row = rows - 1
        while row >= 0:
            if field[row][column]['abbr'] != 'EM':
                vertical_match_length = 1
                while (row - vertical_match_length >= 0 and
                       field[row][column]['abbr'] == field[row - vertical_match_length][column]['abbr']):
                    vertical_match_length += 1
                if vertical_match_length >= 3:
                    for i in range(vertical_match_length):
                        match_matrix[row - i][column] = True
                    score += 10 * vertical_match_length + 5 * max(0, vertical_match_length - 3)
                    print(f"Vertical Match of {vertical_match_length} at column {column}, starting row {row}")
                    row -= vertical_match_length
                    continue
            row -= 1

    return match_matrix, score


#pseudocode for combo scores:
total_score = 0
combo_multiplier = 1

while True:
    match_matrix, score = check_for_matches(field, temp, rows, columns)
    if not any(True in row for row in match_matrix):
        break  # No more matches, combo ends

    # Apply combo multiplier
    total_score += score * combo_multiplier
    print(f"Combo x{combo_multiplier}! Score this round: {score * combo_multiplier}")

    # Mark and clear matches
    temp = manage_match_matrix(match_matrix, temp, rows, columns)
    field = apply_gravity_and_refill(temp)  # You need this function to drop bricks and refill

    combo_multiplier += 1


class Brick:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 50, 50)  # example values
        self.previous_y = self.rect.y
        # other initializations...
def update(self):
    self.previous_y = self.rect.y
    # then update self.rect.y based on movement logic
    self.rect.y += self.velocity_y  # or however you're moving it


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

    # Once x is aligned, handle vertical movement
    if self.rect.x == self.target_x:
        if self.final_target_y is None or self.rect.y < self.target_y:
            self.final_target_y = self.target_y

        if self.is_falling:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.y >= self.final_target_y:
                self.rect.y = self.final_target_y
                self.velocity_y = 0
                self.final_target_y = None
                self.is_falling = False

            # Optional: stop very slow movement
            if abs(self.velocity_y) < 0.5:
                self.velocity_y = 0


1. Introduce a scroll_offset
    This is a value that starts at 0 and increases each frame during the scroll:

    self.scroll_offset += self.scroll_speed  # pixels per frame

2. Apply scroll_offset to Brick Rendering
    In your Brick class or rendering logic, calculate the actual position like this:

    self.rect.y = init_y + (self.row * BRICK_HEIGHT) - scroll_offset
    
    This way, bricks appear to move up smoothly without changing their logical row yet.

3. When scroll_offset >= BRICK_HEIGHT
    That means you've scrolled up one full row. Now:

    Reset scroll_offset = 0
    Decrease each brick’s row by 1
    Call move_to_index() to update their target_y based on the new row
    Add a new row of bricks at the bottom

4. Add a New Row
    You can generate a new row of bricks and insert it at the bottom of your grid:

    new_row = generate_new_brick_row()
    self.sprite_grid.append(new_row) 
    
5. Verify that the top row is empty, rather that row index 0 doesnt contain any sprites at the time when the offset is a couple pixles away from the CELL SIZE if it does then its over....
Additionally when the offset is a couple pixles away from the CELL SIZE the cause the bricks to shake a little bit. So add a little shake method for the sprite.


import random
import uuid

def add_new_row(field, temp, sprite_grid, rows, columns, brick_colors, all_bricks=None):
    for column in range(columns):
        if field[0][column]['abbr'] != 'EM':
            print(f"Game Over, Hit at: {field[0][column]['abbr']}")
            return field, temp, sprite_grid, all_bricks

    for row in range(rows - 1):
        for column in range(columns):
            temp[row][column] = temp[row + 1][column]
            field[row][column] = field[row + 1][column]
            sprite_grid[row][column] = sprite_grid[row + 1][column]

    new_temp_row = []
    new_field_row = []
    new_sprite_row = []

    for column in range(columns):
        brick_color = random.choice(brick_colors)
        brick_data = brick_color.copy()
        brick_data["id"] = str(uuid.uuid4())
        brick = Brick(brick_data, rows - 1, column)

        if all_bricks is not None:
            all_bricks.add(brick)

        new_temp_row.append(brick_data)
        new_field_row.append(brick_data)
        new_sprite_row.append(brick)

    temp[rows - 1] = new_temp_row
    field[rows - 1] = new_field_row
    sprite_grid[rows - 1] = new_sprite_row

    return field, temp, sprite_grid, all_bricks
pygame.event.post(pygame.event.Event(pygame.QUIT))



def add_new_row(field, temp, sprite_grid, rows, columns, brick_colors, all_bricks=None):
    # Shift all rows up by one
    for row in range(rows - 1):
        for column in range(columns):
            temp[row][column] = temp[row + 1][column]
            field[row][column] = field[row + 1][column]
            sprite_grid[row][column] = sprite_grid[row + 1][column]

    # Check for game over condition in the new top row
    for column in range(columns):
        if temp[0][column]['abbr'] != 'EM':
            print(f"Game Over, Hit at: {field[0][column]['abbr']}")
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return field, temp, sprite_grid, all_bricks

    # Create a new row of bricks for the bottom row
    new_temp_row = []
    new_field_row = []
    new_sprite_row = []

    for column in range(columns):
        brick_color = random.choice(brick_colors)
        brick_data = brick_color.copy()
        brick_data["id"] = str(uuid.uuid4())
        brick = Brick(brick_data, rows - 1, column)

        if all_bricks is not None:
            all_bricks.add(brick)

        new_temp_row.append(brick_data)
        new_field_row.append(brick_data)
        new_sprite_row.append(brick)

    # Assign the new row to the bottom of the grid
    temp[rows - 1] = new_temp_row
    field[rows - 1] = new_field_row
    sprite_grid[rows - 1] = new_sprite_row

    return field, temp, sprite_grid, all_bricks


if self.state == "scrolling":
    self.scroll_offset -= self.scroll_speed * dt

    if round(self.scroll_offset % BRICK_HEIGHT) == 0 and not self.row_added:
        self.temp, self.field, self.sprite_grid = add_new_row(
            self.field, self.temp, self.sprite_grid, ROWS, COLUMNS, COLORS_LIST, self.all_bricks
        )

        print(f"FULL ROW RAISED: {self.scroll_offset}")
        print_data_to_console(self.field, self.temp, self.sprite_grid, self.all_bricks)

        self.scroll_offset += BRICK_HEIGHT
        self.row_added = True

    # Reset flag only when scroll_offset is no longer aligned
    elif round(self.scroll_offset % BRICK_HEIGHT) != 0:
        self.row_added = False


def draw_vertical_gradient(surface, top_color, bottom_color, rect):
    x, y, width, height = rect
    for i in range(height):
        ratio = i / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + width, y + i))


# Your color definitions
Y = {"name": "YELLOW", "hex": "#fed86dff", "abbr": "Y", "rgb": (254, 216, 109), "value": 1}
R = {"name": "RED", "hex": "#de6568ff", "abbr": "R", "rgb": (222, 101, 104), "value": 2}
B = {"name": "BLUE", "hex": "#6f9fe9ff", "abbr": "B", "rgb": (111, 159, 233), "value": 3}
G = {"name": "GREEN", "hex": "#94c47fff", "abbr": "G", "rgb": (148, 196, 127), "value": 4}
L = {"name": "LIGHT_GRAY", "hex": "#d0e0e3ff", "abbr": "L", "rgb": (208, 224, 227), "value": 5}
P = {"name": "PURPLE", "hex": "#8e7dc1ff", "abbr": "P", "rgb": (142, 125, 193), "value": 6}
W = {"name": "WHITE", "hex": "#ffffffff", "abbr": "W", "rgb": (255, 255, 255), "value": 7}
DG = {"name": "DARK_GREY", "hex": "#595959ff", "abbr": "DG", "rgb": (89, 89, 89), "value": 8}
BK = {"name": "BLACK", "hex": "#000000ff", "abbr": "BK", "rgb": (0, 0, 0), "value": 9}
EMPTY = {"name": "EMPTY", "hex": "#525252", "abbr": "EM", "rgb": (82, 82, 82, 50), "value": 0}
MATCH_MADE = {"name": "MATCH_MADE", "hex": "#FBFFB9", "abbr": "MM", "rgb": (251, 255, 185), "value": 10}

# Create a lookup dictionary
color_lookup = {color["abbr"]: color["rgb"] for color in [Y, R, B, G, L, P, W, DG, BK, EMPTY, MATCH_MADE]}

# Example: get RGB for 'B'
rgb_value = color_lookup['B']  # Output: (111, 159, 233)
