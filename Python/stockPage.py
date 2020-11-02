import yfinance as yf
from flask import render_template, request





def loadDay():
    stockid = 'MSFT'
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    if request.method == 'POST' and 'stockID' in request.form:
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

        return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                               labels=time, legend=legend, test="")
    values = [20, 21, 263, 10, 10, 10, 10, 10]
    return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels, legend=legend)
