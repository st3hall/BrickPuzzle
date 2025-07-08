from settings import *
from puzzle_grids import *
import pygame
import random
from home_screen_buttons import*

class GameScreen(Screen):
    def __init__(self, manager, player_data):
        self.manager = manager
        self.player_data = player_data
        
        self.player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.matches_found = False
        self.match_made = False
        self.all_bricks = pygame.sprite.Group()
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill(BACK_GROUND)
        
        #self.background = pygame.image.load('images/hill-country-braun-sunrise.jpg')
        self.move_delay = 150
        self.cursor_index_y = ROWS // 2
        self.cursor_index_x = COLUMNS // 2
        self.last_move_time = pygame.time.get_ticks()
        self.cursor_swap_done = False
        self.swap_occurred = False
        self.row_added = False
        self.operation_flags = ["Match", "Empty", "Clear"]
        self.operation_cycle = 0
        self.all_animations_complete = False
        self.state = "resolving"
        self.score = 0
        self.scroll_speed = 25
        self.scroll_offset = 0
        self.time_since_last_row = 0
        self.row_interval = 2
        self.current_row_raised = 0
        self.clock = pygame.time.Clock()
        dt = self.clock.tick(60)/1000
        
                # Initialize your game field
        self.field, self.temp, self.sprite_grid, self.all_bricks = initial_run(COLORS_LIST, self.all_bricks, row_from_top=3)
        print_data_to_console(self.field, self.temp, self.sprite_grid, self.all_bricks)

        result = update_grid(self.field, self.temp, "Match", False)
        self.field = result['temp']
        self.field, self.sprite_grid = sync_temp_to_sprites(self.field, self.temp, self.sprite_grid, "Clear", False)

            # Initialize buttons
        font_small = pygame.font.SysFont(DEFAULT_FONT, 18)
        button_width = 80
        button_height = 30
        center_x = (WINDOW_WIDTH - button_width) // 2
        button_y_start = 20
        button_spacing = button_width //2 + 5

        self.buttons = [
            Button((center_x + (button_spacing), button_y_start, button_width, button_height), "Pause", self.pause_game, font_small, G['rgb'], tuple(min(255, c + 30) for c in G['rgb'])),
            Button((center_x - (button_spacing), button_y_start, button_width, button_height), "Quit", self.return_home, font_small, R['rgb'], tuple(min(255, c + 30) for c in R['rgb']))
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.cursor_swap_done:
                    self.temp = cursor_swap_input(self.field, self.temp, self.cursor_index_x, self.cursor_index_y)
                    self.cursor_swap_done = True
                    self.swap_occurred = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.cursor_swap_done = False

            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(mouse_pos)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.check_click(event.pos)

    def update(self): 
        dt = self.clock.tick(60) / 1000   
        keys = pygame.key.get_pressed()

        self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
            keys, self.player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay, self.current_row_raised
        )
        if self.swap_occurred:
            self.swap_occurred = False
        
        #print(f"State: {self.state}")
        if self.state == "resolving":
            operation_flag = self.operation_flags[self.operation_cycle % len(self.operation_flags)]
            result = update_grid(self.field, self.temp, operation_flag, self.swap_occurred)
            self.field = result['temp']
            self.field, self.sprite_grid = sync_temp_to_sprites(
                self.field, self.temp, self.sprite_grid, operation_flag, self.swap_occurred, self.all_bricks
            )
            self.score += result['score']
            self.next_state = "animating"
        
        if self.state == "animating":
            self.all_animations_complete = update_sprites(self.sprite_grid)
            if self.all_animations_complete:
                self.next_state = "scrolling"
                self.operation_cycle += 1
    
        #Endless mode, scroll
        if self.state == "scrolling":
            self.current_row_raised = int(abs(round(self.scroll_offset) / BRICK_HEIGHT))
            #self.scroll_speed += self.current_row_raised * dt
            self.scroll_offset -= (self.scroll_speed * dt)
                        
            if round(self.scroll_offset % BRICK_HEIGHT) == 0 and not self.row_added:
                #Add new row to temp, and to sprites shift all temp up
                self.temp, self.sprite_grid = add_new_row(self.field, self.temp, self.sprite_grid, COLORS_LIST, self.all_bricks)
                
                print_data_to_console(self.field, self.temp, self.sprite_grid, self.all_bricks)

                self.field, self.sprite_grid = sync_temp_to_sprites(self.field, self.temp, self.sprite_grid)         
               
                print(f"CURRENT SPEED: {self.scroll_speed}, CURRENT ROW: {self.current_row_raised}")                     
                self.row_added = True
            elif round(self.scroll_offset % BRICK_HEIGHT) != 0:
                self.row_added = False

            if check_game_over(self.field, current_row=self.current_row_raised):
                self.player_data.update_score(self.score)
                print("Game Over!")
                self.manager.set_screen(HomeScreen(self.manager, self.player_data))
                return
            
            for r in range(len(self.sprite_grid)):
                for c in range(len(self.sprite_grid[r])):
                    sprite = self.sprite_grid[r][c]
                    if sprite:
                        sprite.update()

            self.next_state = "resolving"

        if hasattr(self, 'next_state'):
            self.state = self.next_state
            del self.next_state
            
        print_data_to_console(self.field, self.temp, self.sprite_grid, self.all_bricks)
            
    def return_home(self):
        from home_screen_buttons import HomeScreen
        self.manager.set_screen(HomeScreen(self.manager, self.player_data))
    
    def return_to_select(self): #Not used here, only in puzzle
        from puzzle_select_screen import PuzzleSelectScreen
        self.manager.set_screen(PuzzleSelectScreen(self.manager, self.player_data))
    
    def pause_game(self):
        from pause_screen import PauseScreen
        self.manager.set_screen(PauseScreen(self.manager, self.player_data))
        game_paused = True

    def retry_puzzle(self):
        self.moves_count = 0
        self.field, self.temp, self.sprite_grid, self.all_bricks, self.moves_available = initial_run_puzzle(COLORS_LIST, self.all_bricks, self.puzzle_number)

    def draw(self, surface):
        surface.blit(self.background, (0,0))#(-center_of_window_x, -center_of_field_y))
        draw_sprites(self.sprite_grid, self.scroll_offset, surface)
        # Add scroll offset
        x = init_x + (self.cursor_index_x * BRICK_WIDTH) 
        y = init_y + (self.cursor_index_y * BRICK_HEIGHT) + self.scroll_offset

        draw_cursor(x, y, BRICK_WIDTH, BRICK_HEIGHT, surface)
        
        #Translucent surface to indicate you cant match with these Quite yet.
        translucent_surface = pygame.Surface((WINDOW_WIDTH, CELL_SIZE*2 + PADDING), pygame.SRCALPHA)
        translucent_surface.fill(DG["rgb"] + (150,))  # Add alpha value for translucency
        #surface.blit(translucent_surface, (0, WINDOW_HEIGHT - (CELL_SIZE*2 + PADDING)))
        
        draw_vertical_gradient(surface, 255, 100, (0, 0, WINDOW_WIDTH, CELL_SIZE + PADDING), step_height=2)
        
        #x,y,width,height=rect
        opaque_surface = pygame.Surface((WINDOW_WIDTH, CELL_SIZE + PADDING), pygame.SRCALPHA)
        opaque_surface.fill(DG["rgb"])
        pygame.draw.line(surface, DG["rgb"], (0, CELL_SIZE + PADDING), (WINDOW_WIDTH, CELL_SIZE + PADDING), 2)
        #surface.blit(opaque_surface, (0, -CELL_SIZE))#top block
        surface.blit(opaque_surface, (0, WINDOW_HEIGHT - (CELL_SIZE + PADDING)))#bottom

        self.clock.tick(60)
        fps = str(int(self.clock.get_fps()))
        font = pygame.font.SysFont(DEFAULT_FONT, 24)
        text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(10, 10))
        #surface.blit(text, text_rect)

        score = str(int(self.score))
        font = pygame.font.SysFont(DEFAULT_FONT, 20)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        text_rect = text.get_rect(topright=(WINDOW_WIDTH-10, 10))
        surface.blit(text, text_rect)

        for button in self.buttons:
            button.draw(surface)

def update_cursor_position(keys, player_pos, cursor_index_x, cursor_index_y, last_move_time, move_delay, current_row_raised = 0):
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time > move_delay:
        visible_rows = GAME_HEIGHT // BRICK_HEIGHT

        # Logical max row index the player can move to
        max_cursor_index_y = current_row_raised + visible_rows - 1

        # Logical min row index (topmost visible row)
        min_cursor_index_y = current_row_raised

        # UP
        if keys[pygame.K_w]:
            if cursor_index_y > min_cursor_index_y:
                cursor_index_y -= 1
                player_pos.y -= BRICK_HEIGHT
                last_move_time = current_time

        # DOWN
        if keys[pygame.K_s]:
            if cursor_index_y < max_cursor_index_y:
                cursor_index_y += 1
                player_pos.y += BRICK_HEIGHT
                last_move_time = current_time

        #LEFT
        if keys[pygame.K_a]:
            # if player_pos.x <= (center_of_window_x - (GAME_WIDTH / 2) + BRICK_WIDTH):
            #     player_pos.x -= 0
            # else:
            player_pos.x -= BRICK_WIDTH
            cursor_index_x = max(1, cursor_index_x - 1)
            last_move_time = current_time
        #RIGHT
        if keys[pygame.K_d]:
            # if player_pos.x >= (center_of_window_x + (GAME_WIDTH / 2) - (BRICK_WIDTH)):
            #     player_pos.x += 0
            # else:
            player_pos.x += BRICK_WIDTH
            cursor_index_x = min(COLUMNS - 1, cursor_index_x + 1)
            last_move_time = current_time
        
    return cursor_index_y, cursor_index_x, last_move_time

def draw_cursor(pos_x, pos_y, width, height, screen): #Make a sprite?
    
    # Base rectangle for the cursor
    rect = pygame.Rect(pos_x, pos_y, width + 4, height + 4)
    cursor_rect_L = rect.move(-width - 2, -2)
    cursor_rect_R = rect.move(- 2, -2)
    
    # Outer outline (slightly larger, Black)
    darker_color = tuple(max(0, c - 40) for c in DG["rgb"])
    outer_outline_L = cursor_rect_L.move(width//2,0).inflate(width, 2)
    outer_outline_R = cursor_rect_R.inflate(2, 2)

    pygame.draw.rect(screen, darker_color, outer_outline_L, width=2)
    # pygame.draw.rect(screen, darker_color, outer_outline_R, width=2)
    
    # Main cursor border (slightly lighter)
    main_color = tuple(max(0, c + 40) for c in DG["rgb"])
    pygame.draw.rect(screen, main_color, cursor_rect_L, width=4)
    pygame.draw.rect(screen, main_color, cursor_rect_R, width=4)

    # Inner outline (slightly smaller, optional)
    lighter_color = tuple(max(0, c + 80) for c in DG["rgb"])
    inner_outline_L = cursor_rect_L.inflate(-2, -2)
    inner_outline_R = cursor_rect_R.inflate(-2, -2) 
    pygame.draw.rect(screen, lighter_color, inner_outline_L, width=2)
    pygame.draw.rect(screen, lighter_color, inner_outline_R, width=2)

    
    # pygame.draw.rect(screen, DG["rgb"], rect.move(-2,-2), width=4)

def initial_run(brick_colors, all_bricks=None, row_from_top = 0):
    field = []
    temp = []
    sprite_grid = []
    for row in range(ROWS):
        temp_row = []
        field_row= []
        sprite_row= []
        for column in range(COLUMNS):
            if row <= row_from_top:
                brick_color = brick_colors[-1]
            else:
                brick_color = brick_colors[random.randrange(0,len(brick_colors)-1)]
            
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
            #print(f"Swapped: {field[row][column-1]['abbr']} with {field[row][column]['abbr']} at ({row}, {column-1}) and ({row}, {column})")
    return temp

def sync_temp_to_sprites(field, temp, sprite_grid, operation_flag=None, swap_occured=None, all_bricks=None):
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
                            old_sprite = sprite_grid[row][col]
                            if not old_sprite:
                                print(f"Missing 'MM' sprite at: {row},{col}")
                            else:
                                match_brick_sprite(old_sprite, MATCH_MADE)
                                new_sprite_grid[row][col] = old_sprite
                                #print(f"Sprite Match: {row},{col}")
                                field[row][col]['abbr'] = 'MM'
                    
                    elif operation_flag == "Empty":
                        if abbr == 'EM': #Temp = EM Happens in seek_for_empty
                            old_sprite = sprite_grid[row][col]
                            if not old_sprite:
                                print(f"Missing 'EM' sprite at: {row},{col}")
                            else:
                                kill_brick_sprite(old_sprite, all_bricks)
                                #print(f"Sprite Killed: {row},{col}")
                                field[row][col]['abbr'] = 'EM'
                                new_sprite_grid[row][col] = old_sprite
                                    
                    elif operation_flag == "Clear":
                        if abbr == 'EM':
                            old_sprite = sprite_grid[row][col]
                            if not old_sprite:
                                print(f"Missing 'CLEAR' sprite at: {row},{col}")
                            else:
                                #print(f"Sprite Cleared: {row},{col}")
                                field[row][col]['abbr'] = 'EM'
                                new_sprite_grid[row][col] = None

                    sprite, old_r, old_c = sprite_lookup[new_sprite_id]
                    sprite.move_to_index(row, col)
                    new_sprite_grid[row][col] = sprite
                    field[row][col] = new_sprite_data #temp_grid is written to field_grid

    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite_grid[r][c] = new_sprite_grid[r][c] #temp_grid is written to sprite_grid

    return field, sprite_grid

def update_grid(field, temp, operation_flag, swap_occured):
    rows = len(temp)
    columns = len(temp[0])    
    score = 0
    if operation_flag == "Match":
        result = check_for_matches(field, temp)
        match_matrix = result['match_matrix']
        score = result['score']
        temp = manage_match_matrix(match_matrix, temp)
        #print(f"Matches checked, and match matrix managed")
    if operation_flag == "Empty":
        temp = clear_matches(field, temp)
        #print(f"Matches cleared")
    if not swap_occured:
        temp = seek_for_empty(field, temp)
        #print(f"Empties searched, and grid phisiscs performed")
    return {'temp': temp, 'score': score}

def check_for_matches(field, temp):
    rows = len(field)
    columns = len(field[0])
   
    match_matrix = [[False for _ in range(columns)] for _ in range(rows)]
    score = 0

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
                    score += 10 * horizontal_match_length + 5 * max(0, horizontal_match_length - 3)
                    #print(f"Horizontal Match of {horizontal_match_length} at row {row}, starting column {column}")
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
                    #print(f"Vertical Match of {vertical_match_length} at column {column}, starting row {row}")
                    row -= vertical_match_length 
                    continue
            row -= 1

    return {'match_matrix': match_matrix, 'score': score}

def manage_match_matrix (match_matrix, temp):
    rows = len(temp)
    columns = len(temp[0])     
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if match_matrix[row][column] == True:
                temp[row][column]['abbr'] = 'MM'
    return temp

def kill_brick_sprite(sprite, all_bricks):
    sprite.start_dying()
    all_bricks.remove(sprite)
    sprite = None

def match_brick_sprite(sprite, color):
    sprite.match_made(color)

def seek_for_empty(field, temp):
    rows = len(field)
    columns = len(field[0])

    for column in range(columns):
        write_row = rows - 1  # Start from the bottom of the column

        # Go from bottom to top, placing non-empty cells into temp from the bottom up
        for row in range(rows - 1, -1, -1):
            if field[row][column]['abbr'] != 'EM':
                temp[write_row][column] = field[row][column]
                write_row -= 1

        # Fill remaining cells in temp with EMPTY
        for r in range(write_row, -1, -1):
            temp[r][column] = EMPTY

    return temp

def seek_for_horizontal_match(field, temp):
    rows = len(field)
    columns = len(field[0])

    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if column + 2 < columns:
                if field[row][column]['abbr'] != 'EM':
                    match_length = 1
                    while column + match_length < columns and field[row][column]['abbr'] == field[row][column + match_length]['abbr']:
                        match_length += 1
                    if match_length >= 3:
                        for i in range(match_length):
                            if temp[row][column + i]['abbr'] == 'MM':
                                pass
                            temp[row][column + i]['abbr'] = 'MM'
                        print(f"Horizontal Match of {match_length} at row {row}, starting column {column}")

def seek_for_vertical_match(field, temp):
    rows = len(field)
    columns = len(field[0])

    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if row >= 2:
                if field[row][column]['abbr'] != 'EM':
                    match_length = 1
                    while row - match_length >= 0 and field[row][column]['abbr'] == field[row - match_length][column]['abbr']:
                        match_length += 1
                    if match_length >= 3:
                        for i in range(match_length):
                            if temp[row - i][column]['abbr'] == 'MM':
                                pass
                            temp[row - i][column]['abbr'] = 'MM'
                        print(f"Vertical Match of {match_length} at column {column}, starting row {row}")
    return temp

def clear_matches(field, temp):
    rows = len(field)
    columns = len(field[0])

    global match_made
    for row in range(rows-1, -1, -1):
        for column in range(columns):
            if field[row][column]['abbr'] == 'MM':
                temp[row][column]['abbr'] = 'EM'

                match_made = True
    return temp

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
    #print(f"Field: {field_export}")

    return field_export, temp_export, sprite_export, match_matrix_export

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

def print_data_to_console(field=None, temp=None, sprite_grid=None, all_bricks=None,match_matrix=None):
    field_export, temp_export, sprite_export, match_matrix_export = get_grid_data(field if field is not None else [], temp if temp is not None else [], sprite_grid if sprite_grid is not None else [], match_matrix if match_matrix is not None else [])
    #all_bricks_grid = print_all_bricks(all_bricks if all_bricks is not None else [])
    export_data({'field': field_export, 'temp': temp_export, 'sprite': sprite_export,'match_matrix': match_matrix_export})

def print_all_bricks(all_bricks):
    rows = len(all_bricks)
    columns = len(all_bricks[0])

    grid = [[None for _ in range(columns)] for _ in range(rows)]
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

def update_sprites(sprite_grid):
    all_animations_complete = True
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            if sprite:
                sprite.update()
                if sprite.is_animating():
                    #print(f"Sprite at ({r}, {c}) is still animating.")
                    all_animations_complete = False
    #print(f"Animations Complete: {all_animations_complete}")
    return all_animations_complete

def draw_sprites(sprite_grid, offset, surface):
    for r in range(len(sprite_grid)):
        for c in range(len(sprite_grid[r])):
            sprite = sprite_grid[r][c]
            if sprite:
                sprite.draw(offset, surface)

def add_new_row(field=None, temp=None, sprite_grid=None, brick_colors = COLORS_LIST, all_bricks=None):
    columns = len(temp[0])

    new_row_index = len(sprite_grid)
    new_temp_row = []
    new_sprite_row = []
    
    for column in range(columns):
        brick_color = random.choice(brick_colors)
        brick_data = brick_color.copy()
        brick_data["id"] = str(uuid.uuid4())
        brick = Brick(brick_data, new_row_index, column)

        if all_bricks is not None:
            all_bricks.add(brick)

        new_temp_row.append(brick_data)
        new_sprite_row.append(brick)

    temp.append(new_temp_row)
    sprite_grid.append(new_sprite_row)
    
    return temp, sprite_grid

def check_game_over(field, current_row):
    for column in range(len(field[0])):
        if field[current_row+1][column]['abbr'] != 'EM':
            return True # Game over condition met
    return False  # Game is still ongoing

def draw_vertical_gradient(surface, start_alpha=0, finish_alpha=255, rect=None, step_height=1):
    x, y, width, height = rect
    steps = height // step_height
    alpha_step = (finish_alpha - start_alpha) / max(steps, 1)

    for i in range(steps):
        current_alpha = int(start_alpha + i * alpha_step)
        block = pygame.Surface((width, step_height), pygame.SRCALPHA)
        block.fill(DG["rgb"] + (current_alpha,))
        surface.blit(block, (x, y + i * step_height))

