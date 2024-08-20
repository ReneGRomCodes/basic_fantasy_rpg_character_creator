import item_instances
"""Functions used for the item shop."""


def show_shop():
    print("General Items:")
    for item in item_instances.general_items:
        print(f" - {item.name:<30}{f"{item.weight} lbs":>7}{f"{item.cost} gp":>10}")

    print("\nWeapons:")
    for k, v in item_instances.weapons.items():
        print(k)
        if k == "Ranged Weapons":
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{item.cost:>18} gp")
        else:
            for item in v:
                print(f" - {item.name:<20}{item.size}{f"{item.weight} lbs":>10}{f"1d{item.damage}":>8}{item.cost:>10} gp")

    print("\nProjectiles:")
    for projectile in item_instances.projectiles:
        print(f" - {projectile.name}")

    print("\nArmor:")
    for armor in item_instances.armors:
        print(f" - {armor.name}")


# show_shop()
# input()
