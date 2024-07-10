import random


def dice_roll(n):
    """Roll an n-sided dice and return the result."""
    return random.randint(1, n)


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

