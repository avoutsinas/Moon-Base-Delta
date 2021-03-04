import os
import arcade
from Views import Main_Menu, spacedungeon, Settings, In_Game_Menu
import arcade.gui
import UIStyles
import constants
from arcade.gui import UIManager

button = arcade.load_sound(os.path.join("Sounds", "button.mp3"))

cammode = "Normal"
difficulty = "Medium"


class MenuVolumeUpButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '>',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="NewGame"
        )
        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        """
        Called when user lets off button
        """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        if constants.MUSIC_VOLUME < 1:

            constants.MUSIC_VOLUME = round(constants.MUSIC_VOLUME + 0.05, 3)
            if self.menu_type == 0:
                self.main_view.music.set_volume(constants.MUSIC_VOLUME / 10)
            elif self.menu_type == 1:
                self.main_view.music.set_volume(constants.MUSIC_VOLUME / 30)
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        else:
            pass

        print(f"MenuVolumeUp button.")
        print("Volume: " + str(int(constants.MUSIC_VOLUME * 100)))


class MenuVolumeDownButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '<',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="EnterCode"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        if constants.MUSIC_VOLUME >= 0.05:
            constants.MUSIC_VOLUME = round(constants.MUSIC_VOLUME - 0.05, 3)
            if self.menu_type == 0:
                self.main_view.music.set_volume(constants.MUSIC_VOLUME / 10)
            elif self.menu_type == 1:
                self.main_view.music.set_volume(constants.MUSIC_VOLUME / 30)
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        else:
            pass

        print(f"MenuVolumeDown button.")
        print("Volume: " + str(int(constants.MUSIC_VOLUME * 100)))


class CameraTightButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '>',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="LoadGame"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global cammode
        if constants.VIEWPORT_MARGIN == 450:
            pass
        elif constants.VIEWPORT_MARGIN == 350:
            constants.VIEWPORT_MARGIN = 450
            cammode = "Tight"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        elif constants.VIEWPORT_MARGIN == 250:
            constants.VIEWPORT_MARGIN = 350
            cammode = "Normal"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))

        print(f"CameraTight button.")
        print("Viewport: " + str(constants.VIEWPORT_MARGIN))


class CameraLooseButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '<',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="Settings"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global cammode
        if constants.VIEWPORT_MARGIN == 250:
            pass
        elif constants.VIEWPORT_MARGIN == 350:
            constants.VIEWPORT_MARGIN = 250
            cammode = "Loose"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        elif constants.VIEWPORT_MARGIN == 450:
            constants.VIEWPORT_MARGIN = 350
            cammode = "Normal"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))

        print(f"CameraLoose button.")
        print("Viewport: " + str(constants.VIEWPORT_MARGIN))


class DifficultyIncreaseButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '>',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="Button2"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global difficulty
        if constants.DIFFICULTY == 2:
            pass
        elif constants.DIFFICULTY == 1:
            constants.DIFFICULTY = 2
            difficulty = "Hard"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        elif constants.DIFFICULTY == 0:
            constants.DIFFICULTY = 1
            difficulty = "Medium"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))

        print(f"CameraTight button.")
        print("Difficulty: " + difficulty)


class DifficultyDecreaseButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            '<',
            center_x=center_x,
            center_y=center_y,
            width=50,
            height=50,
            id="Button3"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        global difficulty
        if constants.DIFFICULTY == 0:
            pass
        elif constants.DIFFICULTY == 1:
            constants.DIFFICULTY = 0
            difficulty = "Easy"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))
        elif constants.DIFFICULTY == 2:
            constants.DIFFICULTY = 1
            difficulty = "Medium"
            self.ui_manager.purge_ui_elements()
            self.settings.window.show_view(Settings.MyView(self.main_view, self.menu_type))

        print(f"DifficultyDecrease button.")
        print("Difficulty: " + difficulty)


class BackButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, ui_manager, settings, main_view, menu_type):
        super().__init__(
            'Back',
            center_x=center_x,
            center_y=center_y,
            width=250,
            height=50,
            id="QuitGame"
        )

        self.ui_manager = ui_manager
        self.settings = settings
        self.main_view = main_view
        self.menu_type = menu_type

    def on_click(self):
        """ Called when user lets off button """
        arcade.play_sound(button, volume=constants.MUSIC_VOLUME / 40)

        self.ui_manager.purge_ui_elements()
        if self.menu_type == 0:
            self.settings.window.show_view(self.main_view)
        elif self.menu_type == 1:
            self.settings.window.show_view(In_Game_Menu.MyView(self.main_view))

        print(f"Back button.")


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

    def __init__(self, main_view, menu_type):
        super().__init__()

        self.background = arcade.load_texture(os.path.join('images', 'In_Game_Menu.jpg'))

        self.right_column_x = 3 * constants.SCREEN_WIDTH // 4
        self.left_column_x = constants.SCREEN_WIDTH // 4
        self.y_slot = constants.SCREEN_HEIGHT // 4

        self.main_view = main_view
        self.menu_type = menu_type
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
            "SETTINGS",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3.2,
            id="Game_Title"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "Sound Volume",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.7,
            id="Text"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            str(int(constants.MUSIC_VOLUME * 100)) + "%",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.5,
            id="mathGame_UI2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "Camera Type",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 2.1,
            id="Text_2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            cammode,
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.9,
            id="BlueUI2"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            "Difficulty",
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.5,
            id="Text_4"

        ))

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            difficulty,
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 1.3,
            id="BlueUI"

        ))

        # Buttons
        button = LineButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 3,
        )
        self.ui_manager.add_ui_element(button)

        button = MenuVolumeUpButton(
            center_x=self.left_column_x * 2.6,
            center_y=self.y_slot * 2.55,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type

        )
        self.ui_manager.add_ui_element(button)

        button = MenuVolumeDownButton(
            center_x=self.left_column_x * 1.4,
            center_y=self.y_slot * 2.55,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
        )
        self.ui_manager.add_ui_element(button)

        button = CameraTightButton(
            center_x=self.left_column_x * 2.6,
            center_y=self.y_slot * 1.95,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
        )
        self.ui_manager.add_ui_element(button)

        button = CameraLooseButton(
            center_x=self.left_column_x * 1.4,
            center_y=self.y_slot * 1.95,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
        )
        self.ui_manager.add_ui_element(button)

        button = DifficultyIncreaseButton(
            center_x=self.left_column_x * 2.6,
            center_y=self.y_slot * 1.35,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
        )
        self.ui_manager.add_ui_element(button)

        button = DifficultyDecreaseButton(
            center_x=self.left_column_x * 1.4,
            center_y=self.y_slot * 1.35,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
        )
        self.ui_manager.add_ui_element(button)

        button = BackButton(
            center_x=self.left_column_x * 2,
            center_y=self.y_slot * 0.7,
            ui_manager=self.ui_manager,
            settings=self,
            main_view=self.main_view,
            menu_type=self.menu_type
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
