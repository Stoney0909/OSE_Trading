from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import MySQLdb
import app
from flask import request, session, render_template
from app import mysql
from flask import Blueprint
from FunctionToCall.StockUserAccount import getGraph

Buy_Sell_api = Blueprint('Buy_Sell_api', __name__)
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")


@Buy_Sell_api.route('/buyStock', methods=['GET', 'POST'])
def buy_Stock():
    msg = ''
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    stockData = yf.Ticker(session['IdOfSearch'])
    history = stockData.history(period="1d", interval="1m")
    time = list()
    priceOfStock = format(si.get_live_price(session['IdOfSearch']), ".2f")
    for row in history.index:
        if (row.hour > 12):
            date = "{}:{}".format(row.hour - 12, row.minute)
        else:
            date = "{}:{}".format(row.hour, row.minute)
        time.append(date)
    company_name = stockData.info['longName']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT amount_Money FROM trading_Profile WHERE trading_ID = %s',
                   (session['id'],))
    account = cursor.fetchone()
    moneyAvalaible = account['amount_Money']
    if request.method == 'GET':
        return render_template('buying_stock.html', stockid=company_name, values=history['Open'],
                               labels=time, legend=legend, msg=priceOfStock, company_name=company_name)
    elif request.method == 'POST' and 'stockPrice' in request.form:
        numberOfShare = request.form.get('stockPrice', type=int)
        symbol = session['IdOfSearch']
        if numberOfShare < 1:
            msg = 'The number of share has to be positive!'
        elif float(moneyAvalaible) < numberOfShare * float(priceOfStock):
            msg = "You don't have enough fund to buy this stock"
            return render_template('successfullyBoughtStock.html', stockid=company_name, values=history['Open'],
                                   labels=time, legend=legend, msg=msg, company_name=company_name)

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO transactions_Table VALUES (NULL, %s, %s,% s,% s,% s,% s,% s,% s,%s,%s)',
                           (priceOfStock, numberOfShare, 'Null', 'Null', 'Null', today, 'Null',
                            session['id'], company_name, symbol))

            SpendMoney = float(numberOfShare) * float(priceOfStock)
            amountOfMoneyAfterSpend = float(moneyAvalaible) - float(SpendMoney)
            Description = 'Spend $'+ str(round(float(SpendMoney), 2)) + ' to buy ' + str(round(float(numberOfShare), 2)) + ' share of ' + company_name + '\'s stock'

            cursor.execute('INSERT INTO transaction_History VALUES (NULL,%s,%s,%s,%s,%s)',
                           (session['id'], today, Description, float(SpendMoney), float(amountOfMoneyAfterSpend)))

            cursor.execute('UPDATE trading_Profile SET amount_Money = %s '
                           'WHERE trading_ID = %s',
                           (float(moneyAvalaible) - (numberOfShare * float(priceOfStock)), session['id'],))
            mysql.connection.commit()
            msg = 'You successfully bought the stock'
            return render_template('successfullyBoughtStock.html', stockid=company_name, values=history['Open'],
                                   labels=time, legend=legend, msg=msg, company_name=company_name)

    return render_template('buying_stock.html', stockid=company_name, values=history['Open'],
                           labels=time, legend=legend, msg=msg, company_name=company_name)



@Buy_Sell_api.route('/SellStock', methods=['GET', 'POST'])
def sellStock_Page():
    error = None
    if request.method == 'POST':
        shareToSold = request.form['shareToSold']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM transactions_Table WHERE transactions_ID = %s',
                       (session['Transaction_ID'],))
        account = cursor.fetchall()
        currentPrice = 0.0
        number, shareYouOwn, profitOrLoss, stockID = gotToPortfolio()
        stockid, values, labels, legend, msg, company_name = getGraph(stockID)
        if account:
            for i in range(0, len(account)):
                currentPrice = si.get_live_price(account[i]['symbol_Of_Stock'])
            if int(shareToSold) > int(number):
                error = "You Don't Own That amount of share"
                return render_template('Sell_stock.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, price=msg, number=number, profitOrLoss=profitOrLoss,
                                       company_name=company_name, error=error)
            elif float(shareToSold) < 1:
                error = "Please input positive number"
                return render_template('Sell_stock.html', stockid=stockid, values=values, labels=labels,
                                       legend=legend, price=msg, number=number, profitOrLoss=profitOrLoss,
                                       company_name=company_name, error=error)
            else:
                cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                cursor2.execute('UPDATE transactions_Table SET numberOfShareSold = numberOfShareSold + %s, sellSharePrice = %s '
                                ', sellShare = %s WHERE transactions_ID = %s',
                                (shareToSold, format(currentPrice, ".2f"), today, session['Transaction_ID'],))

                # Description = 'Sold ' + shareToSold + ' share of ' + company_name + '\'s stock'
                # GetMoney = float(currentPrice * shareToSold)
                # Money = app.getMoney() - GetMoney
                # cursor2.execute('INSERT INTO transaction_History VALUES (NULL,%s,%s,%s,%s,%s)',
                #                 (session['id'], today, Description, float(GetMoney), float(Money)))
                # having crisis

                cursor2.execute('UPDATE trading_Profile SET amount_Money = amount_Money + %s '
                                'WHERE trading_ID = %s',
                                ((int(shareToSold) * currentPrice), session['id'],))
                cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor3.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
                data = cursor3.fetchall()
                mysql.connection.commit()
                Money = app.getMoney()
                return render_template('Home_page.html', len=len(data), data=data, Money = Money)


def gotToPortfolio():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transactions_Table WHERE transactions_ID = %s',
                   (session['Transaction_ID'],))
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
            shareBought = account[i]['numberOfShareAtBuying']
    return number, shareBought, profitOrLoss, stockID
