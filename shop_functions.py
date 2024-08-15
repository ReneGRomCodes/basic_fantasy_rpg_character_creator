import item_instances
"""Functions used for the item shop."""


def show_shop():
    print("Basic Items:")
    for item in item_instances.basic_items:
        print(f" - {item.name:<25} {item.weight:>5} lbs {item.cost:>5} gp")

    print("\nWeapons:")
    for weapon in item_instances.weapons:
        print(f" - {weapon.name:<15} {weapon.size} {weapon.weight:>5} lbs       1d{weapon.damage} {weapon.cost:>5} gp")

    print("\nProjectiles:")
    for projectile in item_instances.projectiles:
        print(f" - {projectile.name}")

    print("\nArmor:")
    for armor in item_instances.armors:
        print(f" - {armor.name}")


show_shop()
input()
