import os
import arcade
from Views import Main_Menu, spacedungeon, Settings, narrativeTemplate
import arcade.gui
import UIStyles
import GlobalVariables as GV
import constants
from arcade.gui import UIManager

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))


class ResumeGameButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, UImanager, menu, main_view):
        super().__init__(
            'Resume Game',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="NewGame"
        )

        self.ui_manager = UImanager
        self.menu = menu
        self.main_view = main_view
        self.music = self.main_view.music

    def on_click(self):
        """
        Called when user lets off button
        Upon Clicking this button the music is stopped,
        the UI is purged and the view is switched to the
        Narrative screen
        """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        self.ui_manager.purge_ui_elements()
        self.menu.window.show_view(self.main_view)
        print(f"ResumeGame button.")


class JournalButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu):
        super().__init__(
            'Journal',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="EnterCode"
        )

        self.menu = menu
        self.ui_manager = UImanager

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        self.ui_manager.purge_ui_elements()
        self.narrative_template = narrativeTemplate.MyView(self.menu.main_view, GV.dialogue, GV.title)
        self.menu.window.show_view(self.narrative_template)
        print(f"Journal button.")


class KeyBindingsButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu):
        super().__init__(
            'Key Bindings',
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
        self.narrative_template = narrativeTemplate.MyView(self.menu.main_view, GV.keybind_text, GV.keybind_title)
        self.menu.window.show_view(self.narrative_template)

        print(f"KeyBindings button.")


class SettingsButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu, main_view):
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
        self.main_view = main_view

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        self.ui_manager.purge_ui_elements()
        self.menu.window.show_view(Settings.MyView(self.main_view, 1))
        print(f"Settings button.")


class QuitToMainMenuButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, UImanager, menu, main_view):
        super().__init__(
            'Quit to Main',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="QuitGame"
        )

        self.ui_manager = UImanager
        self.menu = menu
        self.main_view = main_view

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)
        # reset reachedDialogue booleans
        for self.i in range(len(spacedungeon.reachedDialogue)):
            spacedungeon.reachedDialogue[self.i] = False
        # reset objects
        for self.i in range(len(GV.object)):
            GV.object[self.i][0] = GV.reset_object[self.i][0]
            GV.object[self.i][1] = GV.reset_object[self.i][1]
        # reset lighting
        spacedungeon.reachedLight = False
        # reset oxygen depletion rate
        GV.oxygen_depletion_rate = 0.02

        """Stop music, purge the UI and switch View"""
        self.main_view.stop_song()
        self.ui_manager.purge_ui_elements()
        self.menu.window.show_view(Main_Menu.MyView())
        print(f"QuitToMain button.")


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

    def __init__(self, main_view):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'In_Game_Menu.jpg'))

        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.y_slot = constants.SCREEN_HEIGHT // 4

        self.main_view = main_view
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
                                            self.background, alpha=100)

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, constants.SCREEN_WIDTH - 1, 0, constants.SCREEN_HEIGHT - 1)

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        # Text elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "GAME MENU",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3.3,
            id="Game_Title"

        ))

        # Buttons
        button = LineButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3.1,
        )
        self.ui_manager.add_ui_element(button)

        button = ResumeGameButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.7,
            main_view=self.main_view,
            UImanager=self.ui_manager,
            menu=self
        )
        self.ui_manager.add_ui_element(button)

        button = JournalButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.3,
            UImanager=self.ui_manager,
            menu=self
        )
        self.ui_manager.add_ui_element(button)

        button = KeyBindingsButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.9,
            UImanager=self.ui_manager,
            menu=self
        )
        self.ui_manager.add_ui_element(button)

        button = SettingsButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.5,
            main_view=self.main_view,
            UImanager=self.ui_manager,
            menu=self
        )
        self.ui_manager.add_ui_element(button)

        button = QuitToMainMenuButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.1,
            main_view=self.main_view,
            UImanager=self.ui_manager,
            menu=self
        )
        self.ui_manager.add_ui_element(button)

    """Advances the music of main_view if a track stops playing"""

    def on_update(self, dt):
        position = self.main_view.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.main_view.advance_song()
            self.main_view.play_song()
