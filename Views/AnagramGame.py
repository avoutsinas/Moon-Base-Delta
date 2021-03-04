import os
import arcade
import random
from functools import partial
from io import StringIO
import arcade.gui
import UIStyles
from arcade.gui import UIManager
import constants
import GlobalVariables as GV
from Views import AnagramGame, spacedungeon

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))

"""                              ***Global Variables***"""

text_prompt = "Enter the deciphered password"
display = ""
fails = 0
mixed_password = ""
correct_password = "-1"
first_instance = True
button_text = "Enter Password"
success = False
# This global variable checks the triggered instance of the minigame
saved_instance = 0


def reset_global_variables():
    global first_instance
    global button_text
    global text_prompt
    global success
    global display
    global fails
    global correct_password
    global mixed_password
    global saved_instance

    text_prompt = "Enter the deciphered password"
    display = ""
    fails = 0
    correct_password = "-1"
    mixed_password = ""
    first_instance = True
    button_text = "Enter Password"
    success = False


class ExitButton(arcade.gui.UIGhostFlatButton):
    """
    The Exit Button will quit the minigame
    and return to the main view
    """

    def __init__(self, center_x, center_y, minigame):
        super().__init__(
            'x',
            center_x=center_x,
            center_y=center_y,
            width=20,
            height=22,
            id="exitButton"
        )

        self.minigame = minigame

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global success
        global fails

        if success or fails == 3:
            reset_global_variables()
            self.minigame.window.show_view(self.minigame.main_view)
        else:
            self.minigame.window.show_view(self.minigame.main_view)
        print(f"Exit Button.")


class EnterCodeButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, input_box, ui_manager, minigame):
        super().__init__(
            button_text,
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="EnterCode"
        )

        self.minigame = minigame
        self.ui_manager = ui_manager

        self.input_box = input_box

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        if button_text == "Enter Password":
            self.answer = self.input_box.text
            self.evaluate_answer(self.answer)
            self.ui_manager.purge_ui_elements()
            self.minigame.window.show_view(AnagramGame.MyView(self.minigame.main_view))
            print(f"EnterPassword button. {self.answer}")
        elif button_text == "Exit Console":
            reset_global_variables()
            self.minigame.window.show_view(self.minigame.main_view)

        """
        The following function checks the submitted answer
        """

    def evaluate_answer(self, answer):
        global correct_password
        global success
        global text_prompt
        global fails
        global button_text

        if answer == correct_password:
            success = True
            button_text = "Exit Console"
            text_prompt = "You found the password!"

            """***Enter Winning Unlocks Here***"""
            # play sound effect
            arcade.play_sound(self.minigame.main_view.task_unlock,
                              volume=constants.MUSIC_VOLUME / 25)

            if GV.minigame_id == saved_instance:
                GV.object[saved_instance][1] = True
                if GV.object[saved_instance][0] and GV.object[saved_instance][1]:
                    if saved_instance == 1:
                        self.minigame.main_view.open_door_1()
                    if saved_instance == 2:
                        self.minigame.main_view.open_door_2()
                    if saved_instance == 3:
                        self.minigame.main_view.open_door_3()
                    if saved_instance == 4:
                        self.minigame.main_view.open_door_4()
                    if saved_instance == 5:
                        self.minigame.main_view.open_door_5()
                    if saved_instance == 7:
                        self.minigame.main_view.open_door_7()
                    if saved_instance == 8:
                        self.minigame.main_view.open_door_8()
                    if saved_instance == 9:
                        self.minigame.main_view.open_door_9()
                    if saved_instance == 10:
                        self.minigame.main_view.open_door_10()
                    if saved_instance == 11:
                        self.minigame.main_view.open_door_11()

        elif answer == "":
            text_prompt = "You must enter something!"
            pass
        else:
            fails += 1
            arcade.play_sound(self.minigame.main_view.task_try,
                              volume=constants.MUSIC_VOLUME / 25)
            if fails > 2:
                text_prompt = "You must reboot the console and try again!"
                button_text = "Exit Console"
                fails = 3
                arcade.play_sound(self.minigame.main_view.task_fail,
                                  volume=constants.MUSIC_VOLUME / 10)
            else:
                text_prompt = "Nothing happened, try again!"


class MyView(arcade.View):
    """
    Main view. Really the only view in this example.
    """

    def __init__(self, main_view):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'terminal.jpg'))
        self.main_view = main_view

        self.y_slot = constants.SCREEN_HEIGHT // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4

        global text_prompt
        global first_instance
        global mixed_password
        global correct_password
        global saved_instance

        if saved_instance != GV.minigame_id:
            reset_global_variables()
            saved_instance = GV.minigame_id

        if first_instance:
            first_instance = False

            "If Conditions which generate differet words according to selected difficulty"
            if constants.DIFFICULTY == 0:
                self.wordset = ["chaos", "comet", "cosmic", "kepler", "lunar", "planet",
                                "orbit", "solar", "dwarf", "giant", "hubble", "venus", "earth",
                                "pluto", "ceres", "saturn", "titan", "newton", "europa", "phobos", "uranus"]

                self.confusing = []

                self.i = random.randint(0, len(self.wordset) - 1)
                self.data = self.wordset[self.i]
                self.data_len = len(self.data)
                for self.l in iter(partial(StringIO(self.data).read, 2), ''):
                    self.confusing.append(self.l)

            elif constants.DIFFICULTY == 1:
                self.wordset = ["moonbase", "spaceship", "jupiter", "mercury", "neptune", "asteroid", "astronaut",
                                "cosmonaut", "meteorite", "universe", "blackhole", "astronomy",
                                "equinox", "eclipse", "magnitude", "satellite", "starlight", "stardust",
                                "starboy", "crescent", "bigbang", "milkyway",
                                "telescope", "sputnik"]

                self.confusing = []

                self.i = random.randint(0, len(self.wordset) - 1)
                self.data = self.wordset[self.i]
                self.data_len = len(self.data)
                for self.l in iter(partial(StringIO(self.data).read, 3), ''):
                    self.confusing.append(self.l)

            elif constants.DIFFICULTY == 2:
                self.wordset = ["chemosynthesis", "nucleosynthesis", "spectroscopic", "circumstellar",
                                "electromagnetic", "protoplasmic", "geosynchronous",
                                "hydrostatic", "hypergalaxy", "magnetosphere", "troposphere",
                                "stratosphere", "thermosphere", "occultation", "photosphere", "protoplanetary",
                                "spectrometer", "spectroscopy"]

                self.confusing = []

                self.i = random.randint(0, len(self.wordset) - 1)
                self.data = self.wordset[self.i]
                self.data_len = len(self.data)
                for self.l in iter(partial(StringIO(self.data).read, 5), ''):
                    self.confusing.append(self.l)

            self.firstpart = self.confusing[0]
            self.secondpart = self.confusing[1]
            self.thirdpart = self.confusing[2]

            correct_password = self.firstpart + self.secondpart + self.thirdpart

            self.order = random.randint(1, 3)

            if self.order == 1:
                mixed_password = self.thirdpart + self.secondpart + self.firstpart
            elif self.order == 2:
                mixed_password = self.secondpart + self.thirdpart + self.firstpart
            elif self.order == 3:
                mixed_password = self.firstpart + self.thirdpart + self.secondpart

            print("AnagramGame InstanceNo = " + str(saved_instance))
            print("AnagramGame Current Password: " + correct_password)
        else:
            pass

        self.ui_manager = UIManager()

    def on_draw(self):
        """
        Draw this view. GUI elements are automatically drawn.
        SCREEN_WIDTH and SCREEN_HEIGHT are imported but backgrounds
        needs some tweaking to fit screen
        """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            constants.SCREEN_WIDTH * 1, constants.SCREEN_HEIGHT * 1,
                                            self.background, alpha=40)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, constants.SCREEN_WIDTH - 1, 0, constants.SCREEN_HEIGHT - 1)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        global text_prompt
        global fails

        # Text elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            """The password seems to be jumbled.\n\n Can you decipher it?""",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3.1,
            id="fcg"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "[ " + mixed_password + " ]",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.45,
            id="Blue_Text_Big"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            text_prompt,
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2,
            id="fcg2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "Tries left: " + str(3 - fails),
            center_x=self.left_column_x * 2,
            center_y=self.y_slot / 1.7,
            id="Tries"

        ))

        # Input Box
        ui_input_box = arcade.gui.UIInputBox(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.5,
            width=300,
            id="InputBox"
        )
        ui_input_box.text = ''
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

        # Buttons
        button = EnterCodeButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot,
            input_box=ui_input_box,
            minigame=self,
            ui_manager=self.ui_manager,
        )
        self.ui_manager.add_ui_element(button)

        button = ExitButton(
            center_x=self.right_column_x * 1.25,
            center_y=self.y_slot * 3.7,
            minigame=self
        )
        self.ui_manager.add_ui_element(button)

    """Advances the music of spacedungeon if a track stops playing"""

    def on_update(self, dt):
        position = self.main_view.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.main_view.advance_song()
            self.main_view.play_song()


if __name__ == '__main__':
    # window = arcade.Window(title='Math_Sequence_Game')
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    view = MyView()
    window.show_view(view)
    arcade.run()
