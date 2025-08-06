<h1>BRICKS</h1>
<h2>Video Demo:</h2>
<p>INSERT URL</p>
<h2>Description:</h2>
<p>Bricks is a browser playable puzzle game built with Python, using Pygame for game mechanics and Pygbag to bring it online.</p>
<dt><b>The game has 3 simple mechanics:</b></dt>
<dd>Cursor movement: UP, DOWN, LEFT, RIGHT.</dd>
<dd>Swap the two bricks inside the cursor.</dd>
<dd>3 in a row is a match.</dd>

<p></p>
<p><b>There are 2 game modes:</b></p>
<b>Endless:</b>
<p>The bricks continuously raise from the bottom of the screen. You must clear the bricks before they hit the top!</p>

<p></p>
<b>Puzzle:</b>
<p>Move through a series of pregressivly harder puzzles. The goal is to clear all the bricks in the allowed number of moves.</p>

<p></p>
<b>Before running the code:</b>
<dd>pip install -r requirements.txt</dd>
<dd>nav to src/main.py</dd>

<h3>Bricks file structure:</h3>

```
src/
    build/
        web/
    _init_.py
    game_screen.py
    home_screen_button.py
    home_screen.py (not used)
    index.html
    main.py
    pause_screen.py
    puzzle_grids.py
    puzzle_select_screen.py
    pythonic.py
    screen_manager.py
    settings.py
grid_data.txt
index.html
LICENSE
player_data.json
requirements.txt
setup.py
specifiction
```

This file structure is typical to pygame.

src/ is the source folder

build/ is a generated folder (that probably doesnt need to be inlcluded in the repositiry, because pygbag will create one everytime an update is pushed)

init.py could technically be omitted, as Python 3.3 and higher doesnt require it.

All the "screen.py" files are for each page of the game. Each scene is its own class with a similar structure inherited from the Screen class in settings.py.
They each have a handle_events, update, draw functions, as required for the class and the MAIN loop.

index.html is a modified version that is produced by pygbag to reference the most current documets.

main.py is the MAIN game loop, its a while loop that continues until the game is quit.

In side the MAIN loop it looks at checks for which instance of the screen the user is on. and will loop through that screens handle_events, update, and draw.

pythonic.py is a file created to bypass an error from pygbag saying it was missing.

settings.py is where the global game settings, graphics, brick class and player data is setup.

License is a typical MIT licence.

player_data.json is used for local storage.

requirements.txt contains a list of the libraries and modules required to download to run the game on your local computer.

setup.py is tyical to pygame, but is empty.






