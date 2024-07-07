import numpy as np
import matplotlib.pyplot as plt
from flask import render_template


def aitken(x, y, find):
    size = np.shape(x)[0] # obtaining the number of points
    result = np.empty((size, size), dtype="object")
    for i in range(0, size):
        result[i][0] = y[i]
        for j in range(1, i + 1):
            result[i][j] = 1 / (x[i] - x[j - 1]) * (result[j - 1][j - 1] * (x[i] - find) - result[i][j - 1] * (x[j - 1] - find))
            result[i][j] = np.round(result[i][j], 5) # rounding

    return result


def get_plot(x, y, find):
    # finding the approximate value for the given x
    result_array = aitken(x, y, find)

    # intermediate points
    x2 = []
    y2 = []
    for i in range(0, len(x) - 1):
        step = np.abs(x[i] - x[i + 1]) / 10
        left = x[i]
        right = x[i + 1]
        while left < right + step:
            x2.append(left)
            y2.append(aitken(x, y, left)[-1][3])
            left += step

    # graph
    plt.close()
    plt.scatter(x, y, s=15, c='blue')
    plt.scatter(find, result_array[-1][3], 50, c='green')
    plt.plot(x2, y2, c='red')
    plt.xlabel('x', fontsize=16)
    plt.ylabel('f(x)', fontsize=16)
    plt.grid(True)
    plt.savefig('./app/static/images/aitken.png')

    # LaTeX formula
    find = str(int(find) if find - int(find) == 0.0 else find)
    xi = str(int(x[-1]) if x[-1] - int(x[-1]) == 0.0 else x[-1])
    x2 = str(int(x[2]) if x[2] - int(x[2]) == 0.0 else x[2])
    y22 = str(int(result_array[2][2]) if result_array[2][2] - int(result_array[2][2]) == 0.0 else result_array[2][2])
    yi2 = str(int(result_array[-1][2]) if result_array[-1][2] - int(result_array[-1][2]) == 0.0 else result_array[-1][2])
    res = str(int(result_array[-1][3]) if result_array[-1][3] - int(result_array[-1][3]) == 0.0 else result_array[-1][3])
    formula = "{y_{i3}}(x) = \\frac{1}{x_i-x_2}[{y_{22}}(x)\
        ({x_i}-x) - {y_{i2}}(x)({x_2}-x)]"
    formula_numerical = "{y_{i3}}(x) = \\frac{1}{" + xi + "-" + x2 + "}[" + y22 +\
        '(' + xi + '-' + find + ") - " + yi2 + '(' + x2 + '-' + find + ")] =" + res
    
    return render_template('aitken.html', plot_url='static/images/aitken.png', result=result_array, formula=formula, formula_numerical=formula_numerical)

