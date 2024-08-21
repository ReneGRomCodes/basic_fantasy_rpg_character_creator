import item_instances
"""Functions used for the item shop."""


def show_shop():
    print("General Items:")
    print(f"{"Weight":>40}{"Cost":>10}")
    for item in item_instances.general_items:
        print(f" - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}")

    print("\nWeapons:")
    for k, v in item_instances.weapons.items():
        print(k)
        if k == "Ranged Weapons":
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"{item.cost} gp":>18}")
        else:
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"1d{item.damage}":>8}{f"{item.cost} gp":>10}")

    print("\nProjectiles:")
    for projectile in item_instances.projectiles:
        print(f" - {projectile.name}")

    print("\nArmor:")
    print(f"{"Weight":>28}{"AC":>10}{"Cost":>10}")
    for armor in item_instances.armors:
        print(f" - {armor.name:<15}{f"{armor.weight} lbs":>10}{armor.armor_class:>10}{f"{armor.cost} gp":>10}")


# show_shop()
# input()
