import datetime
from Python import get_graph_html as graph

import yfinance as yf
from pandas_datareader import data
import re
import MySQLdb.cursors
from flask_mail import Mail, Message
from flask import Flask, flash, redirect, url_for
from flask import render_template, request, session
from flask_mysqldb import MySQL
from Python import stockPage

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
app.config['MYSQL_HOST'] = 'database.ck8xkz5g94jg.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'OSE_Trading'

mysql = MySQL(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='oumarcissevu@gmail.com',
    MAIL_PASSWORD='Ousmane1998@'
)

mail = Mail(app)

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
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
        data = cursor2.fetchall()
        if account:
            session['loggedin'] = True
            session['id'] = account['trading_ID']
            session['username'] = account['username']
            session['email'] = account['email']
            session['first_name'] = account['first_Name']
            session['last_name'] = account['last_Name']
            session['phone'] = account['phone']
            session['gender'] = account['gender']

            return render_template('Home_page.html', len=len(data), data=data)
        else:
            msg = 'Incorrect username / password!'
    return render_template('Login_page.html', msg=msg)


from forms import EditProfileForm


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if 'loggedin' in session:
        if form.validate_on_submit():
            session['username'] = form.username.data
            session['email'] = form.email.data
            session['first_name'] = form.first_Name.data
            session['last_name'] = form.last_Name.data
            session['phone'] = form.phone.data
            session['gender'] = form.category.data
            flash('Your changes have been saved.')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE trading_Profile SET username = %s , email = %s, first_Name = %s ,last_Name = %s'
                           ', phone = %s, gender = %s'
                           'WHERE trading_ID = %s',
                           (session['username'], session['email'], session['first_name'],
                            session['last_name'], session['phone'], session['gender'],
                            session['id'],))

            cursor.execute('SELECT * FROM trading_Profile WHERE username = %s',
                           (session['id'],))
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
            data = cursor2.fetchall()
            account = cursor.fetchone()
            mysql.connection.commit()
            return render_template('Home_page.html', msg=account, len=len(data), data=data)
        elif request.method == 'GET':
            form.username.data = session['username']
            form.email.data = session['email']
            form.category.data = session['gender']
            if form.first_Name.data == 'Null':
                form.first_Name.data = ''
            else:
                form.first_Name.data = session['first_name']
            if form.last_Name.data == 'Null':
                form.last_Name.data = ''
            else:
                form.last_Name.data = session['last_name']
            if form.phone.data == 'Null':
                form.phone.data = ''
            else:
                form.phone.data = session['phone']
        return render_template('Profile.html', title='Edit Profile', form=form)


@app.route('/ChangePassword', methods=['GET', 'POST'])
def changePassword_page():
    msg = ''
    if request.method == 'POST' and 'oldPassword' in request.form and 'newPassword' in request.form and 'newPassword2' in request.form:
        oldpassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        newPassword2 = request.form['newPassword2']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE trading_ID = %s AND password = %s',
                       (session['id'], oldpassword,))
        account = cursor.fetchone()
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
        data = cursor2.fetchall()
        if account:
            if newPassword2 != newPassword:
                msg = 'New Password does not match'
            else:
                cursor.execute('UPDATE trading_Profile SET password = %s '
                               'WHERE trading_ID = %s',
                               (newPassword, session['id'],))
                mysql.connection.commit()
                return render_template('Home_page.html', msg=msg, len=len(data), data=data)
        else:
            msg = 'Old password does not match'
            render_template('ChangePassword.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('ChangePassword.html', msg=msg)


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
            cursor.execute('INSERT INTO trading_Profile VALUES (NULL, % s, % s,% s,% s,% s,% s,% s,%s,%s)',
                           ('Null', 'Null', username, email, password, '500', today, 'Null', 'Null'))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('Signup_page.html', msg=msg)


@app.route('/ForgetPassword', methods=['GET', 'POST'])
def forgetPassword_page():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account is None:
            msg = 'This account does not exist'
            return render_template('ForgetPassword_page.html', msg=msg)
        else:
            password = get_random_string(8)
            msg = Message(
                'Hello',
                sender=email,
                recipients=[email]
            )
            msg.html = render_template('msg.html', result=account, password=password)
            mail.send(msg)
            cursor.execute('UPDATE trading_Profile SET password = %s '
                           'WHERE email = %s',
                           (password, email,))
            mysql.connection.commit()
            msg = "Check your email for the new password"
            return render_template('ForgetPassword_page.html', msg=msg)

    return render_template('ForgetPassword_page.html')


@app.route('/Home', methods=['GET', 'POST'])
def home_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
    data = cursor.fetchall()  # data from database
    # return render_template("example.html", value=data)
    return render_template('Home_page.html', len=len(data), data=data)


@app.route('/StockMarket', methods=['GET', 'POST'])
def stock_page():
    return stockPage.loadDay()


@app.route('/buyStock', methods=['GET', 'POST'])
def buy_Stock():
    msg = ''
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    stockData = yf.Ticker(session['IdOfSearch'])
    history = stockData.history(period="1d", interval="1m")
    time = list()
    priceOfStock = stockData.info['dayLow']
    for row in history.index:
        date = datetime.datetime.timestamp(row)
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
            cursor.execute('INSERT INTO transactions_Table VALUES (NULL, % s, % s,% s,% s,% s,% s,% s,%s,%s)',
                           (priceOfStock, numberOfShare, 'Null', 'Null', today, 'Null',
                            session['id'], company_name, symbol))
            cursor.execute('UPDATE trading_Profile SET amount_Money = %s '
                           'WHERE trading_ID = %s',
                           (float(moneyAvalaible) - (numberOfShare * float(priceOfStock)), session['id'],))
            mysql.connection.commit()
            msg = 'You successfully bought the stock'
            return render_template('successfullyBoughtStock.html', stockid=company_name, values=history['Open'],
                                   labels=time, legend=legend, msg=msg, company_name=company_name)

    return render_template('buying_stock.html', stockid=company_name, values=history['Open'],
                           labels=time, legend=legend, msg=msg, company_name=company_name)

@app.route('/SellStock')
def sellStock_Page():
    return render_template('Sell_stock.html')

@app.route('/Portfolio')
def portfolio_Page():
    return render_template('Portfolio_page.html')

@app.route('/SuccessFullBought')
def successBought():
    return render_template('successfullyBoughtStock.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form\
            and 'email' in request.form and 'feedback' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        feedback = request.form['feedback']
        email = request.form['email']
        msg = Message("Feedback",sender=email, recipients=['oumarcisseju@gmail.com'])
        msg.body = "You have received a new feedback from {} <{}>. Comment {}.".format(lastname, email,feedback)
        mail.send(msg)
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
        data = cursor2.fetchall()
        return render_template('Home_page.html', len=len(data), data=data)

    else:
        return render_template('contact.html')


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



if __name__ == '__main__':
    app.run(debug=True)


