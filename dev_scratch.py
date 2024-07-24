"""This file contains code in development and is meant to try out concepts or just play around with ideas."""
import random
import functions as func
import main_functions as mf

ability_scores, char_race, char_class, char_name = mf.random_character_generator()
mf.build_character_sheet(char_class, char_race, char_name, ability_scores)
