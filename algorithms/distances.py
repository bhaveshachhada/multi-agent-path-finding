import operator


def manhattan(position_a, position_b):
    return sum(map(abs, map(operator.sub, position_a, position_b)))


def euclidean(position_a, position_b):
    square_root = lambda x: x**0.5
    square = lambda x: x**2
    return round(square_root(sum(map(square, map(operator.sub, position_a, position_b)))), 2)
