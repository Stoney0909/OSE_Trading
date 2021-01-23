import datetime
import MySQLdb.cursors
from flask_mail import Mail, Message
from flask import Flask
from flask import render_template, request, session
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
app.config['MYSQL_HOST'] = 'ose-trading.ck8xkz5g94jg.us-east-2.rds.amazonaws.com'
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

# Calling the function for Sign up , edit Profile and ChangePassword
from FunctionToCall.Account import account_api

app.register_blueprint(account_api, url_prefix='/Signup')

app.register_blueprint(account_api, url_prefix='/edit_profile')

app.register_blueprint(account_api, url_prefix='/ChangePassword')

app.register_blueprint(account_api, url_prefix='/ForgetPassword')

# Calling the function for StockMarketPage and Portfolio
from FunctionToCall.StockUserAccount import stock_Account_api
app.register_blueprint(stock_Account_api, url_prefix='/StockMarket')

app.register_blueprint(stock_Account_api, url_prefix='/Portfolio')

# Calling the function for buy and Sell stock
from FunctionToCall.Buy_Sell import Buy_Sell_api
app.register_blueprint(Buy_Sell_api, url_prefix='/buyStock')

app.register_blueprint(Buy_Sell_api)


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


@app.route('/Home', methods=['GET', 'POST'])
def home_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
    data = cursor.fetchall()  # data from database

    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT amount_Money FROM trading_Profile where username = %s', (session['username'],))
    Money = cursor2.fetchall()
    # return render_template("example.html", value=data)
    return render_template('Home_page.html', len=len(data), data=data, Money=Money)


@app.route('/SuccessFullBought')
def successBought():
    return render_template('successfullyBoughtStock.html')


@app.route('/TransactionHistory', methods=['GET', 'POST'])
def transaction_history():

    return render_template('TransactionHistory.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form \
            and 'email' in request.form and 'feedback' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        feedback = request.form['feedback']
        email = request.form['email']
        msg = Message("Feedback", sender=email, recipients=['oumarcisseju@gmail.com'])
        msg.body = "You have received a new feedback from {} <{}>. Comment {}.".format(lastname, email, feedback)
        mail.send(msg)
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
        data = cursor2.fetchall()
        return render_template('Home_page.html', len=len(data), data=data)

    else:
        return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
