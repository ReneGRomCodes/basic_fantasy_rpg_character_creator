"""This file contains code in development and is meant to try out concepts or just play around with ideas... alright, at
this point it has become mostly a dumping ground for 'todos'."""

# Old TODOS from console times that could still be good to keep in mind when migrating that part over to PyGame:
# TODO figure out how to implement different attacks with spear in 'item_instance.py'
# TODO Equip/unequip methods work only for armor right now in 'character_model.py'

# Shit to keep in mind:

# PRIORITIES:
# TODO add sections for thief skills to character sheet
# TODO implement possibility to select multiple additional languages based on intelligence bonus
# TODO add option to allow for minor customization of randomly generated characters
# TODO tweak the selection on some screen during character creation. not really happy with how they work


"""Data structure for JSON file to save/load characters. Also resets JSON file when this module is executed directly."""
import json
from core.settings import settings

# Data structure template for JSON.
data = {
    "slot_00": None,
    "slot_01": None,
    "slot_02": None,
    "slot_03": None,
    "slot_04": None,
    "slot_05": None,
    "slot_06": None,
    "slot_07": None,
    "slot_08": None,
}

with open(settings.save_file, "w") as f:
    json.dump(data, f)
