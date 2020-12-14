import yfinance as yf
from flask import render_template, request
stockid = ""

def loadDay():
    legend = "Daily"
    stockid = request.form['stockID']
    if stockid == "":
        stockid = "MSFT"


    stockData = yf.Ticker(stockid)
    history = stockData.history(period="1d", interval="1m")
    time = list()
    for row in history.index:
        if (row.hour > 12):
            date = "{}:{}".format(row.hour - 12, row.minute)
        else:
            date = "{}:{}".format(row.hour, row.minute)

        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                           labels=time, legend=legend)


def loadMonth():
    legend = "Monthly"
    stockid = request.form['stockID']
    if stockid == "":
        stockid = "MSFT"

    stockData = yf.Ticker(stockid)
    history = stockData.history(period="1d", interval="1m")
    time = list()
    for row in history.index:
        if (row.hour > 12):
            date = "{}:{}".format(row.hour - 12, row.minute)
        else:
            date = "{}:{}".format(row.hour, row.minute)

        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                           labels=time, legend=legend, test="")


def load3Month():
    loadDay()


def load6Month():
    loadDay()


def loadYear():
    loadDay()


def loadAllTime():
    loadDay()
