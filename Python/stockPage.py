import yfinance as yf
from flask import render_template, request
stockid = ""


def loadDay():
    legend = "Day"
    stockid = request.form['stockID']
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

    return history, stockid.upper(), time, legend
def loadWeek():
    legend = "Week"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="5d", interval="30m")
    time = list()
    for row in history.index:
        date = "{}/{}" .format(row.month, row.day)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend


def loadMonth():
    legend = "Month"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="1mo", interval="1d")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend


def load3Month():
    legend = "3 Months"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="3mo")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend


def load6Month():
    legend = "6 Months"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="6mo")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend


def loadYear():
    legend = "Year"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="1y")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend

def load5Year():
    legend = "5 Years"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="5y")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history, stockid.upper(), time, legend


def loadAllTime():
    legend = "All Time"
    stockid = (request.form['stockID'])
    stockData = yf.Ticker(stockid)
    history = stockData.history(period="max")
    time = list()
    for row in history.index:
        date = "{}/{}/{}" .format(row.month, row.day, row.year)
        time.append(date)
    currentPrice = history['Open'].iloc[-1]

    return history.iloc[:, :5], stockid.upper(), time, legend
