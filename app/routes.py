from flask import render_template, request
from app import app
from app.computationalmath import aitken, leastsquaremethod, polylagrangederivative, romberg
from app import utils


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aitken', methods=['GET','POST'])
def aitken_template():
    if request.method == 'POST':
        strCoords = request.form['coordinates']
        x, y = utils.parse_coordinates(strCoords)
        find = request.form['find']
        return aitken.get_plot(x, y, float(find))
    else:
        return render_template('aitken.html')


@app.route('/mnk', methods=['GET','POST'])
def leastsquaremethod_template():
    if request.method == 'POST':
        strCoords = request.form['coordinates']
        x, y = utils.parse_coordinates(strCoords)
        P = request.form['P']
        return leastsquaremethod.get_plot(x, y, int(P))
    else:
        return render_template('leastsquaremethod.html')


@app.route('/polylagrangederivative', methods=['GET','POST'])
def polylagrangederivative_template():
    if request.method == 'POST':
        strCoords = request.form['coordinates']
        x, y = utils.parse_coordinates(strCoords)
        return polylagrangederivative.get_plot(x, y)
    else:
        return render_template('polylagrangederivative.html')


@app.route('/romberg', methods=['GET','POST'])
def romberg_template():
    if request.method == 'POST':
        formula = request.form['formula']
        a = request.form['a']
        b = request.form['b']
        accuracy = request.form['accuracy']
        return romberg.get_plot(formula, float(a), float(b), float(accuracy))
    else:
        return render_template('romberg.html')