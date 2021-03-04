import arcade
import os
from arcade.gui.ui_style import UIStyle

""" Main_Menu UI """
UIStyle.default_style().set_class_attrs(
    'Game_Title',
    font_name=os.path.join('fonts', 'kusanagi.otf'),
    font_color=(120, 195, 220),
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'NewGame',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'LoadGame',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'Settings',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'QuitGame',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'Line',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=arcade.color.BLUE_GRAY,
    bg_color_hover=arcade.color.BLUE_GRAY,
    bg_color_press=arcade.color.BLUE_GRAY,
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

""" MathSequenceGame UI """
UIStyle.default_style().set_class_attrs(
    'mathGame_UI1',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'mathGame_UI2',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.BLUE_GRAY,
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'mathGame_UI3',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'WrongAnswer',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.CADMIUM_RED,
    font_color_hover=arcade.color.RED,
    font_color_press=arcade.color.RED,
)

UIStyle.default_style().set_class_attrs(
    'exitButton',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=12,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'EnterCode',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'InputBox',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.BLUE_GRAY,
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_focus=arcade.color.BABY_BLUE,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    bg_color_focus=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY

)

""" End_Game_Screen UI """
UIStyle.default_style().set_class_attrs(
    'Congratulations',
    font_name=os.path.join('fonts', 'kusanagi.otf'),
    font_color=(120, 195, 220),
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'Text',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=18,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'ReturnToMenu',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'Line',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=arcade.color.BLUE_GRAY,
    bg_color_hover=arcade.color.BLUE_GRAY,
    bg_color_press=arcade.color.BLUE_GRAY,
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)
""" New Narrative UI """

UIStyle.default_style().set_class_attrs(
    'NewText',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=16,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

""" Narrative Template UI """
UIStyle.default_style().set_class_attrs(
    'Title',
    font_name=os.path.join('fonts', 'kusanagi.otf'),
    font_color=(120, 195, 220),
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'Text',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=16,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'Continue',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'Line',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=arcade.color.BLUE_GRAY,
    bg_color_hover=arcade.color.BLUE_GRAY,
    bg_color_press=arcade.color.BLUE_GRAY,
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

""" Misc Styles """
UIStyle.default_style().set_class_attrs(
    'Text_2',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=16,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'Text_3',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=16,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'Text_4',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=16,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'BlueUI',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.BLUE_GRAY,
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'BlueUI2',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.BLUE_GRAY,
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'Tries',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.CADMIUM_GREEN,
    font_color_hover=arcade.color.GO_GREEN,
    font_color_press=arcade.color.GO_GREEN,
)

UIStyle.default_style().set_class_attrs(
    'fcg',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=20,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'fcg2',
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_size=20,
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.WHITE_SMOKE,
)

UIStyle.default_style().set_class_attrs(
    'Blue_Text_Big',
    font_size=25,
    font_name=os.path.join('fonts', 'Orbitron-bold.ttf'),
    font_color=arcade.color.BLUE_GRAY,
    font_color_hover=arcade.color.BABY_BLUE,
    font_color_press=arcade.color.BABY_BLUE,
)

UIStyle.default_style().set_class_attrs(
    'Button2',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)

UIStyle.default_style().set_class_attrs(
    'Button3',
    font_name=os.path.join('fonts', 'GOTHIC.ttf'),
    font_color=arcade.color.LIGHT_GRAY,
    font_color_hover=arcade.color.WHITE_SMOKE,
    font_color_press=arcade.color.LIGHT_GRAY,
    bg_color=(30, 30, 30),
    bg_color_hover=(60, 60, 60),
    bg_color_press=(30, 30, 30),
    border_color=arcade.color.BLUE_GRAY,
    border_color_hover=arcade.color.BABY_BLUE,
    border_color_press=arcade.color.BLUE_GRAY
)