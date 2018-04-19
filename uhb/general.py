import math


def area_of_steel(D, t):
    print(D, t)
    return math.pi * (D ** 2 - (D - 2 * t) ** 2) / 4


def area_of_coating(D, t_coat):
    return math.pi * ((D + 2 * t_coat) ** 2 - D ** 2) / 4


def internal_area(D, t):
    return math.pi * (D - 2 * t) ** 2 / 4


def total_area(D, t_coat):
    return math.pi * (D + 2 * t_coat) ** 2 / 4
