from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime
from Python import get_graph_html as graph

import yfinance as yf
from pandas_datareader import data

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'database.ck8xkz5g94jg.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'OSE_Trading'

mysql = MySQL(app)
currentUser = ''
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")


@app.route('/', methods=['GET', 'POST'])
def login_page():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            # Don't erase it, still figure it out
            # session['loggedin'] = True
            # session['trading_id'] = account['trading_id']
            # session['username'] = account['userName']
            currentUser = username
            return render_template('Home_page.html', msg=currentUser)
        else:
            msg = 'Incorrect username / password!'
    return render_template('Login_page.html', msg=msg)


@app.route('/Signup', methods=['GET', 'POST'])
def signup_page():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'password1' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password1 = request.form['password1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        elif not password == password1:
            msg = 'Password does not match'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO trading_Profile VALUES (NULL, % s, % s,% s,% s,% s,% s,% s)',
                           ('Null', 'Null', username, email, password, '150', today))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('Signup_page.html', msg=msg)


@app.route('/ForgetPassword')
def forgetPassword_page():
    return render_template('ForgetPassword_page.html')


@app.route('/Home')
def home_page():
    return render_template('Home_page.html')


@app.route('/StockMarket', methods=['GET', 'POST'])
def stock_page():
    stockid = 'MSFT'
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    if request.method == 'POST' and 'stockID' in request.form:
        stockid = request.form['stockID']

        stockData = yf.Ticker(stockid)
        history = stockData.history(period="1d", interval="1m")
        time = list()
        for row in history.index:
            date = datetime.datetime.timestamp(row)
            time.append(date)
        return render_template('StockMarket_page.html', stockid=history, values=history['Open'],
                               labels=time, legend=legend)

    values = [20, 21, 263, 10, 10, 10, 10, 10]
    return render_template('StockMarket_page.html', stockid=stockid, values=values, labels=labels, legend=legend)


@app.route('/Home', methods=['GET', 'POST'])
def someName():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # sql = "SELECT * FROM trading_Profile WHERE username = % s",(currentUser,)
    cursor.execute("SELECT * FROM trading_Profile WHERE username = % s", (currentUser,))
    results = cursor.fetchall()
    return render_template('Home_page.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
