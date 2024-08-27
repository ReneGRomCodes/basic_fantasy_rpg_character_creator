import item_instances
import os
import functions as func
"""Functions used for the item shop."""


def show_shop(character, instance_list, shop_name, table_header):
    """Show formatted output of selected shop with appropriate class attributes and return int 'counter' for use in
    function 'trade_items()'.
    ARGS:
        character: instance of Character class.
        instance_list: list of instances of Item class and child classes. Lists found in 'item_instances.py'.
        shop_name: String for name of the shop.
        table_header: formatted string for header of shop inventory.
    """
    # Initialize counter for items in shop.
    shop_counter = 1

    print(f"{shop_name}:")
    print(f"{table_header}")

    for item in instance_list:
        # Select appropriate table format for shop.
        if shop_name == "GENERAL ITEMS":
            table_format = f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}"
        elif shop_name == "PROJECTILES":
            table_format = (f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>10}"
                            f"{f"1d{item.damage}":>8}{f"{item.cost} gp":>10}")
        elif shop_name == "ARMOR":
            table_format = (f"{shop_counter:>2} - {item.name:<15}{f"{item.weight} lbs":>10}{item.armor_class:>10}"
                            f"{f"{item.cost} gp":>10}")

        # Print items in shop and amount of items in character inventory.
        if item in character.items:
            inventory = character.items.count(item)
            print(table_format + f"{inventory:>8}")
        else:
            print(table_format)

        shop_counter += 1

    print(f"\nYour money: {character.money} gp")
    return shop_counter


def trade_items(character, instance_list, shop_name, table_header):
    """Initialize trade loop for item shops.
    ARGS:
        character: instance of Character class.
        instance_list: list of instances of Item class and child classes. Lists found in 'item_instances.py'.
        shop_name: String for name of the shop.
        table_header: formatted string for header of shop inventory.
    """
    while True:
        # Print shop in formatted output and get int value for each item.
        shop_counter = show_shop(character, instance_list, shop_name, table_header)

        trade_item = input("\nChoose item to trade or press 'Enter' to return to shop menu: ")

        if not trade_item:
            os.system('cls')
            break
        else:
            try:
                selected_item = instance_list[int(trade_item) - 1]

                if func.check_yes_no(f"Are you sure you want to buy {selected_item.name} (Y/N)? "):
                    if character.buy_item(selected_item):
                        input(f"\n\t{selected_item.name} added to your inventory. Press 'Enter' to continue.")
                        os.system('cls')
                        continue
                    else:
                        input()
                        os.system('cls')
                else:
                    continue

            except IndexError:
                input(
                    f"\n\tInvalid input. Choose a number between 1 and {shop_counter - 1}. Press 'Enter' to continue.")
                os.system('cls')
                continue
            except ValueError:
                input(
                    f"\n\tInvalid input. Choose a number between 1 and {shop_counter - 1}. Press 'Enter' to continue.")
                os.system('cls')
                continue


def general_items_shop(character):
    """Show items available in shop 'GENERAL ITEMS' and prompt user for buy/sell action. ARG 'character' is Character
    class instance."""
    instance_list = item_instances.general_items
    shop_name = "GENERAL ITEMS"
    table_header = f"{"Weight":>42}{"Cost":>10}{"Inventory":>12}"

    trade_items(character, instance_list, shop_name, table_header)


def weapons_shop(character):
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


def projectiles_shop(character):
    """Show items available in shop 'PROJECTILES' and prompt user for buy/sell action. ARG 'character' is Character
    class instance."""
    instance_list = item_instances.projectiles
    shop_name = "PROJECTILES"
    table_header = f"{"weight":>45}{"damage":>8}{"cost":>10}{"Inventory":>12}"

    trade_items(character, instance_list, shop_name, table_header)


def armor_shop(character):
    """Show items available in shop 'ARMOR' and prompt user for buy/sell action. ARG 'character' is Character
    class instance."""
    instance_list = item_instances.armors
    shop_name = "ARMOR"
    table_header = f"{"Weight":>30}{"AC":>10}{"Cost":>10}{"Inventory":>12}"

    trade_items(character, instance_list, shop_name, table_header)


def show_inventory(character):
    """Print formatted output of items in attribute list 'items' from class 'Character' in 'character_model.py'."""
    shop_counter = 1

    print("INVENTORY:")
    print(f"{"Weight":>42}{"Cost":>10}")
    for item in character.items:
        print(f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}")
        shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')
