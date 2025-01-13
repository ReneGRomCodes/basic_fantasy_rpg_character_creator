import core.functions as func
import random
from item_instances import no_shield
"""Console functions. DELETE WHEN OBSOLETE!!!"""


def show_ability_scores(character):
    """Print formatted table of abilities from instance 'character' in console."""
    abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    for ability, key in zip(abilities, character.abilities):
        # 'Pre-formatting' ability name and bonus/penalty for better code-readability further down in print-statement.
        abilities_name = f"{ability}:"
        bonus_penalty = f"{character.abilities[key][1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in output or give out an empty
        # string if bonus_penalty is 0.
        if character.abilities[key][1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif character.abilities[key][1] == 0:
            bonus_penalty = ""
        else:
            pass

        print(f"{abilities_name:<23} {character.abilities[key][0]:>2} {bonus_penalty:>4}")


def show_saving_throws(character):
    """Print formatted output of dict 'saving_throws' from instance 'character'."""
    for k, v in character.saving_throws.items():
        print(f" - {k:<22} +{v:>2}")


def show_special_abilities(character):
    """Print formatted output of list 'specials' from instance 'character'."""
    for special in character.specials:
        print(f" - {special}")


def show_carrying_capacity(character):
    """Print formatted output of dict 'carrying_capacity' from instance 'character'."""
    for k, v in character.carrying_capacity.items():
        print(f" - {k}: {v:>3} pounds")


def show_inventory(character):
    """Print formatted output of list 'inventory' from instance 'character'."""
    for item in character.inventory:
        print(f" - {item.name:<30}{f"{item.weight} lbs":>7}")


def build_character_sheet(character):
    """Take instance 'character' and print character sheet."""

    print(f"{character.name.upper():<25}Level: 1")
    print(f"{character.race_name} {character.class_name:<15}XP: 0 ({character.next_level_xp})")
    print(f"\nArmor Class: {character.armor_class:<8}HP: {character.hp:<8}"
          f"Attack Bonus: +{character.attack_bonus}")
    print("\nAbilities:")
    show_ability_scores(character)
    print("\nSaving Throws:")
    show_saving_throws(character)
    print("\nSpecial Abilities:")
    show_special_abilities(character)

    # Add spells section if class is 'Magic-User', 'Cleric' or combination class.
    if character.spells:
        print("\nSpells:")
        print(f" - {character.spells}")

    print(f"\nMoney: {character.money} gold pieces")
    print("\nCarrying Capacity:")
    show_carrying_capacity(character)
    print("\nWeight Carried:")
    print(f"{character.weight_carried} Pounds")
    print("\nWeapons:")
    print(f"{character.weapon.name}")
    print(f"\n{f"Armor:":<15}{f"AC":>5}")
    print(f"{character.armor.name:<15}{character.armor.armor_class:>5}")
    if character.shield == no_shield:
        pass
    else:
        print(f"{character.shield.name:<15}{f"+{character.shield.armor_class}":>5}")

    if character.inventory:
        print("\nInventory:")
        show_inventory(character)
