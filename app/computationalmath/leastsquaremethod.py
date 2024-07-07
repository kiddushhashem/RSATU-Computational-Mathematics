import numpy as np
import matplotlib.pyplot as plt
from flask import render_template


def gaussMethod(left_matrix, right_matrix):
    matrix_size = np.shape(left_matrix)[0]
    result = np.zeros(matrix_size)
    # remove zeros on the main diagonal of the matrix
    for i in range(0, matrix_size):
        if left_matrix[i][i] != 0:
            continue
        for j in range(0, matrix_size):
            if i == j:
                continue
            if left_matrix[j][i] == 0 or left_matrix[i][j] == 0:
                continue
            left_matrix[[j, i]] = left_matrix[[i, j]]
            right_matrix[[j, i]] = right_matrix[[i, j]]
            break

    # reducing the matrix to triangular form
    for i in range(0, matrix_size):
        if left_matrix[i][i] == 0:
            raise Exception("There is no solution!")
        for j in range(i + 1, matrix_size):
            scaling_factor = left_matrix[j][i] / left_matrix[i][i]
            for k in range(i, matrix_size):
                left_matrix[j][k] -= scaling_factor * left_matrix[i][k]
            right_matrix[j] -= scaling_factor * right_matrix[i]

    # calculating the coefficients
    for i in range(matrix_size - 1, -1, -1):
        s = 0
        for j in range(i, matrix_size):
            s = s + left_matrix[i][j] * result[j]
        result[i] = (right_matrix[i] - s) / left_matrix[i][i]

    return result


def leastSquareMethod(x, y, P):
    xy_size = np.shape(x)[0]
    matrix_size = P + 1
    matrix = np.zeros((matrix_size, matrix_size))
    b = np.zeros(P + 1)

    # matrix in the left-hand side of the equation
    for i in range(0, matrix_size):
        for j in range(0, matrix_size):
            for k in range(0, xy_size):
                matrix[i][j] += np.float_power(x[k], i + j)

    # matrix in the right-hand side of the equation
    for i in range(0, matrix_size):
        for j in range(0, xy_size):
            b[i] += np.float_power(x[j], i) * y[j]

    return gaussMethod(matrix, b)


def get_plot(x, y, P):
    result = leastSquareMethod(x, y, P)

    # points for the x and y axes
    approximatedX = np.linspace(np.min(x), np.max(x))
    approximatedY = 0
    for i in range(0, P+1):
        approximatedY += result[i] * np.float_power(approximatedX, i)

    # graph
    plt.close()
    plt.scatter(x, y, s=15, c='blue')
    plt.plot(approximatedX, approximatedY, c='red')
    plt.xlabel(r'$x$', fontsize=16)
    plt.ylabel(r'$f(x)$', fontsize=16)
    plt.grid(True)
    plt.savefig('./app/static/images/leastsquaremethod.png')

    # LaTeX formula
    formula_out = 'f(x)='
    for i in range(P, -1, -1):
        if i == 0:
            formula_out += str(result[i])
        elif i == 1:
            formula_out += str(result[i]) + 'x+'
        else:
            formula_out += str(result[i]) + 'x^{' + str(i) + '}+'
    
    return render_template('leastsquaremethod.html', plot_url='static/images/leastsquaremethod.png', formula=formula_out)