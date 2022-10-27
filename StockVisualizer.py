import pygal
import lxml
import requests
import datetime
import pandas
import json

inUse = True

def nested_dict_pairs_iterator(dict_obj):
    #iterate over all keys and values
    for key, value in dict_obj.items():
        #check if value is dict type
        if isinstance(value, dict):
            #iterates all dict values
            for pair in  nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            #if value isn't dict type, yeild
            yield (key, value)
 
#seperates the JSON data for the graph; checks if dates in the data match with the user input dates and applies the data in a list for the graph 
def dataSeperator(valueKey):
    emptyDict = []
    for dictValues in nested_dict_pairs_iterator(data):
        #checks if data values exist for the user input dates
        for i in dateRange:
            if dictValues[1] == i:
                #adds the corresponding value to the emptyDict list to be returned
                if dictValues[2] == valueKey:
                    emptyDict.append(dictValues[3])
                
    emptyDict = [eval(i) for i in emptyDict]
    #data in JSON is presented in descending order when the graph needs it in ascending: reverse makes the data order correct
    emptyDict.reverse()
    return emptyDict

def dateChecker():
    emptySet = set()
    emptyList = []
    for dictValues in nested_dict_pairs_iterator(data):
        for i in dateRange:
            if dictValues[1] == i:
                if i not in emptySet:
                    emptySet.add(i)
                    emptyList.append(i)
    emptyList.reverse()
    return emptyList

while inUse == True:
    #User symbol Input
    userSymbol = input("\nEnter the stock symbol you are looking for: ")

    #Chart Type selection, including error checking for string values or invalid integers
    while True:
        try:
            print("\nChart Types \n ------------------------------ \n 1. Bar \n 2. Line \n")
            chartType = int(input("Enter the chart type you want (1, 2): "))
            if chartType < 1 or chartType > 2:
                print("\nThe value needs to be either 1 or 2 \n")
                continue
        except ValueError:
            print("\n The value needs to be an integer \n")
            continue
        else:
            break

    #Time Series selection, including error checking for string values or invalid integers
    while True:
        try:
            print("\nSelect the Time Series of the chart you want to generate \n -------------------------------------------- \n 1. Intraday \n 2. Daily \n 3. Weekly \n 4. Monthly \n")
            timeSeries = int(input("Enter time series option (1, 2, 3, 4): "))
            if timeSeries < 1 or timeSeries > 4:
                print("\nThe value needs to be either 1, 2, 3, or 4 \n")
                continue
        except ValueError:
            print("\n The value needs to be an integer \n")
            continue
        else:
            break

    #Start Date Input, including error checking for incorrect date format        
    while True:
        try:
            startDate = input("\nEnter the start date (YYYY-MM-DD): ")
            checkStartDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        except ValueError:
            print("\nIncorrect date format, the format should be YYYY-MM-DD\n")
            continue
        else:
            break

    #End Date input, including error checking for incorrect date format and end date being before start date
    while True:
        try:
            endDate = input("\nEnter the end date (YYYY-MM-DD): ")
            checkEndDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
            if checkStartDate > checkEndDate:
                print("\nThe end date cannot begin before the start date\n")
                continue
        except ValueError:
            print("\nIncorrect date format, the format should be YYYY-MM-DD\n")
            continue
        else:
            break
            
    #Time series checker that queries the API depending on time series user input; also sets range of dates based on time series
    if timeSeries == 1:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + userSymbol + '&outputsize=full&interval=60min&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        dateRange = pandas.date_range(startDate, endDate, freq='H').strftime('%Y-%m-%d %h:%m:%s')
    elif timeSeries == 2:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        dateRange = pandas.date_range(startDate, endDate, freq='D').strftime('%Y-%m-%d')
    elif timeSeries == 3:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        dateRange = pandas.date_range(startDate, endDate, freq='D').strftime('%Y-%m-%d')
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        dateRange = pandas.date_range(startDate, endDate, freq='D').strftime('%Y-%m-%d')

    #dataSeperator calls
    openData = dataSeperator("1. open")
    highData = dataSeperator("2. high")
    lowData = dataSeperator("3. low")
    closeData = dataSeperator("4. close")

    xDate = dateChecker()

    #Chart checking and applying all data into the browser chart display
    if chartType == 2:
       line_chart = pygal.Line(x_label_rotation=45)
       line_chart.title = 'Stock Data for ' + userSymbol + ': ' + startDate + ' to ' + endDate
       line_chart.x_labels = xDate
       line_chart.add('Open', openData)
       line_chart.add('High', highData)
       line_chart.add('Low',  lowData)
       line_chart.add('Close', closeData)
       line_chart.render_in_browser()
    else:
       bar_chart = pygal.Bar(x_label_rotation=45)
       bar_chart.title = 'Stock Data for ' + userSymbol + ': ' + startDate + ' ' + endDate
       bar_chart.x_labels = xDate
       bar_chart.add('Open', openData)
       bar_chart.add('High', highData)
       bar_chart.add('Low',  lowData)
       bar_chart.add('Close', closeData)
       bar_chart.render_in_browser()
       
    continueUse = str(input("Do you want to view more stock data? Enter 'y' to continue or 'n' to quit: "))
    if continueUse == "n":
        quit()
    else:
        continue
