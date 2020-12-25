#app.py
# a page for wind monitoring
# author: hyh
from flask import Flask, render_template
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas
import math
from windVisual import drawTimeSeries,  drawFrequencyDistribution, drawFrequencyRose


app = Flask(__name__)


@app.route("/plot/<func>")
def plot_graph(func='Wind Direction'):

    start = 0
    end = -1 
    dataDt = 60
    SECPERHOUR = 3600
    SECPERDAT = 24*60*60
    SECPERWEEK = SECPERDAT*7

    options = func.split("_")
    func = options[0] + "_" + options[1]
    if options[2] == "all":
        print("plot all the value")
    if options[2] == "hour":
        print("plot 1 hour value")
        start = int(-SECPERHOUR/dataDt)
    if options[2] == "day":
        print("plot 1 day value")
        start = int(-SECPERDAT/dataDt)
    if options[2] == "week":
        print("plot 1 week value")
        start = int(-SECPERWEEK/dataDt)

    f = pandas.read_excel('20170420から20170426.xlsx')
    fig = Figure(figsize=[12,6])
    print("Run ", func)
    if func == 'TH_Wind Direction':
        drawTimeSeries(fig, f[f.columns[0]][start:end],f[f.columns[1]][start:end], subname=options[1])
    if func == 'TH_Wind speed 1':
        drawTimeSeries(fig, f[f.columns[0]][start:end],f[f.columns[2]][start:end], subname=options[1])
    if func == 'TH_Wind speed 2':
        drawTimeSeries(fig, f[f.columns[0]][start:end],f[f.columns[3]][start:end], subname=options[1])
    if func == 'DS_Wind speed 1':
        drawFrequencyDistribution(fig,f[f.columns[2]][start:end], subname=options[1])
    if func == 'DS_Wind speed 2':
        drawFrequencyDistribution(fig,f[f.columns[3]][start:end], subname=options[1])
    if func == "RS_Wind Direction":
        drawFrequencyRose(fig,f[f.columns[1]][start:end], subname=options[1])
    
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data

@app.route("/update/<func>")
def update(func='Wind Direction'):
    print("Update!!!!!!!!!!!")
    return "1"



@app.route("/")
def index():
    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True, port=9999)