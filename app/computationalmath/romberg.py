import numpy as np
import matplotlib.pyplot as plt
import sympy as smp
from flask import render_template


def romberg(func, a, b, acc):
    array_size = 1000
    r = np.empty((array_size, array_size), dtype="object")

    h = b - a
    # trapezoidal rule at first iteration
    r[0][0] = h/2 * (func(a) + func(b))

    for i in range(1, array_size):
        h /= 2
        summ = 0

        for j in range(1, np.power(2, i - 1)):
            summ += func(a + h * (2 * j - 1))

        # trapezoidal rule
        r[i][0] = 0.5 * r[i - 1][0] + h * summ

        # Richardson extrapolation
        for j in range(1, i + 1):
            ij = np.power(4, j)
            r[i][j] = (ij * r[i][j - 1] - r[i-1][j - 1]) / (ij - 1)

        if i > 1 and np.fabs(r[i][i] - r[i - 1][i - 1]) < acc:
            index = np.where(r[:,0]==None)[0][0]
            # rounding
            count_digits = len(str(acc).split('.')[1])
            for k in range (0, index):
                for j in range (0, k + 1):
                    r[k][j] = np.round(r[k][j], count_digits)

            return r[:index, :index]

    raise RuntimeWarning('Romberg function error')


def get_plot(formula, a, b, accuracy):
    # boundaries
    beforeafter = b - a
    # points for the x-axis
    x = np.linspace(a - beforeafter, b + beforeafter, 101)
    
    # allowed function for eval
    allowed_functions = {'__builtins__': {
        'x': x,
        'sqrt': np.sqrt,
        'fabs': np.fabs,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'arcsin': np.arcsin,
        'arccos': np.arccos,
        'arctan': np.arctan
    }}

    # TODO This is fine for a local project, but it has to be changed during deployment (probably via math parser)
    formula = formula.replace('__', 'gdf!56k.jgfhwpe')
    formula = formula.replace('^', '**')
    y = np.array(eval(formula, allowed_functions))
    result = romberg(eval('lambda x:' + formula, allowed_functions), a, b, accuracy)

    # graph
    plt.close()
    formula_LaTeX = smp.latex(smp.sympify(formula))
    plt.plot(x, y, c='blue', label=r'$f(x)=' + formula_LaTeX + '$')
    plt.fill_between(x, y, where=(y>=0) & (x>=a) & (x<=b), color="g", alpha=0.3)
    plt.xlabel('x', fontsize=16)
    plt.ylabel('f(x)', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.savefig('./app/static/images/romberg.png')

    # LaTeX formula
    a = int(a) if a - int(a) == 0.0 else a
    b = int(b) if b - int(b) == 0.0 else b
    formula0 = "R_{0,0}=h_1(f(a)+f(b))"
    formulaT = "R_{i,0}=\\frac{1}{2}R_{i-1} + h_i\sum_{k=1}^{2^{i-1}}f(a+(2k-1)h_i)"
    formulaR = "R_{i,j}=\\frac{1}{4^j-1}(4^jR_{i,j-1}-R_{i-1,j-1})"
    formula_result =  r'\int\limits_{' + str(a) + '}^{' + str(b) + '}' + formula_LaTeX + "dx\\approx" + str(result[-1][-1])

    return render_template('romberg.html', plot_url='static/images/romberg.png', result=result, formula0=formula0,
    formulaRichardson = formulaR, formulaTrapezium=formulaT, formulaResult=formula_result)