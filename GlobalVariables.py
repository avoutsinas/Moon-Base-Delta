import numpy as np

closed_door_central = False

# Warning checks
radiation_check = False
pressure_check = False

# Minigame ID: Set this variable to a unique number every time a minigame is triggered.
minigame_id = 0

# Variables which contain Keybinding Details
keybind_title = "Keybindings"
keybind_text = """\n
 Object interaction:   E\n\n Use stimpack:            R\n\n Smash objects:          F\n\nIn-Game Menu:     ESC\n\n"""

# Variables which contain text for Credits View
credits_title = "A GAME MADE BY:"
credits_text = """


Ben Schofield\n
Charlie Gamett-Griggs\n
Daniel Storer\n
Emma Wooding\n
Eray Ercan\n
Mia Noonan\n
Tasos Voutsinas\n
Zhengzheng Wang\n"""

# Variables which contain last reached dialogue point
dialogue = "Start exploring the base!"
title = "THE INCIDENT"

# Counter to determine how often player can access oxygen
Counter = 0

# Oxygen and Health depletion rate of player
oxygen_depletion_rate = 0.02
health_depletion_rate = 0.1

# Arrays which check objects that have been interacted with and minigame that have been completed
instanceID = np.array([[0, None],
                       [1, 1],
                       [2, 2],
                       [None, 3],
                       [None, 4],
                       [5, None],
                       [None, 6],
                       [None, 7],
                       [None, 8],
                       [9, None],
                       [10, None],
                       [11, None],
                       [12, None],
                       [13, None],
                       [14, None],
                       [15, None],
                       [16, None],
                       [17, None],
                       [18, None],
                       [19, None],
                       [20, None]])

object = np.array([[False, True],
                   [False, False],
                   [False, False],
                   [True, False],
                   [True, False],
                   [False, True],
                   [True, False],
                   [True, False],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True],
                   [False, True]])

# Copy of objects for reset purposes. This list should be identical to the object list
reset_object = np.array([[False, True],
                         [False, False],
                         [False, False],
                         [True, False],
                         [True, False],
                         [False, True],
                         [True, False],
                         [True, False],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True],
                         [False, True]])
