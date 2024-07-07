import numpy as np
import matplotlib.pyplot as plt
from flask import render_template


def derrive(x, y, i, i0, i1, i2):
    """Calculating the derivative using 3 points"""
    x0 = x[i0]
    x1 = x[i1]
    x2 = x[i2]

    a0 = ((2 * x[i] - x1 - x2) / ((x0 - x1) * (x0 - x2))) * y[i0]
    a1 = ((2 * x[i] - x0 - x2) / ((x1 - x0) * (x1 - x2))) * y[i1]
    a2 = ((2 * x[i] - x0 - x1) / ((x2 - x0) * (x2 - x1))) * y[i2]

    return a0 + a1 + a2


def derrive5(x, y, i, i0, i1, i2, i3, i4):
    """Calculating the derivative using 5 points"""
    x0 = x[i0]
    x1 = x[i1]
    x2 = x[i2]
    x3 = x[i3]
    x4 = x[i4]

    a0 = ((((2 * x[i] - x1 - x2) * x3 + (2 * x[i] - x1) * x2 + (2 * x[i] * x1 - 3 * (x[i]**2))) * x4 + ((2 * x[i] - x1) * x2 + (2 * x[i] * x1 - 3 * (x[i]**2))) * x3 + (2 * x[i] * x1 - 3 * (x[i]**2)) * x2 + (4 * (x[i]**3) - 3 * (x[i]**2) * x1)) / ((x0 - x1) * (x0 - x2) * (x0 - x3) * (x0 - x4))) * y[i0]
    a1 = ((((2 * x[i] - x0 - x2) * x3 + (2 * x[i] - x0) * x2 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x4 + ((2 * x[i] - x0) * x2 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x3 + (2 * x[i] * x0 - 3 * (x[i]**2)) * x2 + (4 * (x[i]**3) - 3 * (x[i]**2) * x0)) / ((x1 - x0) * (x1 - x2) * (x1 - x3) * (x1 - x4))) * y[i1]
    a2 = ((((2 * x[i] - x0 - x1) * x3 + (2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x4 + ((2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x3 + (2 * x[i] * x0 - 3 * (x[i]**2)) * x1 + (4 * (x[i]**3) - 3 * (x[i]**2) * x0)) / ((x2 - x0) * (x2 - x1) * (x2 - x3) * (x2 - x4))) * y[i2]
    a3 = ((((2 * x[i] - x0 - x1) * x2 + (2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x4 + ((2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x2 + (2 * x[i] * x0 - 3 * (x[i]**2)) * x1 + (4 * (x[i]**3) - 3 * (x[i]**2) * x0)) / ((x3 - x0) * (x3 - x1) * (x3 - x2) * (x3 - x4))) * y[i3]
    a4 = ((((2 * x[i] - x0 - x1) * x2 + (2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x3 + ((2 * x[i] - x0) * x1 + (2 * x[i] * x0 - 3 * (x[i]**2))) * x2 + (2 * x[i] * x0 - 3 * (x[i]**2)) * x1 + (4 * (x[i]**3) - 3 * (x[i]**2) * x0)) / ((x4 - x0) * (x4 - x1) * (x4 - x2) * (x4 - x3))) * y[i4]

    return a0 + a1 + a2 + a3 + a4


def finiteddifferences(x, y):
    size = np.shape(x)[0]
    v = np.zeros(size, dtype="float")
    for i in range(0, size):
        if i == 0:
            v[i] = derrive(x, y, i, i, i + 1, i + 2) # derivative at the beginning
        elif i == size - 1:
            v[i] = derrive(x, y, i, i - 2, i - 1, i) # derivative at the end
        else:
            v[i] = derrive(x, y, i, i - 1, i, i + 1)
        v[i] = np.round(v[i], 5) # rounding

    return v


def finiteddifferences5(x, y):
    size = np.shape(x)[0]
    v = np.zeros(size, dtype="float")
    for i in range(0, size):
        if i == 0:
            v[i] = derrive5(x, y, i, i, i + 1, i + 2, i + 3, i + 4) # derivative at the beginning
        elif i == 1:
            v[i] = derrive5(x, y, i, i - 1, i, i + 1, i + 2, i + 3) # derivative at the second point
        elif i == size - 2:
            v[i] = derrive5(x, y, i, i - 3, i - 2, i - 1, i, i + 1) # derivative at the penultimate point
        elif i == size - 1:
            v[i] = derrive5(x, y, i, i - 4, i - 3, i - 2, i - 1, i) # derivative at the end
        else:
            v[i] = derrive5(x, y, i, i - 1, i - 2, i, i + 1, i + 2)
        v[i] = np.round(v[i], 5) # rounding

    return v


def get_plot(x, y):
    result = finiteddifferences(x, y)
    result5 = finiteddifferences5(x, y)

    # graph
    plt.close()
    plt.scatter(x, y, s=15, c='blue')
    plt.scatter(x, result, s=15, c='red')
    plt.scatter(x, result5, s=15, c='green')
    plt.plot(x, y, c='blue', label = r'$f(x)$')
    plt.plot(x, result, c='red', label = r"$f'(x)$")
    plt.plot(x, result5, c='green', label = r"$f'(x)$")
    plt.xlabel(r'$x$', fontsize=16)
    plt.ylabel(r'$f(x)$', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.savefig('./app/static/images/polylagrangederivative.png')

    # LaTeX formula
    formula3 = "{P}'(x)= \\frac{2x - x_1 - x_2} {(x_0-x_1)(x_0-x_2)}y_0 + \\frac{2x - x_0 - x_2} {(x_1-x_0)(x_1-x_2)}y_1 + \\frac{2x - x_0 - x_1} {(x_2-x_0)(x_2-x_1)}y_2"
    formula5 = "{P}'(x)= \\frac{d}{dx}(\\frac{(x-x_1)(x-x_2)(x-x_3)(x-x_4)} {(x_0-x_1)(x_0-x_2)(x_0-x_3)(x_0-x_4)}y_0 + \\frac{(x-x_0)(x-x_2)(x-x_3)(x-x_4)} {(x_1-x_0)(x_1-x_2)(x_1-x_3)(x_1-x_4)}y_1 + \
        \\frac{(x-x_0)(x-x_1)(x-x_3)(x-x_4)} {(x_2-x_0)(x_2-x_1)(x_2-x_3)(x_2-x_4)}y_2 + \\frac{(x-x_0)(x-x_1)(x-x_2)(x-x_4)} {(x_3-x_0)(x_3-x_1)(x_3-x_2)(x_3-x_4)}y_3 + \
        \\frac{(x-x_0)(x-x_1)(x-x_2)(x-x_3)} {(x_4-x_0)(x_4-x_1)(x_4-x_2)(x_4-x_3)}y_4)"

    return render_template('polylagrangederivative.html', plot_url='static/images/polylagrangederivative.png', result=result, result5=result5, x=x, y=y, formula3=formula3, formula5=formula5)