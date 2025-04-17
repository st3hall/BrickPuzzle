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