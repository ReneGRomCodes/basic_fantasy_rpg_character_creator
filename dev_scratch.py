# This file contains code in development and is meant to try out concepts or just play around with ideas.
import random


# Dice roll.
def dice_roll(n):
    """Roll an n-sided dice and return the result."""
    return random.randint(1, n)


# Character creation:
def get_ability_score():
    """Generate random value for ability score, apply bonus/penalty and return the value."""
    base_score = dice_roll(18)
    if base_score <= 3:
        return base_score - 3
    elif base_score <= 5:
        return base_score - 2
    elif base_score <= 8:
        return base_score - 1
    elif base_score <= 12:
        return base_score
    elif base_score <= 15:
        return base_score + 1
    elif base_score <= 17:
        return base_score + 2
    else:
        return base_score + 3


strength = get_ability_score()
dexterity = get_ability_score()
constitution = get_ability_score()
intelligence = get_ability_score()
wisdom = get_ability_score()
charisma = get_ability_score()

player_name = "Adventurer"
player_race = "Human"
player_class = "Fighter"
player_level = 1
player_xp = 0
xp_next_level = 2000
armor_class = 11 + dexterity  # No armor
player_hp = dice_roll(8) + constitution
attack_bonus = 1
starting_money = dice_roll(18) * 10


# Character Sheet:
print(f"{player_name.upper()}                   XP: {player_xp}")
print()
print(f"Race: {player_race}    Class: {player_class}\nLevel: {player_level}       XP for next level: {xp_next_level}")
print()
print(f"Strength:       {strength}")
print(f"Dexterity:      {dexterity}")
print(f"Constitution:   {constitution}")
print(f"Intelligence:   {intelligence}")
print(f"Wisdom:         {wisdom}")
print(f"Charisma:       {charisma}")
print()
print(f"Money:          {starting_money}")
