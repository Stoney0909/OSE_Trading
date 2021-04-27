from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import MySQLdb
from flask import request, session, render_template, flash
import app
from app import *
from flask import Blueprint
from Python import stockPage

stock_Account_api = Blueprint('stock_Account_api', __name__)
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")


@stock_Account_api.route('/StockMarket', methods=['GET', 'POST'])
def stock_page():
    stockid = ''
    legend = ''
    labels = []
    if request.method == 'POST' and 'stockID' in request.form:
        session['IdOfSearch'] = request.form['stockID']
        if request.form.get("Day"):
            try:
                history, stockid, time, legend = stockPage.loadDay()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")


        elif request.form.get("Week"):
            try:
                history, stockid, time, legend = stockPage.loadWeek()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("Month"):
            try:
                history, stockid, time, legend = stockPage.loadMonth()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("3_Month"):
            try:
                history, stockid, time, legend = stockPage.load3Month()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("6_Month"):
            try:
                history, stockid, time, legend = stockPage.load6Month()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("Year"):
            try:
                history, stockid, time, legend = stockPage.loadYear()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("5_year"):
            try:
                history, stockid, time, legend = stockPage.load5Year()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        elif request.form.get("All_Time"):
            try:
                history, stockid, time, legend = stockPage.loadAllTime()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")
        else:
            try:
                history, stockid, time, legend = stockPage.loadDay()
                session['IdOfSearch'] = stockid
                return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                       labels=time, legend=legend, message="")
            except:
                values = []
                return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, message="Stock does not exist!")

    session['IdOfSearch'] = stockid
    values = []
    return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels, legend=legend,
                           message="")

def GetGameID():
     ID = 1 #app.GetGameID()
     return ID

@stock_Account_api.route('/Portfolio', methods=['GET', 'POST'])
def portfolio_Page():
    msg = ''
    sellOrNot = 0.0
    totalGain = 0.0
    number = 0.0
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transactions_Table WHERE trading_ID = %s and GameID = %s', (session['id'], session['gameID']))

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM transactions_Table WHERE numberOfShareSold != numberOfShareAtBuying AND trading_ID = %s and GameID = %s',
            (session['id'], session['gameID']))
        account = cursor.fetchall()
        if account:  # if there is data in here
            for i in range(0, len(account)):
                msg = si.get_live_price(account[i]['symbol_Of_Stock'])
                msg = format(msg, ".2f")
                account[i]['sellSharePrice'] = msg
                sellOrNot = float(account[i]['numberOfShareAtBuying']) - float(account[i]['numberOfShareSold'])
                account[i]['Gain'] = format(
                    (sellOrNot * float(msg) - sellOrNot * float(account[i]['priceOfShareAtBuying'])), ".2f")
                totalGain = totalGain + float(account[i]['Gain'])

            totalGain = format(totalGain, ".2f")
            msg = account
            return render_template('Portfolio_page.html', account=account, len=len(account), msg=msg,
                                   totalGain=totalGain)
        else:
            return render_template('Portfolio_page.html', account=account, len=len(account), msg=msg,
                                   totalGain=totalGain)
    else:
        profitOrLoss = 0.0
        post_id = request.form['Sell']
        session['Transaction_ID'] = post_id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM transactions_Table WHERE transactions_ID = %s and GameID = %s',
                       (post_id, session['gameID']))
        account = cursor.fetchall()
        if account:
            for i in range(0, len(account)):
                number = int(account[i]['numberOfShareAtBuying']) - int(account[i]['numberOfShareSold'])
                stockID = account[i]['symbol_Of_Stock']
                msg = si.get_live_price(account[i]['symbol_Of_Stock'])
                msg = format(msg, ".2f")
                account[i]['sellSharePrice'] = msg
                account[i]['Gain'] = format((float(account[i]['numberOfShareAtBuying']) * float(msg) -
                                             float(account[i]['numberOfShareAtBuying']) * float(
                            account[i]['priceOfShareAtBuying'])), ".2f")
                profitOrLoss = format(float(account[i]['Gain']), ".2f")
        stockid, values, time, legend, msg, company_name = getGraph(stockID)
        return render_template('Sell_stock.html', stockid=stockid, values=values,
                               legend=legend,labels =time, price=msg, number=number, profitOrLoss=profitOrLoss,
                               company_name=company_name)
    account, len2, msg, totalGain = getTable()
    return render_template('Portfolio_page.html', account=account, len=len2, msg=msg,
                           totalGain=totalGain)


# getting the graph
def getGraph(nameOfStock):
    legend = "Monthly Data"
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    stockData = yf.Ticker(session['IdOfSearch'])
    stockID = session['IdOfSearch']
    history = stockData.history(period="1d", interval="1m")
    time = list()
    for row in history.index:
        if (row.hour > 12):
            minute = format(row.minute, '02d')
            date = "{}:{}".format(row.hour - 12, minute)
        else:
            minute = format(row.minute, '02d')
            date = "{}:{}".format(row.hour, minute)
        time.append(date)

    company_name = stockData.info['longName']
    currentPrice = history['Open'].iloc[-1]
    stockid = company_name
    history['Open'] = history['Open'].apply(lambda x: x * ConvertNumber())

    history['Open'] = history['Open'].round(2)
    values = history['Open']
    msg = currentPrice
    return stockid, values, time, legend, msg, company_name


# stockid=company_name, values=history['Open'],labels=time, legend=legend, msg=msg, company_name=company_name
# getting the Table
def getTable():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transactions_Table WHERE trading_ID =%s and GameID = %s',
                   (session['id'], session['gameID'],))
    account = cursor.fetchall()
    if account:
        for i in range(0, len(account)):
            msg = si.get_live_price(account[i]['symbol_Of_Stock'])  # getting stock prices
            msg = format(msg, ".2f")
            account[i]['sellSharePrice'] = msg
            account[i]['Gain'] = format((float(account[i]['numberOfShareAtBuying']) * float(msg) -
                                         float(account[i]['numberOfShareAtBuying']) * float(
                        account[i]['priceOfShareAtBuying'])), ".2f")
            totalGain = totalGain + float(account[i]['Gain'])
        totalGain = format(totalGain, ".2f")
        msg = account
    return account, len(account), msg, totalGain


def ConvertNumber():
    if get_locale() == 'fr':  # convert to euros
        return exchangeToEuros
    if get_locale() == 'es':  # convert to spanish
        return exchangeToPesos
    if get_locale() == 'zh':  # convert to chinese
        return exchangeToYen
    else:
        return 1
