import os
import arcade
import arcade.gui
import constants
import GlobalVariables as GV
from arcade.gui import UIManager
from Views import spacedungeon, Main_Menu
import time

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))


class ReturnToMenuButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, gameover, UImanager, stop_song):
        super().__init__(
            'Return to Menu',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="ReturnToMenu"
        )

        self.ui_manager = UImanager
        self.gameover = gameover
        self.stop_song = stop_song

    def on_click(self):
        """
        Called when user lets off button
        Upon Clicking this button the music is stopped,
        the UI is purged and the view is switched to the
        Narrative screen. The global variables used in
        the main game are also reset to False
        """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        # reset reachedDialogue booleans
        for self.i in range(len(spacedungeon.reachedDialogue)):
            spacedungeon.reachedDialogue[self.i] = False
        # reset objects (to be added)
        for self.i in range(len(GV.object)):
            GV.object[self.i][0] = GV.reset_object[self.i][0]
            GV.object[self.i][1] = GV.reset_object[self.i][1]
        # reset lighting
        spacedungeon.reachedLight = False
        # reset oxygen depletion rate
        GV.oxygen_depletion_rate = 0.02

        """Stop music, purge the UI and switch View"""
        self.stop_song()
        self.ui_manager.purge_ui_elements()
        self.gameover.window.show_view(Main_Menu.MyView())

        print(f"ReturnToMenu button.")


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

        self.background = arcade.load_texture(os.path.join('images', 'mission_failed.jpg'))

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
                                            self.background, alpha=80)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, constants.SCREEN_WIDTH - 1, 0, constants.SCREEN_HEIGHT - 1)

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        # List of music
        self.music_list = [os.path.join('Music', 'scott-buckley-machina.mp3')]

        # Array index of what to play
        self.current_song = 0
        # Play the song
        self.play_song()

        # Text elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "MISSION FAILED!",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3,
            id="Congratulations"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "You did not make it to the escape pods \n"
            "and have run out of oxygen. \n\n"
            "The only chance to further investigate\n"
            "what happened to the moonbase is now lost...",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.9,
            id="Text"
        ))

        # Buttons
        button = LineButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.8,
        )
        self.ui_manager.add_ui_element(button)

        button = ReturnToMenuButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot / 1.9,
            gameover=self,
            UImanager=self.ui_manager,
            stop_song=self.stop_song
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


if __name__ == '__main__':
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    # window = arcade.Window(title='End_Game_Screen')
    view = MyView()
    window.show_view(view)
    arcade.run()
