import requests #import the modules
import datetime

stockOpen = [] #initializes the lists needed for taking in stock info
stockHigh = []
stockClose = []
stockLow = []
stockDate = []

symbol = "GOOGL"
chartType = "line"
timeSeries = "TIME_SERIES_MONTHLY" #temporary variables to run the code
apiKey = "8Y14W33YBDR4EUWS" # I did not see your apiKey so you can use this one or import the one you got Cameron
interval = "5min"
dateStart = "2021-04-09"
dateEnd = "2022-08-09"


#Uses DateTime Function to get dates in ints so we can parse through data later on, Does not contain seconds since I am getting a funky error currently
dateStart = datetime.datetime(int(dateStart[0:4]), int(dateStart[5:7]), int(dateStart[8:10])) 
dateEnd = datetime.datetime(int(dateEnd[0:4]), int(dateEnd[5:7]), int(dateEnd[8:10]))


#The name of the data in the JSON files is not consistent for some reason, so this intializes variable depending on what time series the user chooses. 
if (timeSeries == "TIME_SERIES_MONTHLY"):
    jsonLoop = "Monthly Time Series" 
elif(timeSeries == "TIME_SERIES_DAILY"):
    jsonLoop = "Time Series (Daily)"
elif(timeSeries == "TIME_SERIES_INTRADAY"):
    jsonLoop = "Time Series ("+interval+")"
elif(timeSeries == "TIME_SERIES_WEEKLY"):
    jsonLoop = "Weekly Time Series"


#The intraday Time Series requires a seperate request url, so this calls the function and initializes url so the retrieval works for it
if(timeSeries == "TIME_SERIES_INTRADAY"):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" +symbol+ "&interval=" +interval+ "&outputsize=full&apikey=" +apiKey

#Weekly Monthly and Daily api fetch is all the same so this will access all the information
else:
    url = "https://www.alphavantage.co/query?function=" +timeSeries+ "&symbol=" +symbol+ "&outputsize=full&apikey=" +apiKey

r = requests.get(url) # Gets the information from the api


data = r.json()



for d in data[jsonLoop]: #Loop to go through all fethced data

    date = datetime.datetime(int(d[0:4]), int(d[5:7]), int(d[8:10])) #Converts each data into 
    
    if(date >= dateStart and date <= dateEnd): #Does an if statement that will add data to each respective list when the date of the data is inbetween the start and end date
        stockInfo = data[jsonLoop][d]


        stockOpen.append(float(stockInfo["1. open"]))
        stockHigh.append(float(stockInfo["2. high"])) #adds all data to each respective list
        stockLow.append(float(stockInfo["3. low"]))
        stockClose.append(float(stockInfo["4. close"]))
        stockDate.append(date)

for i in stockOpen:
    print(i)


    





