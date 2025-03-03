import item_instances
import os
import core.rules as rls
import item_model
"""Functions used for the item shop."""

# Shop names.
shop_name_general_items = "GENERAL ITEMS"
shop_name_weapons = "WEAPONS"
shop_name_projectiles = "PROJECTILES"
shop_name_armor = "ARMOR"
shop_name_inventory = "INVENTORY"


def set_shop(character, shop_name):
    """Set 'instance_list' and 'table_header' for formatted output based on selected shop 'shop_name' and call function
    'trade_items()' to initialize trade loop."""

    # Set 'shop_name' to uppercase. Function is called from function 'show_main_shop' in module 'state_manager.py' with
    # the argument given as title case string, but further use in uppercase necessary in this module.
    shop_name = shop_name.upper()

    # Set 'instance_list' and 'table_header' based on selected shop.
    if shop_name == shop_name_general_items:
        instance_list = item_instances.general_items
        table_header = f"{"Weight":>42}{"Cost":>10}{"Inventory":>12}"
    elif shop_name == shop_name_weapons:
        # NOTE: Weapons shop not fully implemented yet!
        weapons_shop(character)
        return
    elif shop_name == shop_name_projectiles:
        instance_list = item_instances.projectiles
        table_header = f"{"Weight":>45}{"Damage":>8}{"Cost":>10}{"Inventory":>12}"
    elif shop_name == shop_name_armor:
        instance_list = item_instances.armors
        table_header = f"{"Weight":>30}{"AC":>10}{"Cost":>10}{"Inventory":>12}"
    elif shop_name == shop_name_inventory:
        # Check if inventory is empty.
        if character.inventory:
            instance_list = character.inventory
            table_header = f"{"Weight":>42}{"Cost":>10}{"Inventory":>12}"
        else:
            # Exit function if inventory is empty and skip function call 'trade_items'.
            print("\n\tYour inventory is empty.")
            input("\nPress enter to return to shop")
            os.system('cls')
            return

    # Start trade loop for selected shop.
    trade_items(character, instance_list, shop_name, table_header)


def weapons_shop(character):  # TODO Fully implement weapons shop.
    """Print items in list 'weapons' from module 'item_instances' in formatted string output."""
    # Show equipped weapon.
    show_equipped(shop_name_weapons, character)

    # Initialize shop counter.
    shop_counter = 1

    print(shop_name_weapons)
    for k, v in item_instances.weapons.items():
        print("\n\n" + k)

        if k == "Ranged Weapons":
            print(f"{"Range":>50}")
            print(f"{"Size":>27}{"Weight":>9}{"S    M    L":^23}{"Cost":>8}")
            for item in v:
                ranges = f"{item.range_list[0]:>3}, {item.range_list[1]:>3}, {item.range_list[2]:>3}"
                print(f"{shop_counter:>2} - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{ranges:^23}"
                      f"{f"{item.cost} gp":>8}")
                shop_counter += 1

        else:
            print(f"{"Size":>27}{"Weight":>9}{"Damage":>8}{"Cost":>10}")
            for item in v:
                print(f"{shop_counter:>2} - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"1d{item.damage}":>8}"
                      f"{f"{item.cost} gp":>10}")
                shop_counter += 1

    input("\nPress enter to return to shop")
    os.system('cls')


def trade_items(character, instance_list, shop_name, table_header):
    """Initialize trade loop for item shops.
    ARGS:
        character: instance of Character class.
        instance_list: list of instances of Item class and child classes. Lists found in 'item_instances.py'.
        shop_name: String for name of the shop. Either "GENERAL ITEMS", "WEAPONS", "PROJECTILES", "ARMOR" or "INVENTORY".
        table_header: formatted string for header of shop inventory.
    """
    while True:
        # Show equipped items based on selected shop.
        show_equipped(shop_name, character)
        # Print shop in formatted output and get int value ('instance_list' index + 1) for each item.
        shop_counter = show_shop(character, instance_list, shop_name, table_header)
        trade_item = input("\nChoose item to trade or press 'Enter' to return to shop menu: ")

        invalid_input_message = (f"\n\tInvalid input. Choose a number between 1 and {shop_counter - 1}. Press 'Enter' to "
                                 f"continue.")

        if not trade_item:
            os.system('cls')
            break
        else:
            try:
                selected_item = instance_list[int(trade_item) - 1]
                choose_buy_sell(character, selected_item)
            except IndexError:
                input(invalid_input_message)
                os.system('cls')
                continue
            except ValueError:
                input(invalid_input_message)
                os.system('cls')
                continue


def show_shop(character, instance_list, shop_name, table_header):
    """Show formatted output of selected shop with appropriate class attributes and return int 'counter' for use in
    function 'trade_items()'.
    ARGS:
        character: instance of Character class.
        instance_list: list of instances of Item class and child classes. Lists found in 'item_instances.py'.
        shop_name: String for name of the shop.
        table_header: formatted string for header of shop inventory.
    RETURN:
        shop_counter: int for number of items in shop.
    """
    # Initialize counter for items in shop.
    shop_counter = 1

    # List to check for items already in inventory, so that they appear only once in shop 'INVENTORY'.
    inventory_list = []

    print(f"{shop_name}:")
    print(f"{table_header}")

    for item in instance_list:
        # Select appropriate table format for shop.
        if shop_name == shop_name_general_items:
            table_format = f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}"
        elif shop_name == shop_name_projectiles:
            table_format = (f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>10}"
                            f"{f"1d{item.damage}":>8}{f"{item.cost} gp":>10}")
        elif shop_name == shop_name_armor:
            table_format = (f"{shop_counter:>2} - {item.name:<15}{f"{item.weight} lbs":>10}{item.armor_class:>10}"
                            f"{f"{item.cost} gp":>10}")
        elif shop_name == shop_name_inventory:
            table_format = f"{shop_counter:>2} - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}"

        # Print items in shop and amount of items in character inventory.
        # List 'inventory_list' and if-elif statements ensure that each item is listed only once if shop 'INVENTORY'
        # is chosen.
        if item in character.inventory and item not in inventory_list:
            inventory = character.inventory.count(item)
            print(table_format + f"{inventory:>8}")
            inventory_list.append(item)
            shop_counter += 1
        elif item in character.inventory and item in inventory_list:
            pass
        else:
            print(table_format)
            shop_counter += 1

    print(f"\nYour money: {character.money} gp")
    return shop_counter


def show_equipped(shop_name, character):
    """Print equipped items in formatted output. Output format is dependent on chosen shop.
    ARGS:
        shop_name: String for name of the shop.
        character: instance of Character class.
    """
    # Format strings for table headers.
    table_header_armor = f"{"AC":>37}{"Weight":>9}"
    table_header_inventory = f"{"AC":>37}{"Weight":>9}{"Damage":>9}"
    table_header_weapons = f"{"Damage":>37}{"Size":>8}{"Weight":>9}"
    # Dicts to show correct equipment slots for each shop.
    slot_dict_armor = {"Armor:": character.armor, "Shield:": character.shield,}
    slot_dict_inventory = {"Armor:": character.armor, "Shield:": character.shield, "Weapon:": character.weapon,}
    slot_dict_weapons = {"Weapon:": character.weapon,}

    # Check if shop has items that can be equipped.
    if shop_name not in [shop_name_armor, shop_name_inventory, shop_name_weapons]:
        pass
    else:
        print("Equipped Items:")

        if shop_name == shop_name_armor:
            print(table_header_armor)

            for k, v in slot_dict_armor.items():
                # Different output format for shield AC.
                if v.shield:
                    # Check if shield is equipped.
                    if v == item_instances.no_shield:
                        print(f"{k:<10}No shield equipped")
                    else:
                        print(f"{k:<10}{v.name:<20}{f"+{v.armor_class}":>7}{v.weight:>5} lbs")

                else:
                    print(f"{k:<10}{v.name:<20}{v.armor_class:>7}{v.weight:>5} lbs")

        elif shop_name == shop_name_inventory:
            print(table_header_inventory)

            for k, v in slot_dict_inventory.items():
                # Different output format for armor and weapons.
                if isinstance(v, item_model.Weapon):
                    # Check if weapon is equipped.
                    if v == item_instances.no_weapon:
                        print(f"{k:<10}No weapon equipped")
                    else:
                        print(f"{k:<10}{v.name:<20}{v.weight:>12} lbs{f"1d{v.damage}":>9}")

                else:
                    if v.shield:
                        # Check if shield is equipped.
                        if v == item_instances.no_shield:
                            print(f"{k:<10}No shield equipped")
                        else:
                            print(f"{k:<10}{v.name:<20}{f"+{v.armor_class}":>7}{v.weight:>5} lbs")
                    else:
                        print(f"{k:<10}{v.name:<20}{v.armor_class:>7}{v.weight:>5} lbs")

        elif shop_name == shop_name_weapons:
            # Check if weapon is equipped.
            if character.weapon == item_instances.no_weapon:
                print("No weapon equipped")

            else:
                print(table_header_weapons)

                for k, v in slot_dict_weapons.items():
                    print(f"{k:<10}{v.name:<20}{f"1d{v.damage}":>7}{v.size:>7}{v.weight:>6} lbs")

        print("\n")


def choose_buy_sell(character, selected_item):
    """Check if 'selected_item' is in class attribute 'character.inventory'. Let user choose to sell or buy item or only
    prompt for buy confirmation if 'selected_item' is not in 'character.inventory'. Call class methods
    'character.buy_item', 'character.sell_item' or abort trade based on user input.
    ARGS:
        character: instance of Character class.
        selected_item: list item selected in function 'trade_items()' through user input.
    """
    buy_sell_prompt = "Do you want to buy or sell this item? "
    buy_amount_prompt = f"\nHow many '{selected_item.name}(s)' do you want to buy? "
    sell_amount_prompt = f"\nHow many '{selected_item.name}(s)' do you want to sell? "

    # Check if 'selected_item' is in characters inventory.
    if selected_item in character.inventory:
        buy_sell_list = [f"Buy '{selected_item.name}'", f"Sell '{selected_item.name}'"]

        # Show buy and sell options if item is in inventory.
        if rls.select_from_list(buy_sell_list, buy_sell_prompt) == buy_sell_list[0]:
            amount = int(input(buy_amount_prompt))
            buy_and_equip(selected_item, character, amount)
        else:
            amount = int(input(sell_amount_prompt))
            sell(selected_item, character, amount)

    # Show buy option only if item is not in characters inventory.
    else:
        amount = int(input(buy_amount_prompt))
        buy_and_equip(selected_item, character, amount)


def buy_and_equip(selected_item, character, amount):
    """Prompt user to enter amount of items and confirm trade and equip item if it is an instance of class 'Armor'.
    ARGS:
        selected_item: selected item from shop. instance of class from 'item_model.py'.
        character: instance of Character class.
        amount: number of 'selected_item' to buy.
    """
    total_cost = selected_item.cost * amount
    confirm_buy_prompt = f"\nAre you sure you want to buy {amount} '{selected_item.name}(s)' for {total_cost} gp (Y/N)? "
    confirm_equip_prompt = f"\n\tDo you want to equip '{selected_item.name}' (Y/N)? "
    added_to_inventory_message = (f"\n\t{amount} '{selected_item.name}(s)' added to your inventory. Press 'Enter' to "
                                  f"continue.")

    if rls.check_yes_no(confirm_buy_prompt):
        if character.buy_item(selected_item, amount):
            input(added_to_inventory_message)
            os.system('cls')

            # Check if item is instance of class Armor and prompt user to equip item if similar item is not equipped yet.
            if (isinstance(selected_item, item_model.Armor) and selected_item != character.armor
                    and selected_item != character.shield):
                if rls.check_yes_no(confirm_equip_prompt):
                    character.equip_item(selected_item)
        else:
            input()
            os.system('cls')


def sell(selected_item, character, amount):
    """Check if trade is valid (enough items in character inventory 'character.inventory') and prompt user to confirm
    trade.
    ARGS:
        selected_item: selected item from shop. instance of class from 'item_model.py'.
        character: instance of Character class.
        amount: number of 'selected_item' to sell.
    """
    # Get amount of 'selected_item' in inventory 'character.items'.
    item_inventory_n = character.inventory.count(selected_item)

    # Check if 'amount' exceeds number of 'selected_item' in character inventory, set confirmation prompt and change
    # 'amount' to max value if necessary.
    if amount > item_inventory_n:
        amount = item_inventory_n
        confirm_sale_prompt = (f"\n\tYou only have {item_inventory_n} '{selected_item.name}'(s) in your inventory!"
                               f"\n\tDo you want to sell all your '{selected_item.name}(s)' for "
                               f"{selected_item.cost*amount} gp (Y/N)? ")
    else:
        confirm_sale_prompt = (f"\n\tAre you sure you want to sell {amount} '{selected_item.name}'(s) for "
                               f"{selected_item.cost * amount} gp (Y/N)? ")

    # Default 'total_revenue' and prompts.
    total_revenue = selected_item.cost * amount
    sale_confirmed_message = (f"\n\t{amount} '{selected_item.name}'(s) sold for {total_revenue} gp. Press 'Enter' to "
                              f"continue.")
    sale_abort_message = "\n\tTrade cancelled. Press 'Enter to return to shop."

    os.system('cls')
    if rls.check_yes_no(confirm_sale_prompt):
        os.system('cls')
        character.sell_item(selected_item, amount)
        input(sale_confirmed_message)
        os.system('cls')
    else:
        os.system('cls')
        input(sale_abort_message)
        os.system('cls')
