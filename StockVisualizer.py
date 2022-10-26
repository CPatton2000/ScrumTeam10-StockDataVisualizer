
import pygal
from lxml import *

class graphResults:
    def graph(data, graphType):
        #data is passed to this function as a dictionary of api results. 
        dateLessData = data.values()
        opens = []
        highs = []
        lows = []
        close = []
        #volumes = []

        for x in dateLessData:
            opens.append(float(x.get("1. open")))
            highs.append(float(x.get("2. high")))
            lows.append(float(x.get("3. low")))
            close.append(float(x.get("4. close")))
            #volumes.append(float(x.get("5. volume")))

        if graphType == 0:
            chart = pygal.Bar()
            chart.add("Opens", opens)
            chart.add("Highs", highs)
            chart.add("Lows", lows)
            chart.add("Closes", close)
            #chart.add("Volumes", volumes)
            chart.render_in_browser()
        else:
            chart = pygal.Line()
            chart.add("Opens", opens)
            chart.add("Highs", highs)
            chart.add("Lows", lows)
            chart.add("Closes", close)
            #chart.add("Volumes", volumes)
            chart.render_in_browser()
