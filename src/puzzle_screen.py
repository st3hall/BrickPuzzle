from settings import *
import pygame
import random
from home_screen_buttons import *
from game_screen import *
from puzzle_grids import *
from puzzle_select_screen import PuzzleSelectScreen


class PuzzleScreen(Screen):
    def __init__(self, manager, puzzle_id, player_data):
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
        self.clock = pygame.time.Clock()
        self.moves_count = 0
        self.moves_available = 0
        self.puzzle_number = puzzle_id
        dt = self.clock.tick(60)/1000
        
        self.player_data.load()
        self.total_puzzles = len(puzzle_dict)
                
        
        # Initialize your game field
        self.field, self.temp, self.sprite_grid, self.all_bricks, self.moves_available = initial_run_puzzle(COLORS_LIST, self.all_bricks,self.puzzle_number)

        result = update_grid(self.field, self.temp, "Match", False)
        self.field = result['temp']
        self.field, self.sprite_grid = sync_temp_to_sprites(self.field, self.temp, self.sprite_grid, "Clear", False)

                #Retry Button   
        font_small = pygame.font.SysFont(DEFAULT_FONT, 18)
        button_width = 80
        button_height = 30
        center_x = (WINDOW_WIDTH - button_width) // 2
        button_y_start = 20
        button_spacing = button_width //2 + 5

        self.buttons = [
            Button((center_x - (button_spacing), button_y_start, button_width, button_height), "Select", self.return_to_select, font_small, G['rgb'], tuple(min(255, c + 30) for c in G['rgb'])),
            Button((center_x + (button_spacing), button_y_start, button_width, button_height), "Restart", self.retry_puzzle, font_small, R['rgb'], tuple(min(255, c + 30) for c in R['rgb']))
        ]
        
    def return_to_select(self):
        from puzzle_select_screen import PuzzleSelectScreen
        self.manager.set_screen(PuzzleSelectScreen(self.manager, self.player_data))

    def retry_puzzle(self):
        self.moves_count = 0
        self.field, self.temp, self.sprite_grid, self.all_bricks, self.moves_available = initial_run_puzzle(COLORS_LIST, self.all_bricks, self.puzzle_number)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(event.pos)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.cursor_swap_done:
                    self.temp = cursor_swap_input(self.field, self.temp, self.cursor_index_x, self.cursor_index_y)
                    self.cursor_swap_done = True
                    self.swap_occurred = True
                    self.moves_count += 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.cursor_swap_done = False

    def update(self): 
        dt = self.clock.tick(60) / 1000   
        keys = pygame.key.get_pressed()
        completed_puzzles = self.player_data.puzzles

        self.cursor_index_y, self.cursor_index_x, self.last_move_time = update_cursor_position(
            keys, self.player_pos, self.cursor_index_x, self.cursor_index_y, self.last_move_time, self.move_delay
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
                self.next_state = "resolving"
                self.operation_cycle += 1
            
            for r in range(len(self.sprite_grid)):
                for c in range(len(self.sprite_grid[r])):
                    sprite = self.sprite_grid[r][c]
                    if sprite:
                        sprite.update()
          

        if hasattr(self, 'next_state'):
            self.state = self.next_state
            del self.next_state
        
        result = check_if_done(self.field, self.moves_count, self.moves_available)

        if result in ["complete", "retry"]:
            if result == "complete":
                print(f"Puzzle {self.puzzle_number} completed!")
                self.player_data.complete_puzzle(self.puzzle_number)
                self.puzzle_number += 1
                self.moves_count = 0

                completed_puzzles = self.player_data.puzzles  # Make sure this is updated
                if len(completed_puzzles) == self.total_puzzles:
                    print("All puzzles completed! Returning to home screen.")
                    self.manager.set_screen(PuzzleSelectScreen(self.manager, self.player_data))
                    return

                # Check if the next puzzle exists
                if self.puzzle_number >= self.total_puzzles:
                    # Find the first puzzle index that hasn't been completed
                    for i in range(self.total_puzzles):
                        if i not in completed_puzzles:
                            self.puzzle_number = i
                            break

            elif result == "retry":
                print("Retrying puzzle...")

            self.moves_count = 0
            self.field, self.temp, self.sprite_grid, self.all_bricks, self.moves_available = initial_run_puzzle(
                COLORS_LIST, self.all_bricks, self.puzzle_number
            )
    
    def draw(self, surface):
        surface.blit(self.background, (0,0)) #(-center_of_window_x, -center_of_field_y))
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
        #surface.blit(opaque_surface, (0, WINDOW_HEIGHT - (CELL_SIZE + PADDING)))#bottom

        moves_left = self.moves_available - self.moves_count
        self.clock.tick(60)
        fps = str(int(self.clock.get_fps()))
        font = pygame.font.SysFont(DEFAULT_FONT, 20)
        text = font.render(f"Moves: {moves_left}", True, L['rgb'])
        text_rect = text.get_rect(topleft=(10, 20))
        surface.blit(text, text_rect)

        font = pygame.font.SysFont(DEFAULT_FONT, 20)
        text = font.render(f"Puzzle #: {self.puzzle_number}", True, L['rgb'])
        text_rect = text.get_rect(topright=(WINDOW_WIDTH-10, 20))
        surface.blit(text, text_rect)
        
        for button in self.buttons:
            button.draw(surface)
       
def get_puzzle(puzzle_dict, number=1):
    key = f"puzzle_{number}"
    puzzle = puzzle_dict.get(key)
    if puzzle:
        return puzzle["board"], puzzle["max_moves"]
    else:
        return None, None
   
def initial_run_puzzle(brick_colors, all_bricks=None, puzzle_number=1):
    board, moves = get_puzzle(puzzle_dict, puzzle_number)
    #print(puzzle)
    color_lookup = {color["abbr"]: color for color in brick_colors}
    #print(color_lookup)
    field = []
    temp = []
    sprite_grid = []
    for row in range(ROWS):
        temp_row = []
        field_row= []
        sprite_row= []
        for column in range(COLUMNS):
            #i want brick color to return the dict associated with the abbr at that location
            abbr = board[row][column]
           #print(f"Row:{row}, Column:{column}, abbr: {abbr}")
            brick_color = color_lookup[abbr]
            #print(f"Brick Color:{brick_color}")
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

    return field, temp, sprite_grid, all_bricks, moves

def check_if_done(field, moves, moves_available):
    if moves <= moves_available:
        for row in range(len(field)):
            for column in range(len(field[row])):
                if field[row][column]['abbr'] != 'EM':
                    return False
        return "complete"
    else:
        print("No more moves available. Retry?")
        return "retry"
     
def load_new_puzzle(self, puzzle_dict, next_number):
    key = f"puzzle_{next_number}"
    if key in puzzle_dict:
        self.field = puzzle_dict[key]["board"]
        self.moves_available = puzzle_dict[key]["max_moves"]
        self.puzzle_number = next_number
        self.moves_count = 0
        # Optionally reset any animations, timers, or UI elements
        print(f"Loaded puzzle {next_number}")
    else:
        print("No more puzzles available.")
        self.manager.set_screen(HomeScreen(self.manager))  # Or any end screen
