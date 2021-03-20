import datetime
import MySQLdb.cursors
from babel import Locale
from flask_mail import Mail, Message
from flask import Flask, jsonify
from flask import render_template, request, session
from flask_mysqldb import MySQL
from flask_babel import _, refresh, Babel
from flask import g, request
from babel.dates import format_datetime, format_date
from babel.numbers import format_currency
from forex_python.converter import CurrencyRates

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
app.config['MYSQL_HOST'] = 'ose.ck8xkz5g94jg.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'OSE_Trading'

babel = Babel(app)


# add to you main app code
@babel.localeselector
def get_locale():
    return 'zh'
    # request.accept_languages.best_match(app.config['LANGUAGES'].keys())


mysql = MySQL(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='oumarcissevu@gmail.com',
    MAIL_PASSWORD='Ousmane1998@',
    LANGUAGES={
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'zh': 'Chinese'
    }
)

mail = Mail(app)

currentUser = ''
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")
c = CurrencyRates()
exchangeToEuros = c.get_rate('USD', 'EUR')
exchangeToPesos = c.get_rate('USD', 'MXN')
exchangeToYen = c.get_rate('USD', 'CNY')
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
            cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor3.execute('SELECT * FROM trading_Profile where username = %s', (account['username'],))
            Money = cursor3.fetchall()
            return render_template('Home_page.html', len=len(data), data=data, Money=Money)
        else:
            msg = _('Incorrect username / password!')
    return render_template('Login_page.html', msg=msg)


@app.route('/Home', methods=['GET', 'POST'])
def home_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM trading_Profile ORDER BY  amount_Money desc')
    data = cursor.fetchall()  # data from database

    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT * FROM trading_Profile where username = %s', (session['username'],))
    Money = cursor2.fetchall()
    # return render_template("example.html", value=data)
    return render_template('Home_page.html', len=len(data), data=data, Money=Money)


@app.route('/SuccessFullBought')
def successBought():
    return render_template('successfullyBoughtStock.html')


@app.route('/TransactionHistory', methods=['GET', 'POST'])
def transaction_history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transaction_History WHERE trading_ID = %s', (session['id'],))
    account = cursor.fetchall()
    return render_template('TransactionHistory.html', len=len(account), Account=account)


@app.route('/loan', methods=['GET', 'POST'])
def Loan():
    # Grabing data
    Confirm_Msg = ''
    UserID = 0
    if request.method == 'POST' and 'Loan_Amount' in request.form:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT trading_ID FROM trading_Profile where username = %s', (session['username'],))
        User = cursor.fetchone()
        UserID = int(User['trading_ID'])

        Amount_OF_Loan = float(request.form['Loan_Amount'])  # this is getting the input for Amount of loan
        Pay_Back_round = 5.0
        Interest_Rate = 0.05
        Pay_Back_Money_Per_Time = round(float(Amount_OF_Loan) / Pay_Back_round,
                                        2)  # How much money user have to pay back per period
        Interest_Amount = float(Amount_OF_Loan) * Interest_Rate
        Total_Pay_Back = round(float(Interest_Rate) * float(Amount_OF_Loan), 2) + Pay_Back_Money_Per_Time
        Loan_Date = today
        Pay_BackDay_Period = 7  # user have to pay amount of money back in 7 day
        Pay_Back_Day = today + str(datetime.timedelta(days=Pay_BackDay_Period))
        # if Pay_Back_Day == today:
        #     Pay_Back_Day = today + datetime.timedelta(days= Pay_BackDay_Period)

        cursor.execute('INSERT INTO Loan VALUES (NULL, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s)',
                       (UserID, Amount_OF_Loan, Interest_Amount, Total_Pay_Back, Interest_Rate, Pay_Back_round,
                        Pay_BackDay_Period, Loan_Date, Pay_Back_Day, Amount_OF_Loan, 1))
        cursor.fetchall()

        Confirm_Msg = 'You had loan $' + str(Amount_OF_Loan) + \
                      ', in next 7 days, you have to pay back $' \
                      + str(Total_Pay_Back) + ' include interest'
        mysql.connection.commit()
        return render_template('loan.html', Amount_OF_Loan=Amount_OF_Loan, Confirm_Msg=Confirm_Msg)
    return render_template('loan.html', Confirm_Msg=Confirm_Msg)


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
        Money = getMoney()
        return render_template('Home_page.html', len=len(data), data=data, Money=Money)

    else:
        return render_template('contact.html')


def getMoney():
    cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor3.execute('SELECT * FROM trading_Profile where username = %s', (session['username'],))
    Money = cursor3.fetchall()
    return Money


@app.template_filter()  # Convert the number to local variable
def ConvertNumberToEuros(number):
    if get_locale() == 'fr':  # convert to euros
        return format_currency(float(number) * exchangeToEuros, 'EUR', locale='fr_FR')
    if get_locale() == 'es':  # convert to spanish
        return format_currency(float(number) * exchangeToPesos, 'MXN', locale='es_MX')
    if get_locale() == 'zh':  # convert to chinese
        return format_currency(float(number) * exchangeToYen, 'CNY', locale='zh_CN')
    else:
        return format_currency(float(number), 'USD', locale='en_US')


@app.template_filter()
def getAppropriate_Date(date):
    if get_locale() == 'fr':
        return datetime.datetime.strftime(date, '%d-%m-%Y')
    if get_locale() == 'es':
        return datetime.datetime.strftime(date, '%d-%m-%Y')
    if get_locale() == 'zh':
        return datetime.datetime.strftime(date, '%Y-%m-%d')
    else:
        return datetime.datetime.strftime(date, '%Y-%m-%d')


if __name__ == '__main__':
    app.run(debug=True)
