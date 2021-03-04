
# Grey Team: Dungeon-Game
A space-themed dungeon game created by an agile software engineering team for a uni project. 

## Install guide
1. Ensure you have Python 3 installed on your machine
1. Clone the code of the branch you want to edit to your machine using `git clone`.
2. Using the command line switch to the same directory as the project. Run `pip install -r requirements.txt` to install 
    project requirements. 
3. To run the main game run `python main.py`

## Tutorial list

- [Multi-room maps](https://arcade.academy/examples/sprite_rooms.html#sprite-rooms)
- [Change Main program to use views](https://arcade.academy/tutorials/views/index.html#view-tutorial)
- [Scrolling maps](https://arcade.academy/examples/sprite_move_scrolling.html?highlight=scrolling)
- [Tiled map with levels](https://arcade.academy/examples/sprite_tiled_map_with_levels.html#sprite-tiled-map-with-levels)

## Map creation
Maps can be created using the [Tiled map editor](https://www.mapeditor.org/). Each map should
sit in the `maps` directory and a guide for drawing levels [can be found here](https://arcade.academy/examples/platform_tutorial/index.html#platformer-part-eight). 

Currently maps only have walls, which should be added in a layer called `Walls`. Other objects can be added in other 
layers. Sprites are embedded in the map creation process with Tiled. 

