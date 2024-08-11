class Item:

    def __init__(self, name, cost, weight):
        self.name = name
        self.cost = cost
        self.weight = weight


class Weapon(Item):

    def __init__(self, name, cost, weight, size, damage):
        super().__init__(name, cost, weight)
        self.size = size
        self.damage = damage


class Armor(Item):

    def __init__(self, name, cost, weight, armor_class):
        super().__init__(name, cost, weight)
        self.armor_class = armor_class
