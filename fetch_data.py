import colorama
import datetime as dt
import pandas as pd
import pandas_datareader as web
import numpy as np
import os


def yahoo_fetcher(ticker):
    start_date = "2000-01-01"
    yesterday = dt.date.today() - dt.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    yesterday = dt.datetime.strptime(yesterday, "%Y-%m-%d")
    os.mkdir("data")
    os.chdir("data")
    ticker_name = str(ticker + ".NS")
    ticker_file = str(ticker_name + ".csv")

    if os.path.exists(ticker_file):
        print("Stock File Exists")
        data = pd.read_csv(ticker_file)
        length = len(data["Date"]) - 1
        last_date = data["Date"][length]
        last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
        

        if(last_date != yesterday):
            print("File not upto date")
            print("Updating File")
            data = web.get_data_yahoo(ticker_name, start_date, yesterday)
            data.reset_index(inplace=True,drop=False)
            data.to_csv(ticker_file)
            print("File Updated")


        else:
            print("File upto date")
            

    
    else:
        print("\033[0;37;41m File does not exist.")
        print("\033[0;37;40m")
        print("Fetching...\n")
        data = web.get_data_yahoo(ticker_name, start_date, yesterday)
        data.reset_index(inplace=True,drop=False)
        data["Date"] = pd.to_datetime(data["Date"])
        data.to_csv(ticker_file)
    if ("Unnamed: 0" in data.columns):
        data.drop("Unnamed: 0", inplace = True, axis = 1)
    os.chdir("..")
    print("\033[0;37;40m")
    return data
