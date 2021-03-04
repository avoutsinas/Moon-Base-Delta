import os
import arcade
from arcade.experimental.lights import Light, LightLayer
import constants
import GlobalVariables as GV
import time
from Dialogue import DialogueText, TitleText
from arcade.gui import UIManager, UIGhostFlatButton
from Warnings import warning, dialogue

from Views import narrativeTemplate, End_Game_Screen, Game_Over_Screen, MathSequenceGame, In_Game_Menu, FakeCodeGame, \
    AnagramGame
import numpy as np

# Global variable which decides where the AI should be drawn
discoveredAI = False

# An array of 16 booleans defining if the player has reached a dialogue point
reachedDialogue = [False, False, False, False,
                   False, False, False, False,
                   False, False, False, False,
                   False, False, False, False
                   ]

reachedLight = False

# Global variable which has value True if spacedungeon is the current view and False if not
# This global variable is used to correctly stop in-game Music
spaceDungeonIsView = True

# Modules
stimpackModule = False
oxygenTankModule = False
radiationShieldModule = False
exoskeletonModule = False


class SpaceDungeon(arcade.View):
    def __init__(self):
        """
        Initializer function
        """
        super().__init__()

        self.current_level = 0
        self.rooms = None
        self.player = None
        self.player_list = None
        self.physics_engine = None
        self.paused = False
        self.all_sprites = arcade.SpriteList()

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Light related
        self.light_layer_normal = None
        self.light_layer_adjusted = None
        self.player_light_normal = None
        self.player_light_adjusted = None

        # UI Manager
        self.ui_manager = UIManager()

        # Music Related
        self.music_list = []
        self.current_song = 0
        self.music = None

        # Keep track of player health and oxygen
        self.health = 30
        self.oxygen = 100
        # health bar dimentions and position parameters
        self.healthbar_padding = 8
        self.healthbar_height = 30
        self.healthbar_width = 180
        # oxygen bar dimentions and position parameters
        self.oxbar_padding = 8
        self.oxbar_height = 30
        self.oxbar_width = 180

        self.stimpacks = 0
        self.oxycanisters = 0

        # Sound effects
        self.oxygen_refill_sound = arcade.load_sound(os.path.join("Sounds", "oxygen_refill.mp3"))
        self.task_start = arcade.load_sound(os.path.join("Sounds", "task_start.mp3"))
        self.task_unlock = arcade.load_sound(os.path.join("Sounds", "task_unlock.mp3"))
        self.task_fail = arcade.load_sound(os.path.join("Sounds", "task_fail.mp3"))
        self.task_try = arcade.load_sound(os.path.join("Sounds", "task_try.mp3"))
        self.upgrade = arcade.load_sound(os.path.join("Sounds", "upgrade.mp3"))
        self.button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        # Generics
        arcade.set_background_color(arcade.color.BLACK)
        self.paused = False

        # Player setup
        self.player = arcade.Sprite(os.path.join('Custom_graphics', 'player_model.png'), constants.MODEL_SCALING)
        self.player.center_y = constants.SCREEN_HEIGHT / 2
        self.player.left = constants.SCREEN_WIDTH / 2
        self.all_sprites.append(self.player)

        self.load_level(self.current_level)
        self.view_left = 0
        self.view_bottom = 0

        # Light related

        self.light_layer_normal = LightLayer(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.light_layer_normal.set_background_color(arcade.color.BLACK)
        self.light_layer_adjusted = LightLayer(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.light_layer_adjusted.set_background_color(arcade.color.BLACK)

        radius_normal = 800
        radius_adjusted = 125
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light_normal = Light(0, 0, radius_normal, color, mode)
        self.light_layer_normal.add(self.player_light_normal)
        self.player_light_adjusted = Light(0, 0, radius_adjusted, color, mode)
        self.light_layer_adjusted.add(self.player_light_adjusted)

        self.ui_manager.purge_ui_elements()

        # List of music
        self.music_list = [os.path.join('Music', 'in_game', 'Backdoor_Exit.mp3'),
                           os.path.join('Music', 'in_game', 'Detector.mp3'),
                           os.path.join('Music', 'in_game', 'Counterflow.mp3')]
        # Array index of what to play
        self.current_song = 0
        # Play the song
        self.play_song()

    def load_level(self, level):

        my_map = arcade.tilemap.read_tmx(f"maps/level_{level}.tmx")

        'Loads layers'
        # Test layer
        # self.Keypad_1_test = arcade.tilemap.process_layer(my_map,
        #      'Test/Keypad_1',
        #     constants.MAP_SCALING,
        #    use_spatial_hash=True)

        # self.Keypad_2_test = arcade.tilemap.process_layer(my_map,
        #       'Test/Keypad_2',
        #      constants.MAP_SCALING,
        #     use_spatial_hash=True)

        # self.Keypad_3_test = arcade.tilemap.process_layer(my_map,
        #     'Test/Keypad_3',
        #    constants.MAP_SCALING,
        #   use_spatial_hash=True)

        # self.test_text = arcade.tilemap.process_layer(my_map,
        #   'Test/Text',
        #  constants.MAP_SCALING,
        # use_spatial_hash=True)

        # Background

        self.floor_list = arcade.tilemap.process_layer(my_map,
                                                       'Background/Floor',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      'Background/Walls',
                                                      constants.MAP_SCALING,
                                                      use_spatial_hash=True)

        self.object_list = arcade.tilemap.process_layer(my_map,
                                                        'Background/Objects',
                                                        constants.MAP_SCALING,
                                                        use_spatial_hash=False)

        # Doors

        self.door_0 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_1',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_1 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_med',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_2 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_central',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_3 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_airlock',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_5 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_lab',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_7 = arcade.tilemap.process_layer(my_map,
                                                   'Doors/Door_security',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.door_server1 = arcade.tilemap.process_layer(my_map,
                                                         'Doors/Door_server1',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        self.door_server2 = arcade.tilemap.process_layer(my_map,
                                                         'Doors/Door_server2',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        self.door_server3 = arcade.tilemap.process_layer(my_map,
                                                         'Doors/Door_server3',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        # Keypads

        self.keypad_0 = arcade.tilemap.process_layer(my_map,
                                                     'Keypads/Keypad_1',
                                                     constants.MAP_SCALING,
                                                     use_spatial_hash=True)

        self.keypad_0_open = arcade.tilemap.process_layer(my_map,
                                                          'Keypads/Keypad_1_open',
                                                          constants.MAP_SCALING,
                                                          use_spatial_hash=True)

        self.keypad_1 = arcade.tilemap.process_layer(my_map,
                                                     'Keypads/Keypad_med',
                                                     constants.MAP_SCALING,
                                                     use_spatial_hash=True)

        self.keypad_1_open = arcade.tilemap.process_layer(my_map,
                                                          'Keypads/Keypad_med_open',
                                                          constants.MAP_SCALING,
                                                          use_spatial_hash=True)

        self.keypad_2 = arcade.tilemap.process_layer(my_map,
                                                     'Keypads/Keypad_central',
                                                     constants.MAP_SCALING,
                                                     use_spatial_hash=True)

        self.keypad_2_open = arcade.tilemap.process_layer(my_map,
                                                          'Keypads/Keypad_central_open',
                                                          constants.MAP_SCALING,
                                                          use_spatial_hash=True)

        self.keypad_5 = arcade.tilemap.process_layer(my_map,
                                                     'Keypads/Keypad_lab',
                                                     constants.MAP_SCALING,
                                                     use_spatial_hash=True)

        self.keypad_5_open = arcade.tilemap.process_layer(my_map,
                                                          'Keypads/Keypad_lab_open',
                                                          constants.MAP_SCALING,
                                                          use_spatial_hash=True)

        self.keypad_server1 = arcade.tilemap.process_layer(my_map,
                                                           'Keypads/Keypad_server1',
                                                           constants.MAP_SCALING,
                                                           use_spatial_hash=True)

        self.keypad_server1_open = arcade.tilemap.process_layer(my_map,
                                                                'Keypads/Keypad_server1_open',
                                                                constants.MAP_SCALING,
                                                                use_spatial_hash=True)

        # Computers

        self.comp_2 = arcade.tilemap.process_layer(my_map,
                                                   'Computers/Chief',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.comp_3 = arcade.tilemap.process_layer(my_map,
                                                   'Computers/Security',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.comp_8 = arcade.tilemap.process_layer(my_map,
                                                   'Computers/Server',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        # Terminals

        self.terminal_6 = arcade.tilemap.process_layer(my_map,
                                                       'Terminals/reactor',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.terminal_7 = arcade.tilemap.process_layer(my_map,
                                                       'Terminals/security',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        # Stimpacks

        self.stimpack_1 = arcade.tilemap.process_layer(my_map,
                                                       'Stimpacks/Stimpack_1',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.stimpack_2 = arcade.tilemap.process_layer(my_map,
                                                       'Stimpacks/Stimpack_2',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.stimpack_3 = arcade.tilemap.process_layer(my_map,
                                                       'Stimpacks/Stimpack_3',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.stimpack_4 = arcade.tilemap.process_layer(my_map,
                                                       'Stimpacks/Stimpack_4',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        # Warnings

        self.radiation = arcade.tilemap.process_layer(my_map,
                                                      'PlayerBlock/Radiation',
                                                      constants.MAP_SCALING,
                                                      use_spatial_hash=True)

        self.pressure = arcade.tilemap.process_layer(my_map,
                                                     'PlayerBlock/Pressure',
                                                     constants.MAP_SCALING,
                                                     use_spatial_hash=True)

        # Dialogue

        self.dialogue_1 = arcade.tilemap.process_layer(my_map,
                                                       'Dialogue/Dialogue_1',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.dialogue_2 = arcade.tilemap.process_layer(my_map,
                                                       'Dialogue/Dialogue_2',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.dialogue_3 = arcade.tilemap.process_layer(my_map,
                                                       'Dialogue/Dialogue_3',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        # Dialogue 4 is caused by an interaction

        self.dialogue_5 = arcade.tilemap.process_layer(my_map,
                                                       'Dialogue/Dialogue_5',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        # Dialogue 6 is caused by an interaction

        # Dialogue 7 is caused by an interaction

        # Dialogue 8 is caused by an interaction

        self.dialogue_9 = arcade.tilemap.process_layer(my_map,
                                                       'Dialogue/Dialogue_9',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        # Dialogue 10 is caused by an interaction

        self.dialogue_11 = arcade.tilemap.process_layer(my_map,
                                                        'Dialogue/Dialogue_11',
                                                        constants.MAP_SCALING,
                                                        use_spatial_hash=True)

        self.dialogue_12 = arcade.tilemap.process_layer(my_map,
                                                        'Dialogue/Dialogue_12',
                                                        constants.MAP_SCALING,
                                                        use_spatial_hash=True)

        # Dialogue 13 is caused by an interaction

        # Dialogue 14 is caused by an interaction

        # Dialogue 15 is caused by an interaction

        # Dialogue 16 is caused by an interaction

        # Other

        self.text = arcade.tilemap.process_layer(my_map,
                                                 'Text',
                                                 constants.MAP_SCALING,
                                                 use_spatial_hash=True)

        self.Mainframe = arcade.tilemap.process_layer(my_map,
                                                      'Mainframe',
                                                      constants.MAP_SCALING,
                                                      use_spatial_hash=True)

        self.lights = arcade.tilemap.process_layer(my_map,
                                                   'Lights/Lights',
                                                   constants.MAP_SCALING,
                                                   use_spatial_hash=True)

        self.fuses = arcade.tilemap.process_layer(my_map,
                                                  'Lights/Fuse_Boxes',
                                                  constants.MAP_SCALING,
                                                  use_spatial_hash=True)

        self.PeripheralAI = arcade.tilemap.process_layer(my_map,
                                                         'PeripheralAI',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        self.Moon = arcade.tilemap.process_layer(my_map,
                                                 'Background/Moon',
                                                 constants.MAP_SCALING,
                                                 use_spatial_hash=True)

        self.broken_valve = arcade.tilemap.process_layer(my_map,
                                                         'Broken_Valve',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        self.escapePods = arcade.tilemap.process_layer(my_map,
                                                       'EscapePods/EscapePods',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.interactables = arcade.tilemap.process_layer(my_map,
                                                          'Interactables',
                                                          constants.MAP_SCALING,
                                                          use_spatial_hash=True)

        # Module items
        self.oxygenModule = arcade.tilemap.process_layer(my_map,
                                                         'Modules/OxygenTankModule',
                                                         constants.MAP_SCALING,
                                                         use_spatial_hash=True)

        self.stimModule = arcade.tilemap.process_layer(my_map,
                                                       'Modules/StimpackModule',
                                                       constants.MAP_SCALING,
                                                       use_spatial_hash=True)

        self.radiationModule = arcade.tilemap.process_layer(my_map,
                                                            'Modules/RadiationShieldModule',
                                                            constants.MAP_SCALING,
                                                            use_spatial_hash=True)

        self.exoModule = arcade.tilemap.process_layer(my_map,
                                                      'Modules/ExoskeletonModule',
                                                      constants.MAP_SCALING,
                                                      use_spatial_hash=True)

        self.collision_objects = arcade.SpriteList()

        ' Adds layers to either object_list or collison_objects so player collides with them'

        # Background
        for i in self.wall_list:
            self.collision_objects.append(i)
        for i in self.object_list:
            self.collision_objects.append(i)
        # Doors
        for i in self.door_0:
            self.collision_objects.append(i)
        for i in self.door_1:
            self.collision_objects.append(i)
        for i in self.door_2:
            self.collision_objects.append(i)
        for i in self.door_3:
            self.collision_objects.append(i)
        for i in self.door_5:
            self.collision_objects.append(i)
        for i in self.door_7:
            self.collision_objects.append(i)
        for i in self.door_server1:
            self.collision_objects.append(i)
        for i in self.door_server3:
            self.collision_objects.append(i)

        # Keypads
        for i in self.keypad_0:
            self.object_list.append(i)
        for i in self.keypad_1:
            self.object_list.append(i)
        for i in self.keypad_2:
            self.object_list.append(i)
        for i in self.keypad_5:
            self.object_list.append(i)
        for i in self.keypad_server1:
            self.object_list.append(i)
        # Computers
        for i in self.comp_2:
            self.object_list.append(i)
        for i in self.comp_3:
            self.object_list.append(i)
        for i in self.comp_8:
            self.object_list.append(i)
        # Terminals
        for i in self.terminal_6:
            self.object_list.append(i)
        for i in self.terminal_7:
            self.object_list.append(i)
        # Stimpacks
        for i in self.stimpack_1:
            self.object_list.append(i)
        for i in self.stimpack_2:
            self.object_list.append(i)
        for i in self.stimpack_3:
            self.object_list.append(i)
        for i in self.stimpack_4:
            self.object_list.append(i)
        # Dialogue
        for i in self.dialogue_1:
            self.object_list.append(i)
        for i in self.dialogue_2:
            self.object_list.append(i)
        for i in self.dialogue_3:
            self.object_list.append(i)
        for i in self.dialogue_5:
            self.object_list.append(i)
        for i in self.dialogue_9:
            self.object_list.append(i)
        for i in self.dialogue_11:
            self.object_list.append(i)
        for i in self.dialogue_12:
            self.object_list.append(i)
        # Other
        for i in self.PeripheralAI:
            self.object_list.append(i)
        for i in self.lights:
            self.object_list.append(i)
        for i in self.fuses:
            self.object_list.append(i)
        for i in self.broken_valve:
            self.object_list.append(i)
        for i in self.escapePods:
            self.object_list.append(i)
        # Modules
        for i in self.oxygenModule:
            self.object_list.append(i)
        for i in self.stimModule:
            self.object_list.append(i)
        for i in self.exoModule:
            self.object_list.append(i)
        for i in self.radiationModule:
            self.object_list.append(i)
        for i in self.interactables:
            self.object_list.append(i)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_0(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_0:
            self.collision_objects.remove(i)
        for i in self.keypad_0:
            self.object_list.remove(i)
        for i in self.keypad_0_open:
            self.object_list.append(i)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_1(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_1:
            self.collision_objects.remove(i)
        for i in self.keypad_1:
            self.object_list.remove(i)
        for i in self.keypad_1_open:
            self.object_list.append(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_2(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_2:
            self.collision_objects.remove(i)
        for i in self.keypad_2:
            self.object_list.remove(i)
        for i in self.keypad_2_open:
            self.object_list.append(i)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def close_door_2(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_2:
            self.collision_objects.append(i)
        for i in self.keypad_2:
            self.object_list.append(i)
        for i in self.keypad_2_open:
            self.object_list.remove(i)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_3(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_3:
            self.collision_objects.remove(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_5(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_5:
            self.collision_objects.remove(i)
        for i in self.keypad_5:
            self.object_list.remove(i)
        for i in self.keypad_5_open:
            self.object_list.append(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_7(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_7:
            self.collision_objects.remove(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def close_door_server2(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_server2:
            self.collision_objects.append(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_9(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_server1:
            self.collision_objects.remove(i)
        for i in self.keypad_server1:
            self.object_list.remove(i)
        for i in self.keypad_server1_open:
            self.object_list.append(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    def open_door_server3(self):
        arcade.set_viewport(self.view_left,
                            constants.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            constants.SCREEN_HEIGHT + self.view_bottom)
        for i in self.door_server3:
            self.collision_objects.remove(i)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.collision_objects)

    '                              ***Helper Functions***'

    "This function triggers the MathSequenceGame minigame"

    def trigger_math_sequence_game(self):
        arcade.play_sound(self.task_start, volume=constants.MUSIC_VOLUME / 25)
        self.stop_player_sprite()
        maths_game_view = MathSequenceGame.MyView(self)
        self.window.show_view(maths_game_view)

    "This function triggers the FakeCodeGame minigame"

    def trigger_fake_code_game(self):
        arcade.play_sound(self.task_start, volume=constants.MUSIC_VOLUME / 25)
        self.stop_player_sprite()
        fcg_game_view = FakeCodeGame.MyView(self)
        self.window.show_view(fcg_game_view)

    "This function triggers the FakeCodeGame minigame"

    def trigger_anagram_game(self):
        arcade.play_sound(self.task_start, volume=constants.MUSIC_VOLUME / 25)
        self.stop_player_sprite()
        anagram_game_view = AnagramGame.MyView(self)
        self.window.show_view(anagram_game_view)

    "This function uses a dialogue and title variable "
    "from Dialogue.py to trigger a specific narrative."
    "The player movement is also set to 0 to avoid bugs."

    def trigger_narrative(self, dialogue, title):
        # Daniels changes
        # When dialogue has been triggered appends global variable with that dialogue point
        if title == warning.Title_Pressure or title == warning.Title_Radiation:
            pass
        else:
            GV.dialogue = dialogue
            GV.title = title
        narrative_template = narrativeTemplate.MyView(self, dialogue, title)
        self.window.show_view(narrative_template)
        self.stop_player_sprite()

    "This function triggers the In_Game_Menu_View"

    def trigger_in_game_menu_view(self):
        self.stop_player_sprite()
        self.window.show_view(In_Game_Menu.MyView(self))

    "This function triggers the End_Game_View"

    def trigger_endgame_view(self):
        global spaceDungeonIsView
        end_game = End_Game_Screen.MyView()
        self.window.show_view(end_game)
        self.music.stop()
        spaceDungeonIsView = False

    "This function triggers the Game_Over_Screen"

    def trigger_gameover_view(self):
        global spaceDungeonIsView
        game_over = Game_Over_Screen.MyView()
        self.window.show_view(game_over)
        self.music.stop()
        spaceDungeonIsView = False

    """This function stops the player from moving. 
    It is called when another view is triggered."""

    def stop_player_sprite(self):
        self.player.change_x = 0
        self.player.change_y = 0

    'Adds an amount of oxygen to self.oxygen'

    def add_oxygen(self, amount):
        while amount >= 0 and self.oxygen < 100:
            self.oxygen += 1
            amount -= 1
        arcade.play_sound(self.oxygen_refill_sound, volume=constants.MUSIC_VOLUME / 10)

    '                              ***Music Functions***'

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        global spaceDungeonIsView
        self.current_song += 1
        if self.current_song >= len(self.music_list) and spaceDungeonIsView:
            self.current_song = 0
        print(f"Advancing song to {self.current_song}.")

    def stop_song(self):
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        print(f"Playing {self.music_list[self.current_song]}")
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(constants.MUSIC_VOLUME / 30)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def on_draw(self):
        arcade.start_render()
        self.Moon.draw()
        self.floor_list.draw()
        self.wall_list.draw()
        self.object_list.draw()
        self.text.draw()
        self.all_sprites.draw()

        if reachedLight == True:
            with self.light_layer_adjusted:
                self.Moon.draw()
                self.wall_list.draw()
                self.floor_list.draw()
                self.wall_list.draw()
                self.object_list.draw()
                self.Mainframe.draw()

                '''Draws AI robot in the peripheral room, but it will be removed and placed in the central command
                room at the right time'''
                if not discoveredAI:
                    self.PeripheralAI.draw()
                else:
                    self.Mainframe.draw()

                self.escapePods.draw()

                if not oxygenTankModule:
                    self.oxygenModule.draw()

                if not stimpackModule:
                    self.stimModule.draw()

                if not radiationShieldModule:
                    self.radiationModule.draw()

                if not exoskeletonModule:
                    self.exoModule.draw()

                # Doors

                if reachedDialogue[10]:
                    self.door_server2.draw()

                if not reachedDialogue[10]:
                    self.door_server3.draw()

                self.text.draw()
                self.interactables.draw()
                self.all_sprites.draw()
                self.light_layer_adjusted.draw(ambient_color=constants.AMBIENT_COLOUR)
        else:
            with self.light_layer_normal:
                self.Moon.draw()
                self.wall_list.draw()
                self.floor_list.draw()
                self.wall_list.draw()
                self.object_list.draw()
                self.Mainframe.draw()
                # Doors
                if not GV.object[0][0]:
                    self.door_0.draw()

                if not GV.object[1][0] or not GV.object[1][1]:
                    self.door_1.draw()

                if not GV.object[2][0] or not GV.object[2][1] or GV.closed_door_central:
                    self.door_2.draw()

                if not GV.object[3][0] or not GV.object[3][1]:
                    self.door_3.draw()

                if not GV.object[5][0] or not GV.object[5][1]:
                    self.door_5.draw()

                if not GV.object[7][0] or not GV.object[7][1]:
                    self.door_7.draw()

                if not GV.object[9][0] or not GV.object[9][1]:
                    self.door_server1.draw()

                if reachedDialogue[10]:
                    self.door_server2.draw()

                if not reachedDialogue[10]:
                    self.door_server3.draw()

                '''Draws AI robot in the peripheral room, but it will be removed and placed in the central command
                room at the right time'''
                if not discoveredAI:
                    self.PeripheralAI.draw()
                else:
                    self.Mainframe.draw()

                self.escapePods.draw()

                self.text.draw()
                self.interactables.draw()

                if not oxygenTankModule:
                    self.oxygenModule.draw()

                if not stimpackModule:
                    self.stimModule.draw()

                if not radiationShieldModule:
                    self.radiationModule.draw()

                if not exoskeletonModule:
                    self.exoModule.draw()

                # Test list
                # self.Keypad_1_test.draw()
                # self.Keypad_2_test.draw()
                # self.Keypad_3_test.draw()
                # self.test_text.draw()

                self.all_sprites.draw()
                self.light_layer_normal.draw(ambient_color=constants.AMBIENT_COLOUR)

        # Draw our health and oxygen on the screen, scrolling it with the viewport
        self.health_text = f"Health: {int(self.health)}%"
        self.oxygen_text = f"Oxygen: {int(self.oxygen)}%"

        self.health_center_x = 120 + self.view_left
        self.health_center_y = 45 + self.view_bottom
        self.oxygen_center_x = 120 + self.view_left
        self.oxygen_center_y = 80 + self.view_bottom

        arcade.draw_rectangle_filled(center_x=self.health_center_x,
                                     center_y=self.health_center_y,
                                     width=self.healthbar_width, height=self.healthbar_height,
                                     color=(30, 30, 30, 200))
        arcade.draw_rectangle_filled(center_x=self.health_center_x,
                                     center_y=self.health_center_y,
                                     width=((
                                                    self.healthbar_width - self.healthbar_padding) * self.health / 100) // 1,
                                     height=self.healthbar_height - self.healthbar_padding,
                                     color=(194, 59, 34, 225))

        arcade.draw_rectangle_filled(center_x=self.oxygen_center_x,
                                     center_y=self.oxygen_center_y,
                                     width=self.oxbar_width, height=self.oxbar_height,
                                     color=(30, 30, 30, 200))
        arcade.draw_rectangle_filled(center_x=self.oxygen_center_x,
                                     center_y=self.oxygen_center_y,
                                     width=((self.oxbar_width - self.oxbar_padding) * self.oxygen / 100) // 1,
                                     height=self.oxbar_height - self.oxbar_padding,
                                     color=(0, 0, 255, 225))

        arcade.draw_text("___VITALS___", self.oxygen_center_x - 82, self.oxygen_center_y + 15,
                         (0, 128, 0), 15,
                         font_name=os.path.join('fonts', 'Kusanagi.otf'))

        arcade.draw_text(self.health_text, self.health_center_x - 60, self.health_center_y - 10,
                         arcade.csscolor.LIGHT_GRAY, 14,
                         font_name=os.path.join('fonts', 'Orbitron-bold.ttf'))

        arcade.draw_text(self.oxygen_text, self.oxygen_center_x - 62, self.oxygen_center_y - 10,
                         arcade.csscolor.LIGHT_GRAY, 14,
                         font_name=os.path.join('fonts', 'Orbitron-bold.ttf'))

        arcade.draw_text(f"Stimpacks: {int(self.stimpacks)}", self.oxygen_center_x + 690, self.oxygen_center_y - 60,
                         arcade.csscolor.LIGHT_GRAY, 14,
                         font_name=os.path.join('fonts', 'Orbitron-bold.ttf'))

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Handle user input. Input handled:
        - WASD or arrow keys for movement of player
        - Q quits the game
        - P pauses the game
        Character moves at the MOVE_RATE, defined in the constants at the top.
        """

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.E:

            # Door 0
            door_check = arcade.check_for_collision_with_list(self.player, self.keypad_0)

            if not GV.object[0][0]:
                if reachedDialogue[0]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[0][0]
                        self.trigger_math_sequence_game()

            # AI
            door_check = arcade.check_for_collision_with_list(self.player, self.PeripheralAI)

            if not GV.object[1][0]:
                if reachedDialogue[2]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[1][0]
                        self.trigger_anagram_game()

            # Door 1
            door_check = arcade.check_for_collision_with_list(self.player, self.keypad_1)

            if not GV.object[1][0]:
                if reachedDialogue[2]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[1][0]
                        self.trigger_math_sequence_game()

            # Door 2
            door_check = arcade.check_for_collision_with_list(self.player, self.keypad_2)

            if not GV.object[2][0]:
                if reachedDialogue[3]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[2][0]
                        self.trigger_math_sequence_game()

            # Door 5
            door_check = arcade.check_for_collision_with_list(self.player, self.keypad_5)

            if not GV.object[5][0]:
                if reachedDialogue[6]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[5][0]
                        self.trigger_math_sequence_game()

            # Door Server 1
            door_check = arcade.check_for_collision_with_list(self.player, self.keypad_server1)

            if not GV.object[9][0]:
                if reachedDialogue[9]:
                    if door_check != []:
                        GV.minigame_id = GV.instanceID[9][0]
                        self.trigger_math_sequence_game()

            '''
            fuse_check = arcade.check_for_collision_with_list(self.player, self.fuses)
            global reachedLight
            if fuse_check != []:
                reachedLight = False
            '''

            'Launching fake code minigame when interacting with computers and broken valves'

            # Comp 2
            if reachedDialogue[3] and arcade.check_for_collision_with_list(self.player, self.comp_2):
                if not GV.object[2][1]:
                    GV.minigame_id = GV.instanceID[2][1]
                    self.trigger_fake_code_game()

            # Comp 3 (optional)
            if reachedDialogue[4] and arcade.check_for_collision_with_list(self.player, self.comp_3):
                if not GV.object[3][1]:
                    GV.minigame_id = GV.instanceID[3][1]
                    self.trigger_fake_code_game()

            # Comp 8
            if reachedDialogue[9] and arcade.check_for_collision_with_list(self.player, self.comp_8):
                if not GV.object[8][1]:
                    GV.minigame_id = GV.instanceID[8][1]
                    self.trigger_fake_code_game()

            # Broken valve
            if reachedDialogue[4] and arcade.check_for_collision_with_list(self.player, self.broken_valve):
                if not GV.object[4][1]:
                    GV.minigame_id = GV.instanceID[4][1]
                    self.trigger_fake_code_game()

            ' Launch anagram minigame when interacting with terminals'

            # Terminal 6
            if reachedDialogue[7] and arcade.check_for_collision_with_list(self.player, self.terminal_6):
                if not GV.object[6][1]:
                    GV.minigame_id = GV.instanceID[6][1]
                    self.trigger_anagram_game()

            # Terminal 7
            if reachedDialogue[8] and arcade.check_for_collision_with_list(self.player, self.terminal_7):
                if not GV.object[7][1]:
                    GV.minigame_id = GV.instanceID[7][1]
                    self.trigger_anagram_game()

            # Ending
            if reachedDialogue[-1] and arcade.check_for_collision_with_list(self.player, self.escapePods):
                self.trigger_endgame_view()

            # Dialogue and Modules
            global stimpackModule
            if reachedDialogue[3] != True and reachedDialogue[2] == True:
                if arcade.check_for_collision_with_list(self.player, self.stimModule):
                    stimpackModule = True
                    for i in self.stimModule:
                        self.object_list.remove(i)
                    self.trigger_narrative(DialogueText.dialogue_4_text, TitleText.Title_4)
                    arcade.play_sound(self.upgrade,
                                      volume=constants.MUSIC_VOLUME / 25)
                    reachedDialogue[3] = True

            global oxygenTankModule
            if reachedDialogue[5] != True and reachedDialogue[4] == True:
                if arcade.check_for_collision_with_list(self.player, self.oxygenModule):
                    oxygenTankModule = True
                    for i in self.oxygenModule:
                        self.object_list.remove(i)
                    self.trigger_narrative(DialogueText.dialogue_6_text, TitleText.Title_6)
                    arcade.play_sound(self.upgrade, volume=constants.MUSIC_VOLUME / 35)
                    reachedDialogue[5] = True
                    GV.oxygen_depletion_rate = 0.01
                    print("oxygen_depletion_rate changed to: " + str(GV.oxygen_depletion_rate))

            # This is meant to be 4, do not change to 5
            if reachedDialogue[6] != True and reachedDialogue[4] == True:
                if GV.object[4][1]:
                    if arcade.check_for_collision_with_list(self.player, self.Mainframe):
                        self.trigger_narrative(DialogueText.dialogue_7_text, TitleText.Title_7)
                        reachedDialogue[6] = True

            global radiationShieldModule
            if reachedDialogue[7] != True and reachedDialogue[6] == True:
                if arcade.check_for_collision_with_list(self.player, self.radiationModule):
                    radiationShieldModule = True
                    for i in self.radiationModule:
                        self.object_list.remove(i)
                    self.trigger_narrative(DialogueText.dialogue_8_text, TitleText.Title_8)
                    arcade.play_sound(self.upgrade,
                                      volume=constants.MUSIC_VOLUME / 25)
                    reachedDialogue[7] = True

            global exoskeletonModule
            if reachedDialogue[9] != True and reachedDialogue[8] == True:
                if arcade.check_for_collision_with_list(self.player, self.exoModule):
                    exoskeletonModule = True
                    for i in self.exoModule:
                        self.object_list.remove(i)
                    self.trigger_narrative(DialogueText.dialogue_10_text, TitleText.Title_10)
                    arcade.play_sound(self.upgrade,
                                      volume=constants.MUSIC_VOLUME / 25)
                    reachedDialogue[9] = True

            '''Needs to be activated after computer used'''
            global reachedLight
            if reachedDialogue[12] != True and reachedDialogue[11] == True:
                if arcade.check_for_collision_with_list(self.player, self.fuses):
                    self.trigger_narrative(DialogueText.dialogue_13_text, TitleText.Title_13)
                    reachedDialogue[12] = True
                    reachedLight = False

            if reachedDialogue[13] != True and reachedDialogue[12] == True:
                if arcade.check_for_collision_with_list(self.player, self.escapePods):
                    GV.closed_door_central = True
                    self.close_door_2()
                    self.trigger_narrative(DialogueText.dialogue_14_text, TitleText.Title_14)
                    reachedDialogue[13] = True

            if reachedDialogue[14] != True and reachedDialogue[13] == True:
                if arcade.check_for_collision_with_list(self.player, self.fuses):
                    GV.closed_door_central = False
                    self.open_door_2()
                    self.trigger_narrative(DialogueText.dialogue_15_text, TitleText.Title_15)
                    reachedDialogue[14] = True

            if reachedDialogue[14] == True and arcade.check_for_collision_with_list(self.player, self.door_2):
                GV.closed_door_central = False
                self.open_door_2()

            if reachedDialogue[15] != True and reachedDialogue[14] == True:
                if arcade.check_for_collision_with_list(self.player, self.Mainframe):
                    self.trigger_narrative(DialogueText.dialogue_16_text, TitleText.Title_16)
                    reachedDialogue[15] = True

            # Oxygen increase

            if arcade.check_for_collision_with_list(self.player, self.interactables) and GV.Counter <= 0:
                # Function that adds certain amount of oxygen
                # if the player has the oxygen module he can top up the oxygen
                if oxygenTankModule:
                    self.add_oxygen(100)
                    GV.Counter = 40
                # if the player doesn't have the oxygen module he can restore 50 oxygen
                elif not oxygenTankModule:
                    self.add_oxygen(50)
                    GV.Counter = 30
            elif arcade.check_for_collision_with_list(self.player, self.interactables) and GV.Counter > 0:
                arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)

            # Stimpack increase

            if arcade.check_for_collision_with_list(self.player, self.stimpack_1):
                if stimpackModule:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 3:
                        self.stimpacks = 3
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock,volume= constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_1:
                            self.object_list.remove(i)
                else:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 1:
                        self.stimpacks = 1
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_1:
                            self.object_list.remove(i)

            if arcade.check_for_collision_with_list(self.player, self.stimpack_2):
                if stimpackModule:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 3:
                        self.stimpacks = 3
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_2:
                            self.object_list.remove(i)
                else:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 1:
                        self.stimpacks = 1
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_2:
                            self.object_list.remove(i)

            if arcade.check_for_collision_with_list(self.player, self.stimpack_3):
                if stimpackModule:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 3:
                        self.stimpacks = 3
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_3:
                            self.object_list.remove(i)
                else:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 1:
                        self.stimpacks = 1
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_3:
                            self.object_list.remove(i)

            if arcade.check_for_collision_with_list(self.player, self.stimpack_4):
                if stimpackModule:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 3:
                        self.stimpacks = 3
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_4:
                            self.object_list.remove(i)
                else:
                    self.stimpacks = self.stimpacks + 1
                    if self.stimpacks > 1:
                        self.stimpacks = 1
                        arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                    else:
                        arcade.play_sound(self.task_unlock, volume=constants.MUSIC_VOLUME / 25)
                        for i in self.stimpack_4:
                            self.object_list.remove(i)

            # Test keypads

        # if arcade.check_for_collision_with_list(self.player, self.Keypad_1_test):
        #    GV.minigame_id = 8
        #   self.trigger_anagram_game()

        # if arcade.check_for_collision_with_list(self.player, self.Keypad_2_test):
        #    GV.minigame_id = 9
        #   self.trigger_anagram_game()

        #  if arcade.check_for_collision_with_list(self.player, self.Keypad_3_test):
        #     GV.minigame_id = 10
        #    self.trigger_fake_code_game()

        if symbol == arcade.key.ESCAPE:
            arcade.play_sound(self.button, volume=constants.MUSIC_VOLUME / 30)
            self.trigger_in_game_menu_view()

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = constants.MOVE_RATE

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -constants.MOVE_RATE

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -constants.MOVE_RATE

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = constants.MOVE_RATE

        if symbol == arcade.key.R:
            if self.stimpacks > 0:
                if self.health == 100:
                    arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)
                else:
                    self.health = self.health + 40
                    arcade.play_sound(self.oxygen_refill_sound, volume=constants.MUSIC_VOLUME / 10)
                    if self.health > 100:
                        self.health = 100
                    self.stimpacks = self.stimpacks - 1
            else:
                arcade.play_sound(self.task_fail, volume=constants.MUSIC_VOLUME / 10)

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Handle key releases for movement keys, sets direction delta back to 0
        """
        if (
                symbol == arcade.key.W
                or symbol == arcade.key.UP
                or symbol == arcade.key.S
                or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
                symbol == arcade.key.A
                or symbol == arcade.key.LEFT
                or symbol == arcade.key.D
                or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        if self.paused:
            return

        # All sprite movement is handled by the physics engine.
        self.physics_engine.update()

        # Variable to check if boundary changed
        changed = False

        # Scroll left
        left_boundary = self.view_left + constants.VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + constants.SCREEN_WIDTH - constants.VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + constants.SCREEN_HEIGHT - constants.VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                constants.SCREEN_HEIGHT + self.view_bottom)

        global reachedLight
        if reachedLight == True:
            self.player_light_adjusted.position = self.player.position
        else:
            self.player_light_normal.position = self.player.position
        global inDialogue
        if reachedDialogue[0] != True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_1):
                "When a collision is detected, the view is changed to a narrative screen"
                self.trigger_narrative(DialogueText.dialogue_1_text, TitleText.Title_1)
                "The dialogue boolean is changed"
                reachedDialogue[0] = True

        if reachedDialogue[1] != True and reachedDialogue[0] == True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_2):
                self.trigger_narrative(DialogueText.dialogue_2_text, TitleText.Title_2)
                reachedDialogue[1] = True

        if reachedDialogue[2] != True and reachedDialogue[1] == True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_3):
                self.trigger_narrative(DialogueText.dialogue_3_text, TitleText.Title_3)
                reachedDialogue[2] = True

        if reachedDialogue[4] != True and reachedDialogue[3] == True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_5):
                self.trigger_narrative(DialogueText.dialogue_5_text, TitleText.Title_5)
                reachedDialogue[4] = True

        if reachedDialogue[8] != True and reachedDialogue[7] == True:
            if GV.object[6][1]:
                if arcade.check_for_collision_with_list(self.player, self.dialogue_9):
                    self.trigger_narrative(DialogueText.dialogue_9_text, TitleText.Title_9)
                    reachedDialogue[8] = True

        if reachedDialogue[10] != True and reachedDialogue[9] == True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_11):
                self.open_door_server3()
                self.close_door_server2()
                self.trigger_narrative(DialogueText.dialogue_11_text, TitleText.Title_11)
                reachedDialogue[10] = True

        if reachedDialogue[11] != True and reachedDialogue[10] == True:
            if arcade.check_for_collision_with_list(self.player, self.dialogue_12):
                self.trigger_narrative(DialogueText.dialogue_12_text, TitleText.Title_12)
                reachedDialogue[11] = True
                GV.opened_door_central = False

        if reachedDialogue[10] and arcade.check_for_collision_with_list(self.player, self.lights):
            reachedLight = True

        "Logic for Blocking player access to areas with high levels of radiation and pressure"
        if not reachedDialogue[7]:
            if arcade.check_for_collision_with_list(self.player, self.radiation):
                GV.radiation_check = True
                self.trigger_narrative(dialogue.dialogue_Radiation, warning.Title_Radiation)
                for i in self.radiation:
                    self.collision_objects.append(i)

        if reachedDialogue[7] and GV.radiation_check:
            for i in self.radiation:
                self.collision_objects.remove(i)
            GV.radiation_check = False

        if not reachedDialogue[9]:
            if arcade.check_for_collision_with_list(self.player, self.pressure):
                GV.pressure_check = True
                self.trigger_narrative(dialogue.dialogue_Pressure, warning.Title_Pressure)
                for i in self.pressure:
                    self.collision_objects.append(i)

        if reachedDialogue[9] and GV.pressure_check:
            for i in self.pressure:
                self.collision_objects.remove(i)
            GV.pressure_check = False

        "Logic for Oxygen and subsequent Health depletion"
        "For stimpack usage add 40 health until health is 100 if health+40>100 then health is 100"

        if self.oxygen >= GV.oxygen_depletion_rate:
            self.oxygen -= GV.oxygen_depletion_rate
        else:
            self.oxygen = 0

        if self.oxygen == 0:
            if self.health >= GV.health_depletion_rate:
                self.health -= GV.health_depletion_rate
            else:
                self.health = 0

        if self.health == 0:
            self.trigger_gameover_view()

        "Logic for counter"
        GV.Counter -= 0.02

        "Music update routine"
        position = self.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0 and spaceDungeonIsView:
            self.advance_song()
            self.play_song()
