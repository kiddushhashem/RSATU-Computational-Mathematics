from flask import Flask
import matplotlib


matplotlib.use('Agg')


app = Flask(__name__)


from app import routes
