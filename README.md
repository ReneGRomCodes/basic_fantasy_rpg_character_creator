# "Basic Fantasy RPG" Character Creator

## Overview

This is a fully functional character creator for the "Basic Fantasy RPG" game system, designed in Python using Pygame. It
serves as both a standalone application and a portfolio piece, demonstrating dynamic adaptability and modular structure.

While it is not a "character creator creator", it can be easily modified to accommodate other RPG rule systems with some
coding adjustments.

The program is built with Python and Pygame, featuring a UI that dynamically adjusts itself based on added UI element
instances. However, modifying the core rule set (races, classes, abilities, etc.) requires manual changes in rules.py and
character_model.py. If a new system requires additional screens (e.g., spell selection), they need to be implemented
separately but can reuse existing UI functions for consistency.

## Features

Easily Modifiable Rule System – Modify rules.py and character_model.py to adapt the character creator for other RPG
systems.

Adaptive UI – GUI elements reposition and resize automatically based on added UI instances, ensuring a clean layout.

Modular Design – Clear separation between game logic, descriptions, and UI elements for easier expansion.

Pygame-Based UI – Fully interactive graphical interface with text fields, buttons, and adaptive layout handling.

Reusable UI Functions – New screens can be built while leveraging existing helper functions for consistency.

State Management System – Tracks application flow and interactions to ensure a smooth experience.

## Installation

### Requirements

Python 3.12

pip 24.2

pygame 2.6.0

pygame-textinput 1.0.1

### Installing Python packages:

`pip install pygame pygame-textinput`

### Running the Program

Clone or download the repository.

Navigate to the project directory.

Run:

`python main.py`

## Project Structure
```
project_root/
│── main.py                # Main entry point, initializes Pygame and runs the main loop
│── core/                  # Handles game logic (settings, state management, character models, etc.)
│   ├── settings.py        # Stores configuration values (screen size, etc.)
│   ├── event_handlers.py  # Handles input events
│   ├── state_manager.py   # Manages application states
│   ├── rules.py           # Defines game mechanics and rules
│   └── character_model.py # Manages character attributes and interactions
│
│── descr/                 # Stores string-based descriptions (races, classes, etc.)
│
│── gui/                   # Manages UI components and rendering.
│   ├── screen_objects.py  # GUI element classes (buttons, text fields, etc.)
│   ├── cs_model.py        # Character sheet class and GUI logic
│   ├── gui_elements.py    # Creates and stores references to UI elements for rendering
│   ├── gui.py             # Handles UI logic and rendering functions
│   ├── ui_helpers.py      # Helper functions for positioning elements
│   ├── credits.py         # Credits screen logic
│   ├── settings_gui.py    # Settings screen logic
│   └── art/               # Contains graphic assets
│
└── README.md              # You are here
```
## Adding New Features

The program is designed with expandability in mind, making it easy to introduce new attributes, UI elements, or even
entirely new mechanics. Below is an example of how to add a new UI element, such as a "Luck" ability score, to the
character creation process.

Example: Adding a "Luck" Ability Score

    Modify the Character Model
        Add "luck" as a new attribute in character_model.py, ensuring it follows the same structure as other abilities.

    Update the Rules
        Modify rules.py to include "Luck" where necessary (e.g., defining how it's rolled, whether it affects class
        selection, etc.).

    Create the UI Element
        In screen_objects.py, create a new UI element class (or reuse an existing one) to display the "Luck" score.

    Add It to the GUI System
        Instantiate the "Luck" UI element in gui_elements.py, and add it to relevant functions in gui.py, ensuring it is
        included in the relevant screens.

    Adjust UI Layout
        Since the UI adapts dynamically, the new element will be positioned automatically. However, if needed,
        tweak ui_helpers.py to fine-tune spacing.

By following this process, new attributes, mechanics, or even entirely new selection screens can be integrated with minimal effort while keeping the UI flexible and consistent.

### Adding a New GUI Element

Choose an appropriate GUI class from screen_objects.py

Instantiate the new element in gui_elements.py according to documentation within the module.

Implement the new element in the relevant modules (e.g., gui.py).

## Work in Progress

Some obsolete or work-in-progress files remain in the main directory and will be removed in future updates.

## Future Plans

Implementing an item shop UI based on existing logic.

Refining documentation for easier customization.

## License

This repository is licensed under the MIT License. Feel free to use, modify, and distribute the code for your own
educational and non-commercial purposes.

## Credits

Created by René Grewe Romero. Feedback and contributions are welcome!

Basic Fantasy Role-Playing Game, Copyright 2006-2025 Chris Gonnerman. All Rights reserved.
Distributed under CC BY-SA license. www.basicfantasy.com