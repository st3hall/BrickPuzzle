from settings import *
from grid import *

import pygame
import time
import random

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
pygame.display.set_caption("Bricks")
dt = 0
font = pygame.font.Font(None, 36)
init_x = center_of_window_x - (BRICK_WIDTH * COLUMNS / 2)
init_y = center_of_window_y - (BRICK_HEIGHT * ROWS / 2)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
cursor_swap_done = False




def main():
    global last_move_time
    global cursor_swap_done
    move_delay = 70
    cursor_index_y = ROWS // 2
    cursor_index_x = COLUMNS // 2
    last_move_time = pygame.time.get_ticks()
    run = True
    temp_grid = []
    field_grid= []

    field_grid, temp_grid = initial_run(ROWS, COLUMNS, COLORS_LIST, temp_grid, field_grid)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not cursor_swap_done:
                    temp_grid = cursor_swap_input(field_grid, temp_grid, cursor_index_x, cursor_index_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    cursor_swap_done = False

        screen.fill(B['hex'])
        keys = pygame.key.get_pressed()
    
        cursor_index_y, cursor_index_x, last_move_time = update_cursor_position(keys, player_pos,cursor_index_x, cursor_index_y, last_move_time,move_delay)           
        update_grid(field_grid, temp_grid, ROWS, COLUMNS)
        draw_cursor(player_pos.x, player_pos.y, BRICK_WIDTH, BRICK_HEIGHT)    
                
        pygame.display.flip()      
        dt = clock.tick(60) / 1000        
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
def draw_brick(color, pos_x, pos_y, width = BRICK_WIDTH, height = BRICK_HEIGHT):
    pygame.draw.rect(screen, color, (pos_x, pos_y, width, height))
    pygame.draw.rect(screen, W["hex"], (pos_x, pos_y, width, height), OUTLINE_WIDTH)
def draw_cursor(pos_x, pos_y, width, height):
    points_left = [(pos_x, pos_y), (pos_x - width, pos_y), (pos_x - width, pos_y + height), (pos_x, pos_y + height)]
    points_right = [(pos_x, pos_y), (pos_x + width, pos_y), (pos_x + width, pos_y + height), (pos_x, pos_y + height)]
    pygame.draw.lines(screen, DG["hex"], True, points_left, 4)
    pygame.draw.lines(screen, DG["hex"], True, points_right, 4)
def initial_run(rows, columns, brick_colors, temp, field):
    read_grid = []
    for row in range(rows, 0, -1):
        temp_row = []
        field_row= []
        read_row= []
        for column in range(columns):
            brick_color = brick_colors[random.randrange(0,len(brick_colors))]
            temp_row.append(brick_color)
            field_row.append(brick_color)
            read_row.append(brick_color["abbr"])
        temp.append(temp_row)
        field.append(field_row)
        read_grid.append(read_row)
    print(read_grid)
    return field, temp
def cursor_swap_input(field, temp, cursor_x, cursor_y):
    global cursor_swap_done
    global last_move_time

    current_time = pygame.time.get_ticks()

    row = int(cursor_y)
    column = int(cursor_x)

    # Ensure column-1 is within bounds
    if column > 0:
        cursor_L = field[row][column-1]
        cursor_R = field[row][column]
        
        # Swap the elements
        temp_L = cursor_L
        cursor_L = cursor_R 
        cursor_R = temp_L

        # Update the temp array
        temp[row][column-1] = cursor_L
        temp[row][column] = cursor_R
        pygame.time.wait(50)
  
        cursor_swap_done = True
        last_move_time = current_time
    return temp
def seek_for_empty(field, temp, rows, columns):
    for row in range(rows-1,-1,-1):  # Start from the last row and go upwards and on the second to top
        for column in range(columns):
            if field[row][column] == EMPTY:
                temp[row][column] = field[row-1][column]
                if row-1 == 0:
                    temp[0][column] = EMPTY
    return temp
def seek_for_horizontal_match(field, temp, rows, columns):
    for row in range(rows-1,-1,-1):
        for column in range(columns):
            if column + 2 < columns:
                if field[row][column] != EMPTY and field[row][column] != MATCH_MADE:
                    if field[row][column] == field[row][column+1] == field[row][column+2]: # Horizontal match
                        temp[row][column] = MATCH_MADE
                        temp[row][column+1] = MATCH_MADE
                        temp[row][column+2] = MATCH_MADE                   
    return temp
def seek_for_vertical_match(field, temp, rows, columns):
    for row in range(rows-1,-1,-1):  # Start from the second to last row and go upwards
        for column in range(columns):
            # Check for vertical match
            if row + 2 < rows-1:
                if field[row][column] != EMPTY and field[row][column] != MATCH_MADE:
                    if field[row][column] == field[row+1][column] == field[row+2][column]:  # Vertical match
                        temp[row][column] = MATCH_MADE
                        temp[row+1][column] = MATCH_MADE
                        temp[row+2][column] = MATCH_MADE                       
    return temp
def clear_matches(field, temp, rows, columns):
    for row in range(rows-1,-1,-1):
        for column in range(columns):
            if field[row][column] == MATCH_MADE:
                temp[row][column] = EMPTY
    return temp
def write_from_temp(field, temp):
    global cursor_swap_done
    for row in range(len(field)):
        for column in range(len(field[row])):
            field[row][column] = temp[row][column]
    return field
def render_grid(x_offset, y_offset, rows, columns, field):
    for row in range(rows-1,-1,-1):  # Start from the last row and go upwards
        for column in range(columns):
            pos_x = init_x + x_offset * column
            pos_y = init_y + y_offset * row
            cell_value = field[int(row)][int(column)]
            rgb_value = cell_value["rgb"]
            draw_brick(rgb_value, pos_x, pos_y)
def update_grid(field, temp, rows, columns): #the queue, first temp comes from cursor swap    
    temp = seek_for_vertical_match(field, temp, rows, columns)
    temp = seek_for_horizontal_match(field, temp, rows, columns)
    pygame.time.wait(30)
    temp = clear_matches(field, temp, rows, columns)
    temp = seek_for_empty(field, temp, rows, columns) #shifts temp row = field row-1
    field = write_from_temp(field, temp)
    render_grid(BRICK_WIDTH, BRICK_HEIGHT, rows, columns, field)                            

if __name__ == "__main__":
    main()
    
