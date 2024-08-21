import item_instances
"""Functions used for the item shop."""


def show_shop():
    print("GENERAL ITEMS:")
    print(f"{"Weight":>40}{"Cost":>10}")
    for item in item_instances.general_items:
        print(f" - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}")

    print("\n\nWEAPONS:")
    for k, v in item_instances.weapons.items():
        print("\n", k)
        print(f"{"size":>25}{"weight":>9}{"damage":>8}{"cost":>10}")
        if k == "Ranged Weapons":
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"{item.cost} gp":>18}")
        else:
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"1d{item.damage}":>8}"
                      f"{f"{item.cost} gp":>10}")

    print("\n\nPROJECTILES:")
    print(f"{"weight":>43}{"damage":>8}{"cost":>10}")
    for projectile in item_instances.projectiles:
        print(f" - {projectile.name:<30}{f"{projectile.weight} lbs":>10}{f"1d{projectile.damage}":>8}"
              f"{f"{projectile.cost} gp":>10}")

    print("\n\nARMOR:")
    print(f"{"Weight":>28}{"AC":>10}{"Cost":>10}")
    for armor in item_instances.armors:
        print(f" - {armor.name:<15}{f"{armor.weight} lbs":>10}{armor.armor_class:>10}{f"{armor.cost} gp":>10}")


# show_shop()
# input()
