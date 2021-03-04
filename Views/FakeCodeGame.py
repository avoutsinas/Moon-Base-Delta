import os
import arcade
from random import choice
import arcade.gui
import UIStyles
from arcade.gui import UIManager
import constants
import GlobalVariables as GV
from Views import FakeCodeGame, spacedungeon

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))

text_prompt = "Hint: Codes do not contain duplicate numbers"
fails = 0
first_instance = True
global_n = -1
chosen_list = []
button_text = "Enter Code"
success = False
entered_code = -1
# This global variable checks the triggered instance of the minigame
saved_instance = 0


def reset_global_variables():
    global first_instance
    global entered_code
    global button_text
    global text_prompt
    global success
    global fails
    global global_n
    global chosen_list
    global saved_instance

    text_prompt = "Hint: Codes do not contain duplicate numbers"
    fails = 0
    first_instance = True
    global_n = -1
    chosen_list = []
    button_text = "Enter Code"
    success = False
    entered_code = -1
    saved_instance = 0


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
        if success or fails == 20:
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

    def __init__(self, center_x, center_y, input_box, ui_manager, minigame, n, choice_list):
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
        self.n = n
        self.choice_list = choice_list
        self.num_of_correct_guesses = 0
        self.input_list = []
        self.flag = False

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global entered_code

        if button_text == "Enter Code":
            self.answer = self.input_box.text
            entered_code = self.answer
            self.convert_string_to_int(self.answer)
            self.ui_manager.purge_ui_elements()
            self.minigame.window.show_view(FakeCodeGame.MyView(self.minigame.main_view))
            print(f"EnterCode button. {self.answer}")
        elif button_text == "Exit Terminal":
            reset_global_variables()
            self.minigame.window.show_view(self.minigame.main_view)

        """
        The following functions check the submitted answer
        """

    def convert_string_to_int(self, answer):
        global text_prompt
        if len(answer) > self.n:
            text_prompt = "You have entered too many characters"
        elif 0 < len(answer) < self.n:
            text_prompt = "You have entered too few characters"
        elif len(answer) == 0:
            text_prompt = "You have to enter " + str(global_n) + " digits"
        else:
            try:
                for i in range(self.n):
                    self.input_list.append(int(answer[i]))
            except ValueError:
                self.flag = True
                text_prompt = "The terminal will only accept digits"
                pass
            if not self.flag:
                self.code_checker(self.input_list)

    def code_checker(self, answer_list):
        for i in range(self.n):
            if answer_list[i] == self.choice_list[i]:
                self.num_of_correct_guesses += 1
            else:
                pass
        self.print_guesses(self.num_of_correct_guesses)

    def print_guesses(self, num):
        global text_prompt
        global fails
        global global_n
        global button_text
        global entered_code
        global success
        print(saved_instance)
        if fails == 19:
            text_prompt = "You must reboot the terminal and try again!"
            button_text = "Exit Terminal"
            arcade.play_sound(self.minigame.main_view.task_fail,
                              volume=constants.MUSIC_VOLUME / 10)
            fails = 20
        else:
            if self.n > num:
                text_prompt = "Code Entered: " + str(entered_code) + "\n\n" + str(num) + "/" + str(
                    global_n) + " correct digits"
                fails += 1
                arcade.play_sound(self.minigame.main_view.task_try,
                                  volume=constants.MUSIC_VOLUME / 25)
            elif num == self.n:
                """***Enter unlocking condition for main game here***"""
                # play sound effect
                arcade.play_sound(self.minigame.main_view.task_unlock,
                                  volume=constants.MUSIC_VOLUME / 25)

                if GV.minigame_id == saved_instance:
                    GV.object[saved_instance][1] = True
                    if GV.object[saved_instance][0] and GV.object[saved_instance][1]:
                        if saved_instance == 2:
                            self.minigame.main_view.open_door_2()
                        if saved_instance == 3:
                            self.minigame.main_view.open_door_3()
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
                '''
                if GV.minigame_id == 2:
                    GV.object[2][1] = True
                    if GV.object[2][0] and GV.object[2][1]:
                        self.minigame.main_view.open_door_2()
                '''
                success = True
                text_prompt = "You cracked the code!"
                button_text = "Exit Terminal"


class MyView(arcade.View):
    """
    Main view. Really the only view in this example.
    """

    def __init__(self, main_view):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'console.jpg'))
        self.main_view = main_view

        self.y_slot = constants.SCREEN_HEIGHT // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4

        global first_instance
        global global_n
        global chosen_list
        global saved_instance

        if saved_instance != GV.minigame_id:
            reset_global_variables()
            saved_instance = GV.minigame_id

        if first_instance:
            first_instance = False
            # this is one of the more important variables, can be changed to increase/decrease difficulty

            "if condition to generate a code according to specified difficulty"
            if constants.DIFFICULTY == 0:
                self.n = 2
            elif constants.DIFFICULTY == 1:
                self.n = 3
            elif constants.DIFFICULTY == 2:
                self.n = 4

            global_n = self.n

            self.sequence = [i for i in range(10)]
            self.choice_list = []

            # this for loop generates a unique list of random numbers
            for i in range(self.n):
                self.new_item = choice(self.sequence)
                self.sequence.remove(self.new_item)
                self.choice_list.append(self.new_item)

            chosen_list = self.choice_list
            print("FakeCodeGame InstanceNo = " + str(saved_instance))
            print("FakeCodeGame Current Code: " + str(self.choice_list))
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
                                            self.background, alpha=50)

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
            """You need to crack the terminal passcode.\n
Enter """ + str(global_n) + """ unique digits and try to guess the code!""",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3,
            id="fcg"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            text_prompt,
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.25,
            id="mathGame_UI2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "Tries left: " + str(20 - fails),
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
            n=global_n,
            choice_list=chosen_list
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
