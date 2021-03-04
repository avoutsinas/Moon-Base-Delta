import os
import arcade
from Views import newNarrative, Settings, narrativeTemplate
import arcade.gui
import UIStyles
import constants
import GlobalVariables as GV
from constants import MUSIC_VOLUME
from arcade.gui import UIManager
import time

# This global variable checks if the menu is being set up for the first time.
# It helps with music flow between menu screens which do not start the main game.
# Turn to False only if you want to trigger another GUI view from the menu.
# The reason this boolean exists is that you cannot trigger a GUI view without
# setting it up first.
menu_first_setup = True

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))


class NewGameButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, menu, UImanager, stop_song):
        super().__init__(
            'New Game',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="NewGame"
        )

        self.ui_manager = UImanager
        self.menu = menu
        self.stop_song = stop_song

    def on_click(self):
        """
        Called when user lets off button
        Upon Clicking this button the music is stopped,
        the UI is purged and the view is switched to the
        Narrative screen
        """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        global menu_first_setup
        menu_first_setup = True
        self.stop_song()
        self.ui_manager.purge_ui_elements()
        self.menu.window.show_view(newNarrative.MyView())
        print(f"NewGame button.")


class CreditsButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu):
        super().__init__(
            'Credits',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="LoadGame"
        )

        self.menu = menu
        self.ui_manager = UImanager

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        self.ui_manager.purge_ui_elements()
        self.credits_view = narrativeTemplate.MyView(self.menu, GV.credits_text, GV.credits_title)
        self.menu.window.show_view(self.credits_view)
        global menu_first_setup
        menu_first_setup = False
        print(f"Credits button.")


class SettingsButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu):
        super().__init__(
            'Settings',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="Settings"
        )

        self.ui_manager = UImanager
        self.menu = menu

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        self.ui_manager.purge_ui_elements()
        self.menu.window.show_view(Settings.MyView(self.menu, 0))
        global menu_first_setup
        menu_first_setup = False
        print(f"Settings button.")


class QuitGameButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y):
        super().__init__(
            'Quit Game',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="QuitGame"
        )

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        arcade.close_window()
        print(f"QuitGame button.")


class LineButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y):
        super().__init__(
            "",
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=1,
            id="Line"
        )


class MyView(arcade.View):
    """
    Main view. Really the only view in this example.
    """

    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'menu.jpg'))

        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.y_slot = constants.SCREEN_HEIGHT // 4

        self.music_list = []
        self.current_song = 0
        self.music = None

        self.ui_manager = UIManager()

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.current_song += 1
        if self.current_song >= len(self.music_list):
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
        self.music.play(constants.MUSIC_VOLUME / 10)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def on_draw(self):
        """
        Draw this view. GUI elements are automatically drawn.
        SCREEN_WIDTH and SCREEN_HEIGHT are imported but backgrounds
        needs some tweaking to fit screen
        """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            constants.SCREEN_WIDTH * 1, constants.SCREEN_HEIGHT * 1,
                                            self.background, alpha=250)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, constants.SCREEN_WIDTH - 1, 0, constants.SCREEN_HEIGHT - 1)

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        # List of music
        self.music_list = [os.path.join('Music', 'hayden-folker-cloud-nine.mp3'),
                           os.path.join('Music', 'arthur-vyncke-a-few-jumps-away.mp3')]
        # Array index of what to play. Note that this happens only the first time that the Menu is triggered
        global menu_first_setup
        if menu_first_setup:
            self.current_song = 0
            # Play the song
            self.play_song()

        # Text elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "MOON BASE DELTA",
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 3,
            id="Game_Title"

        ))

        # Buttons
        button = LineButton(
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 2.8,
        )
        self.ui_manager.add_ui_element(button)

        button = NewGameButton(
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 2.4,
            menu=self,
            UImanager=self.ui_manager,
            stop_song=self.stop_song
        )
        self.ui_manager.add_ui_element(button)

        button = SettingsButton(
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 2,
            menu=self,
            UImanager=self.ui_manager
        )
        self.ui_manager.add_ui_element(button)

        button = CreditsButton(
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 1.6,
            menu=self,
            UImanager=self.ui_manager
        )
        self.ui_manager.add_ui_element(button)

        button = QuitGameButton(
            center_x=self.left_column_x / 1.1,
            center_y=self.y_slot * 1.2,
        )
        self.ui_manager.add_ui_element(button)

    def on_update(self, dt):

        position = self.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()
