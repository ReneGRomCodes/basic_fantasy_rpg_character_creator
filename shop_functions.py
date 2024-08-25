import item_instances
import os
"""Functions used for the item shop."""


def show_general_items():
    """Print items in list 'general_items' from module 'item_instances' in formatted string output."""
    shop_counter = 1

    print("GENERAL ITEMS:")
    print(f"{"Weight":>42}{"Cost":>10}")
    for item in item_instances.general_items:
        print(f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}")
        shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')


def show_weapons():
    """Print items in list 'weapons' from module 'item_instances' in formatted string output."""
    shop_counter = 1

    print("WEAPONS:")
    for k, v in item_instances.weapons.items():
        print("\n\n" + k)

        if k == "Ranged Weapons":
            print(f"{"Range":>50}")
            print(f"{"size":>27}{"weight":>9}{"S    M    L":^23}{"cost":>8}")
            for item in v:
                ranges = f"{item.range_list[0]:>3}, {item.range_list[1]:>3}, {item.range_list[2]:>3}"
                print(f"{shop_counter:>2} - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{ranges:^23}"
                      f"{f"{item.cost} gp":>8}")
                shop_counter += 1

        else:
            print(f"{"size":>27}{"weight":>9}{"damage":>8}{"cost":>10}")
            for item in v:
                print(f"{shop_counter:>2} - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"1d{item.damage}":>8}"
                      f"{f"{item.cost} gp":>10}")
                shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')


def show_projectiles():
    """Print items in list 'projectiles' from module 'item_instances' in formatted string output."""
    shop_counter = 1

    print("PROJECTILES:")
    print(f"{"weight":>45}{"damage":>8}{"cost":>10}")
    for projectile in item_instances.projectiles:
        print(f"{shop_counter:>2} - {projectile.name:<30}{f"{projectile.weight} lbs":>10}{f"1d{projectile.damage}":>8}"
              f"{f"{projectile.cost} gp":>10}")
        shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')


def show_armor():
    """Print items in list 'armor' from module 'item_instances' in formatted string output."""
    shop_counter = 1

    print("ARMOR:")
    print(f"{"Weight":>30}{"AC":>10}{"Cost":>10}")
    for armor in item_instances.armors:
        print(f"{shop_counter:>2} - {armor.name:<15}{f"{armor.weight} lbs":>10}{armor.armor_class:>10}"
              f"{f"{armor.cost} gp":>10}")
        shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')
