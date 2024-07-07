import numpy as np


def parse_coordinates(data):
    data = data.replace(' ', '')
    x = np.array(list(map(lambda x: x.split(';')[0], data.split('\n'))))
    y = np.array(list(map(lambda y: y.split(';')[1], data.split('\n'))))
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return x, y