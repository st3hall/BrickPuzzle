from settings import *
from puzzle_grids import *

import pygame
import random
import copy
import json
from screen_manager import ScreenManager
#from home_screen import HomeScreen
from pause_screen import PauseScreen
from game_screen import GameScreen
from puzzle_screen import PuzzleScreen
from home_screen_buttons import HomeScreen
import asyncio #for online game functionality
from js import localStorage


pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
manager = ScreenManager()
manager.set_screen(HomeScreen(manager, player_data=PlayerData()))

async def main():
    run = True
    game_started = False
    game_paused = False

    while run:
        events = pygame.event.get()
        manager.handle_events(events)
        
        for event in events:
            if event.type == pygame.QUIT:
                run = False           

            current_screen = manager.current_screen

            if isinstance(current_screen, HomeScreen):
                if current_screen.game_started:
                    game_started = True
                    game_paused = False
                    manager.set_screen(GameScreen(manager))

            elif isinstance(current_screen, PauseScreen):
                if not current_screen.game_paused:
                    game_paused = False
    
            elif isinstance(current_screen, GameScreen):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print(f"Key Down")
                    game_paused = True
                    manager.set_screen(PauseScreen(manager))
                    print("You should be paused")
            
            elif isinstance(current_screen, PuzzleScreen):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print(f"Key Down")
                    game_paused = True
                    manager.set_screen(PauseScreen(manager))
                    print("You should be paused")

        # Update and draw the current screen 
        manager.update()
        manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
        
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
