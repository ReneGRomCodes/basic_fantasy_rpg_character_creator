# "Basic Fantasy RPG" Character Creator

## Overview

This is a fully functional character creator for the "Basic Fantasy RPG" game system, designed in Python using Pygame. It
serves as both a standalone application and a portfolio piece, demonstrating dynamic adaptability and modular structure.

The program automatically adjusts GUI elements based on screen size and allows easy expansion by modifying core class
structures. While the final character sheet is not yet complete, the underlying framework is stable and adaptable.

## Features

Dynamic GUI Scaling – Automatically adapts to different screen sizes.

Modular Design – Clearly separated packages for core logic, descriptions, and GUI elements.

Easily Expandable – Adding new attributes, elements, or features requires minimal changes.

Pygame-Based UI – Custom-drawn interface using text fields, buttons, and other components.

State Management System – Keeps track of application flow and interactions.

## Installation

### Requirements

Python 3.12

pip 24.2

### The following Python packages:

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
│── core/                  # Core game logic (non-GUI modules)
│   ├── settings.py        # Stores configuration values (screen size, etc.)
│   ├── event_handlers.py  # Handles input events
│   ├── main_functions.py  # Manages application states
│   ├── functions.py       # Defines mechanics for character creation based on game rules
│   └── credits.py         # (To be moved to gui/) Credits screen logic
│   └── character_model.py # Player character class for creation process
│
│── descr/                 # String-based descriptions (races, classes, abilities, etc.)
│
│── gui/                   # Graphical user interface components
│   ├── screen_objects.py  # GUI element classes (buttons, text fields, etc.)
│   ├── cs_model.py        # Character sheet class and GUI logic
│   ├── gui_elements.py    # Creates GUI elements and returns them as a dictionary
│   ├── gui.py             # Functions for drawing elements on screen
│   └── ui_helpers.py      # Helper functions for positioning elements
│
└── README.md              # You are here
```
## Adding New Features

The program is designed with expandability in mind. Below is an example of how new elements can be added with minimal
effort:

### Adding a New GUI Element

Choose an appropriate GUI class from screen_objects.py

Instantiate the new element in gui_elements.py according to documentation within the module.

Call the new element in the relevant screen module (e.g., gui.py).

## Work in Progress

The final character sheet display is incomplete.

The program currently does not return to the main menu after displaying the character sheet.

Some obsolete or work-in-progress files remain in the main directory and will be removed in future updates.

## License

This repository is licensed under the MIT License. Feel free to use, modify, and distribute the code for your own
educational and non-commercial purposes.

## Credits

Created by René Grewe Romero. Feedback and contributions are welcome!

Basic Fantasy Role-Playing Game, Copyright 2006-2025 Chris Gonnerman. All Rights reserved.
Distributed under CC BY-SA license. www.basicfantasy.com