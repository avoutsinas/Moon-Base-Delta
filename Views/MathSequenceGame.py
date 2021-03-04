import os
import arcade
import random
import arcade.gui
import UIStyles
from arcade.gui import UIManager
import constants
import GlobalVariables as GV
from Views import spacedungeon, MathSequenceGame

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))

hidden_num = -1
text_prompt = "What could be missing?"
display = ""
fails = 0
printed_sequence = []
first_instance = True
button_text = "Enter Number"
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
    global hidden_num
    global printed_sequence

    text_prompt = "What could be missing?"
    display = ""
    fails = 0
    hidden_num = -1
    printed_sequence = []
    first_instance = True
    button_text = "Enter Number"
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

        if button_text == "Enter Number":
            self.answer = self.input_box.text
            self.evaluate_answer(self.answer)
            self.ui_manager.purge_ui_elements()
            self.minigame.window.show_view(MathSequenceGame.MyView(self.minigame.main_view))
            print(f"EnterNumber button. {self.answer}")
        elif button_text == "Exit Keypad":
            reset_global_variables()
            self.minigame.window.show_view(self.minigame.main_view)

        """
        The following function checks the submitted answer
        """

    def evaluate_answer(self, answer):
        global success
        global text_prompt
        global fails
        global button_text
        global count
        print(saved_instance)
        try:
            if int(answer) == int(hidden_num):
                success = True
                text_prompt = "You found the missing number!"
                button_text = "Exit Keypad"
                self.minigame.window.show_view(self.minigame.main_view)

                """***Enter Unlock Conditions Here"""
                # play sound effect
                arcade.play_sound(self.minigame.main_view.task_unlock,
                                  volume=constants.MUSIC_VOLUME / 25)
                # Checks which keypad the player is at and opens door accordingly
                if GV.minigame_id == saved_instance:
                    # Second index on object (column) always 0 for this game
                    GV.object[saved_instance][0] = True
                    if GV.object[saved_instance][0] and GV.object[saved_instance][1]:
                        if saved_instance == 0:
                            self.minigame.main_view.open_door_0()
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

            else:
                fails += 1
                text_prompt = "The keypad did not accept the number. Try again!"
                arcade.play_sound(self.minigame.main_view.task_try,
                                  volume=constants.MUSIC_VOLUME / 25)
                if fails > 2:
                    text_prompt = "You must restart the keypad to try again!"
                    button_text = "Exit Keypad"
                    fails = 3
                    arcade.play_sound(self.minigame.main_view.task_fail,
                                      volume=constants.MUSIC_VOLUME / 10)
                    return 1
                else:
                    print("try again!")
        except ValueError:
            text_prompt = "You must enter something!"
            return 1
            pass


class MyView(arcade.View):
    """
    Main view. Really the only view in this example.
    """

    def __init__(self, main_view):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'locked_door.jpg'))
        self.main_view = main_view

        self.y_slot = constants.SCREEN_HEIGHT // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4

        global text_prompt
        global first_instance
        global hidden_num
        global printed_sequence
        global saved_instance

        if saved_instance != GV.minigame_id:
            reset_global_variables()
            saved_instance = GV.minigame_id

        if first_instance:
            first_instance = False

            """
            The fibonacci main code is defined here in order for the program to display
            the random sequence
            """

            "If Conditions which generate differet words according to selected difficulty"
            if constants.DIFFICULTY == 0:
                self.array1 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
                self.array2 = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42]
                self.array3 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
                self.array4 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
                self.array5 = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98]
            elif constants.DIFFICULTY == 1:
                self.array1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
                self.array2 = [0, 3, 8, 15, 24, 35, 48, 63, 80, 99, 120, 143, 168, 195]
                self.array3 = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
                self.array4 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
                self.array5 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
            elif constants.DIFFICULTY == 2:
                self.array1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
                self.array2 = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136]
                self.array3 = [3, 9, 4, 8, 5, 7, 6, 6, 7, 5, 8, 4, 9, 3, 10, 2, 11, 1, 12, 0, 13]
                self.array4 = [0, 2, 4, 3, 5, 7, 6, 8, 10, 9, 11, 13, 12, 14, 16, 15]
                self.array5 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
            """
            One sequence is selected at random for each instance of the game
            """
            self.allGames = [self.array1, self.array2, self.array3, self.array4, self.array5]
            self.selectedGame = random.choice(self.allGames)
            self.index = random.randint(6, len(self.selectedGame) - 1)
            self.myarray = []

            for i in range(self.index - 6, self.index):
                self.myarray.append(self.selectedGame[i])

            self.blocked_index = random.randint(0, 4)
            self.hidden_number = self.myarray[self.blocked_index]
            self.myarray[self.blocked_index] = "x"
            self.array_to_print = " , ".join([str(item) for item in self.myarray])
            printed_sequence = self.array_to_print

            # a global variable is used to pass on the hidden_number to the submission button
            hidden_num = self.hidden_number

            print("MathSequenceGame InstanceNo = " + str(saved_instance))
            print(self.selectedGame)


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
                                            self.background, alpha=60)

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

        # Text elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "The door security code seems to be corrupted...",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3,
            id="mathGame_UI1"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "[ " + str(printed_sequence) + " ]",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.5,
            id="mathGame_UI2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            text_prompt,
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2,
            id="mathGame_UI3"

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
    window = arcade.Window(title='Math_Sequence_Game')
    view = MyView()
    window.show_view(view)
    arcade.run()
