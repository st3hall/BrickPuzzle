from settings import *
from grid import *

import pygame
import random
import copy
import json

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
pygame.display.set_caption("Bricks")
dt = 0
font = pygame.font.Font(None, 36)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
cursor_swap_done = False
matches_found = False
match_made = False
all_bricks = pygame.sprite.Group()
background = pygame.image.load('images\hill-country-braun-sunrise.jpg')


def main():
    global last_move_time
    global cursor_swap_done
    global match_made
    move_delay = 150
    cursor_index_y = ROWS // 2
    cursor_index_x = COLUMNS // 2
    last_move_time = pygame.time.get_ticks()
    run = True
    temp_grid = []
    field_grid= []
    sprite_grid = []
    swap_occured = False
    match_made = False
    operation_flags = ["Match", "Empty", "Clear"]
    operation_cycle = 0

    #initalize all the grids field, temp, sprite_grid, they should all have the same contents
    field, temp, sprite_grid, all_bricks = initial_run(ROWS, COLUMNS, COLORS_LIST, temp_grid, field_grid, sprite_grid)
    
    print_data_to_console(field, temp, sprite_grid)

    field = update_grid(field, temp, ROWS, COLUMNS, "Match", False)
    print_data_to_console(field, temp, sprite_grid)
    field, sprite_grid = sync_temp_to_sprites(field, temp, sprite_grid, "Clear", swap_occured)

    print_data_to_console(field, temp, sprite_grid)

    # all_bricks.update()
    # all_bricks.draw(screen)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not cursor_swap_done:
                    temp = cursor_swap_input(field, temp, cursor_index_x, cursor_index_y)
                    cursor_swap_done = True
                    swap_occured = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    cursor_swap_done = False

        operation_flag = operation_flags[operation_cycle % len(operation_flags)]

        screen.blit(background, (-center_of_window_x,-center_of_field_y))
        keys = pygame.key.get_pressed()

        cursor_index_y, cursor_index_x, last_move_time = update_cursor_position(keys, player_pos,cursor_index_x, cursor_index_y, last_move_time, move_delay)

        if swap_occured:
            swap_occured = False

        
        temp = update_grid(field, temp, ROWS, COLUMNS, operation_flag, swap_occured)
        print_data_to_console(field, temp, sprite_grid)
        field, sprite_grid, sync_temp_to_sprites(field, temp, sprite_grid, operation_flag, swap_occured)
        if operation_flag == 'Clear':
            pygame.time.wait(10)
        operation_cycle += 1
        


        print_data_to_console(field, temp, sprite_grid)

        # all_bricks.update()
        # all_bricks.draw(screen)
        all_animations_complete = render_sprites(sprite_grid)
        draw_cursor(player_pos.x, player_pos.y, BRICK_WIDTH, BRICK_HEIGHT)

        if all_animations_complete:
            #print("Animations are complete")
            update_grid(field, temp, ROWS, COLUMNS, operation_flag, swap_occured)

        pygame.display.flip()
        dt = clock.tick(300) / 1000

    pygame.quit()

def update_cursor_position(keys, player_pos, cursor_index_x, cursor_index_y, last_move_time, move_delay):
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time > move_delay:
        #UP
        if keys[pygame.K_w]:
            if player_pos.y <= (center_of_window_y - (GAME_HEIGHT / 2)):
                player_pos.y -= 0
            else:
                player_pos.y -= BRICK_HEIGHT
                cursor_index_y = max(0, cursor_index_y - 1)
            last_move_time = current_time
        #DOWN
        if keys[pygame.K_s]:
            if player_pos.y >= (center_of_window_y + (GAME_HEIGHT / 2) - BRICK_HEIGHT):
                player_pos.y += 0
            else:
                player_pos.y += BRICK_HEIGHT
                cursor_index_y = min(ROWS - 1, cursor_index_y + 1)
            last_move_time = current_time
        #LEFT
        if keys[pygame.K_a]:
            if player_pos.x <= (center_of_window_x - (GAME_WIDTH / 2) + BRICK_WIDTH):
                player_pos.x -= 0
            else:
                player_pos.x -= BRICK_WIDTH
                cursor_index_x = max(0, cursor_index_x - 1)
            last_move_time = current_time
        #RIGHT
        if keys[pygame.K_d]:
            if player_pos.x >= (center_of_window_x + (GAME_WIDTH / 2) - (BRICK_WIDTH)):
                player_pos.x += 0
            else:
                player_pos.x += BRICK_WIDTH
                cursor_index_x = min(COLUMNS - 1, cursor_index_x + 1)
            last_move_time = current_time
    return cursor_index_y, cursor_index_x, last_move_time

def draw_cursor(pos_x, pos_y, width, height):
    points_left = [(pos_x, pos_y), (pos_x - width, pos_y), (pos_x - width, pos_y + height), (pos_x, pos_y + height)]
    points_right = [(pos_x, pos_y), (pos_x + width, pos_y), (pos_x + width, pos_y + height), (pos_x, pos_y + height)]
    pygame.draw.lines(screen, DG["hex"], True, points_left, 4)
    pygame.draw.lines(screen, DG["hex"], True, points_right, 4)

def initial_run(rows, columns, brick_colors, temp, field, sprite_grid):
    field.clear()
    temp.clear()
    sprite_grid.clear()
    for row in range(rows):
        temp_row = []
        field_row= []
        sprite_row= []
        for column in range(columns):
            brick_color = brick_colors[random.randrange(0,len(brick_colors)-1)] #Brick colors is a list of dictionaries containing brick data.
            brick_data = brick_color.copy()
            brick_data["id"] = str(uuid.uuid4())

            brick = Brick(brick_data, row, column)
            all_bricks.add(brick)

            temp_row.append(brick_data)
            field_row.append(brick_data)
            sprite_row.append(brick)
        temp.append(temp_row)
        field.append(field_row)
        sprite_grid.append(sprite_row)

    return field, temp, sprite_grid, all_bricks

def rebuild_sprite_grid(field):
    sprite_grid = []
    for row_idx, row in enumerate(field):
        sprite_row = []
        for col_idx, brick_data in enumerate(row):
            brick = Brick(brick_data, row_idx, col_idx)
            sprite_row.append(brick)
        sprite_grid.append(sprite_row)
    return sprite_grid

def cursor_swap_input(field, temp, cursor_x, cursor_y):
    global cursor_swap_done
    global last_move_time
    current_time = pygame.time.get_ticks()
    row = int(cursor_y)
    column = int(cursor_x)
    if column > 0:
        if temp[row][column-1] != EMPTY or temp[row][column] != EMPTY:
            import copy

            temp[row][column-1], temp[row][column] = (
                copy.deepcopy(temp[row][column]),
                copy.deepcopy(temp[row][column-1]),
                )

            cursor_swap_done = True
            last_move_time = current_time
            print(f"Swapped: {field[row][column-1]['abbr']} with {field[row][column]['abbr']} at ({row}, {column-1}) and ({row}, {column})")
    return temp

def sync_temp_to_sprites(field, temp, sprite_grid, operation_flag, swap_occured):
    # Step 1: Build a lookup of sprite IDs to their positions
    sprite_lookup = {}
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            if sprite:
                sprite_lookup[sprite.brick_data['id']] = (sprite, r, c)

    new_sprite_grid = [[None for x in range(len(sprite_grid[0]))] for y in range(len(sprite_grid))]
    for row in range(len(temp)):
        for col in range(len(temp[row])):
            new_sprite_data = temp[row][col]
            abbr = temp[row][col].get('abbr','')
            # print(f"New sprite data: {new_sprite_data}")
            # print(f"Checking cell: {row},{col}, abbr: {abbr}")

            if 'id' in new_sprite_data:  # Check if 'id' exists in new_sprite_data
                new_sprite_id = new_sprite_data['id']
                if new_sprite_id in sprite_lookup:
                    
                    if operation_flag == "Match":
                        if abbr == 'MM':
                            print(f"Sprite Match: {row},{col}")   
                            old_sprite = sprite_grid[row][col]
                            if old_sprite:
                                match_brick_sprite(old_sprite, MATCH_MADE)
                                new_sprite_grid[row][col] = old_sprite
                                print(f"Sprite Match: {row},{col}")
                                field[row][col]['abbr'] = 'MM'
                    
                    if operation_flag == "Empty":
                        if abbr == 'EM': #Temp = EM Happens in seek_for_empty
                            print(f"Sprite Killed: {row},{col}")
                            old_sprite = sprite_grid[row][col]
                            if old_sprite:
                                kill_brick_sprite(old_sprite)
                                print(f"Sprite Killed: {row},{col}")
                                field[row][col]['abbr'] = 'EM'
                                new_sprite_grid[row][col] = old_sprite
                                    
                    if operation_flag == "Clear":
                        if abbr == 'EM':
                            print(f"Sprite Cleared: {row},{col}")
                            field[row][col]['abbr'] = 'EM'
                            new_sprite_grid[row][col] = None

                    if not swap_occured:
                        sprite, old_r, old_c = sprite_lookup[new_sprite_id]
                        sprite.move_to_index(row, col)
                        new_sprite_grid[row][col] = sprite
                        field[row][col] = new_sprite_data

    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite_grid[r][c] = new_sprite_grid[r][c]

    return field, sprite_grid

def update_grid(field, temp, rows, columns, operation_flag, swap_occured):
    if operation_flag == "Match":
        temp = seek_for_vertical_match(field, temp, rows, columns)
        temp = seek_for_horizontal_match(field, temp, rows, columns)
        #print(f"Matches searched")
    if operation_flag == "Empty":
        temp = clear_matches(field, temp, rows, columns)
        #print(f"Matches cleared")
    if not swap_occured:
        temp = seek_for_empty(field, temp, rows, columns)
        #print(f"Empties searched, and grid phisiscs performed")
    return temp

def kill_brick_sprite(sprite):
    sprite.start_dying()
    #all_bricks.remove(sprite)
    sprite = None

def match_brick_sprite(sprite, color):
    sprite.match_made(color)

def render_grid(rows, columns, sprite_grid): #inital run, I dont use this anymore
    #print(f"Length of paramter sprite grid {len(sprite_grid)}")
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            # print(f"Length of paramter sprite grid {len(sprite_grid)}")
            # print(f"row: {row}, column: {column}")
            brick = sprite_grid[int(row)][int(column)]
            if brick:
                all_bricks.add(brick)
    #all_bricks.draw(screen)
    return all_bricks

def seek_for_empty(field, temp, rows, columns):
    for row in range(rows-1, -1, -1):  # Start from the last row and go upwards, including row 0w
        for column in range(columns):
            if field[row][column]['abbr'] == 'EM':
                for r in range(row, 0, -1):  # Move the entire column down
                    temp[r][column] = field[r-1][column]
                temp[0][column] = EMPTY  # Set the top cell to EMPTY there will not be an id added...atleast not yet.
    return temp

def seek_for_horizontal_match(field, temp, rows, columns):
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
                        print(f"Horizontal Match of {match_length} at row {row}, starting column {column}")
    return temp

def seek_for_vertical_match(field, temp, rows, columns):
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
                        print(f"Vertical Match of {match_length} at column {column}, starting row {row}")
    return temp

def clear_matches(field, temp, rows, columns):
    global match_made
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if field[row][column]['abbr'] == 'MM':
                temp[row][column]['abbr'] = 'EM'

                match_made = True
    return temp

# Function to check if any bricks are in match state
def any_bricks_in_match_state(sprite_grid):
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            if sprite is None:
                continue
            if sprite.is_in_match_state():
                #print(f"Brick in match state at ({r}, {c})")
                return True
    return False

# Function to check if any bricks are in dying state
def any_bricks_in_dying_state(sprite_grid):
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            if sprite is None:
                continue
            if sprite.is_in_dying_state():
                #print(f"Brick in dying state at ({r}, {c})")
                return True
    return False

def write_from_temp(field, temp): #This might be a thing of the past
    global cursor_swap_done
    for row in range(len(field)):
        for column in range(len(field[row])):
            field[row][column] = copy.deepcopy(temp[row][column])
    return field

def spawn_brick_sprite(sprite_grid, row, column, brick_data): #I dont use this
    brick = Brick(brick_data, row, column)
    sprite_grid[row][column] = brick
    all_bricks.add(brick)

def draw_brick(color, pos_x, pos_y, width, height): #Not used anymore
    pygame.draw.rect(screen, color, (pos_x, pos_y, width, height))
    pygame.draw.rect(screen, W["hex"], (pos_x, pos_y, width, height), OUTLINE_WIDTH)

def get_grid_data(field, temp, sprite_grid):
    field_export = []
    temp_export = []
    sprite_export = []
    for row in range(len(field)):
        field_row = []
        temp_row = []
        sprite_row = []
        for column in range(len(field[row])):
            field_row.append(field[row][column]['abbr'])
            temp_row.append(temp[row][column]['abbr'])
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
    #print(f"Field: {field_export}")

    return field_export, temp_export, sprite_export

def export_data(data, filename="grid_data.txt"):
    try:
        with open(filename, 'w') as file:
            file.write('{\n')
            for i, (key, grid) in enumerate(data.items()):
                comma = ',' if i < len(data) - 1 else ''
                file.write(f'  "{key}": [\n')
                for j, row in enumerate(grid):
                    row_comma = ',' if j < len(grid) - 1 else ''
                    file.write(f'    {repr(row)}{row_comma}\n')
                file.write(f'  ]{comma}\n')
            file.write('}\n')

        #print(f"Data written to {filename}")

        with open(filename, 'r') as file:
            loaded_data = eval(file.read())  # Still Python format
            #print("Data loaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_data_to_console(field, temp, sprite_grid):
    field_export, temp_export, sprite_export = get_grid_data(field, temp, sprite_grid)
    all_bricks_grid = print_all_bricks(all_bricks)
    export_data({'field': field_export, 'temp': temp_export, 'sprite': sprite_export, 'all_bricks_grid': all_bricks_grid})

def print_all_bricks(all_bricks):
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    for brick in all_bricks:
        r = brick.row
        c = brick.column
        if brick.brick_data is None:
            grid[r][c] = 'NA'
        else:
            grid[r][c] = brick.brick_data['abbr']
    # print("All_bricks:")
    # for row in grid:
    #     print(row)
    return grid

def render_sprites(sprite_grid):
    all_animations_complete = True
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            #print(f"Sprite: {sprite}")
            if sprite is None:
                continue
            sprite.update()
            sprite.draw(screen)
            if sprite.is_in_dying_state() or sprite.is_in_match_state():
                all_animations_complete = False
    
    return all_animations_complete

if __name__ == "__main__":
    main()

