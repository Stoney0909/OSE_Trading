from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import MySQLdb
from flask import request, session, render_template, flash
from app import mysql
from flask import Blueprint
from Python import stockPage

stock_Account_api = Blueprint('stock_Account_api', __name__)
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")


@stock_Account_api.route('/StockMarket', methods=['GET', 'POST'])
def stock_page():
    stockid =''
    legend = ''
    labels = []
    if request.method == 'POST' and 'stockID' in request.form:

        if request.form.get("Day"):
            history, stockid, time, legend = stockPage.loadDay()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("Week"):
            history, stockid, time, legend = stockPage.loadWeek()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("Month"):
            history, stockid, time, legend = stockPage.loadMonth()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("3_Month"):
            history, stockid, time, legend = stockPage.load3Month()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("6_Month"):
            history, stockid, time, legend = stockPage.load6Month()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("Year"):
            history, stockid, time, legend = stockPage.loadYear()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("5_year"):
            history, stockid, time, legend = stockPage.load5Year()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        elif request.form.get("All_Time"):
            history, stockid, time, legend = stockPage.loadAllTime()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                                   labels=time, legend=legend)
        else:
            history, stockid, time, legend = stockPage.loadDay()
            session['IdOfSearch'] = stockid
            return render_template('StockMarket_page.html', stockid=stockid, values=history['Open'],
                labels=time, legend=legend)


    session['IdOfSearch'] = stockid
    values = []
    return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels, legend=legend)


@stock_Account_api.route('/Portfolio', methods=['GET', 'POST'])
def portfolio_Page():
    msg = ''
    sellOrNot = 0.0
    totalGain = 0.0
    number = 0.0
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transactions_Table WHERE trading_ID = %s', (session['id'],))

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM transactions_Table WHERE numberOfShareSold != numberOfShareAtBuying AND trading_ID = %s',
            (session['id'],))
        account = cursor.fetchall()
        if account: # if there is data in here
            for i in range(0, len(account)):
                msg = si.get_live_price(account[i]['symbol_Of_Stock'])
                msg = format(msg, ".2f")
                account[i]['sellSharePrice'] = msg
                sellOrNot = float(account[i]['numberOfShareAtBuying']) - float(account[i]['numberOfShareSold'])
                account[i]['Gain'] = format((sellOrNot * float(msg) - sellOrNot * float(account[i]['priceOfShareAtBuying'])), ".2f")
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
        cursor.execute('SELECT * FROM transactions_Table WHERE transactions_ID = %s',
                       (post_id,))
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
        stockid, values, labels, legend, msg, company_name = getGraph(stockID)
        return render_template('Sell_stock.html', stockid=stockid, values=values, labels=labels,
                               legend=legend, price=msg, number=number, profitOrLoss=profitOrLoss,
                               company_name=company_name)
    account, len2, msg, totalGain = getTable()
    return render_template('Portfolio_page.html', account=account, len=len2, msg=msg,
                           totalGain=totalGain)

# getting the graph
def getGraph(nameOfStock):
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    stockData = yf.Ticker(nameOfStock)
    history = stockData.history(period="1d", interval="1m")
    time = list()
    priceOfStock = si.get_live_price(nameOfStock)
    priceOfStock = format(priceOfStock, ".2f")
    for row in history.index:
        if (row.hour > 12):
            date = "{}:{}".format(row.hour - 12, row.minute)
        else:
            date = "{}:{}".format(row.hour, row.minute)
        time.append(date)
    company_name = stockData.info['longName']
    stockid = company_name
    values = history['Open']
    labels = time
    legend = legend
    msg = priceOfStock
    company_name = company_name
    return stockid, values, labels, legend, msg, company_name

# getting the Table
def getTable():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transactions_Table WHERE trading_ID = %s',
                   (session['id'],))
    account = cursor.fetchall()
    if account:
        for i in range(0, len(account)):
            msg = si.get_live_price(account[i]['symbol_Of_Stock'])
            msg = format(msg, ".2f")
            account[i]['sellSharePrice'] = msg
            account[i]['Gain'] = format((float(account[i]['numberOfShareAtBuying']) * float(msg) -
                                         float(account[i]['numberOfShareAtBuying']) * float(
                        account[i]['priceOfShareAtBuying'])), ".2f")
            totalGain = totalGain + float(account[i]['Gain'])
        totalGain = format(totalGain, ".2f")
        msg = account
    return account, len(account), msg, totalGain