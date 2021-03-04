import arcade
from Views import Main_Menu
import constants


def main():
    """
    Main method
    """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    start_view = Main_Menu.MyView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
