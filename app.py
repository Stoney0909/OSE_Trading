import datetime
import MySQLdb.cursors
import time
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


@babel.localeselector
def get_locale():
    return 'es'
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


@app.route('/PayBackLoanPage', methods=['GET', 'POST'])
def PayBack():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Amount_Of_Money_PayBack_Left FROM Loan where UserID = %s', (session['id'],))
    Amount_Of_Money_need_to_PayBack_Left = cursor.fetchone()['Amount_Of_Money_PayBack_Left']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT payBackDayBy FROM Loan where UserID = %s', (session['id'],))
    PaybackDay = cursor.fetchone()['payBackDayBy']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT amount_Money FROM trading_Profile where trading_ID = %s', (session['id'],))
    AccountMoney = cursor.fetchone()['amount_Money']

    if request.method == 'POST' and 'Pay_Back_Loan_Money' in request.form:

        PlayBackMoney = float(request.form['Pay_Back_Loan_Money'])

        if PlayBackMoney < 1:
            msg = _('Please enter a positive number')
        elif PlayBackMoney > Amount_Of_Money_need_to_PayBack_Left:
            msg = _('You only have to play back ') + str(Amount_Of_Money_need_to_PayBack_Left)
        elif PlayBackMoney > AccountMoney:
            msg = _('You don\'t have that much money in your account')
        else:
            AccountMoney -= PlayBackMoney
            Amount_Of_Money_need_to_PayBack_Left -= PlayBackMoney
            if Amount_Of_Money_need_to_PayBack_Left == 0:
                msg = _('You have paid off all the loans')
                # time.sleep(3)

            else:
                msg = _('You still need to pay back ') + str(Amount_Of_Money_need_to_PayBack_Left) + _(" by ") + str(
                    PaybackDay)

        cursor.execute('UPDATE trading_Profile SET amount_Money = %s WHERE trading_ID = %s',
                       (AccountMoney, session['id'],))
        cursor.fetchall()

        cursor.execute('DELETE FROM Loan WHERE UserID = %s',
                       (session['id'],))
        cursor.fetchall()

        mysql.connection.commit()

        return render_template('PayBackLoanPage.html',
                               Amount_Of_Money_need_to_PayBack_Left=Amount_Of_Money_need_to_PayBack_Left,
                               PaybackDay=PaybackDay,
                               AccountMoney=AccountMoney,
                               msg=msg)

    return render_template('PayBackLoanPage.html',
                           Amount_Of_Money_need_to_PayBack_Left=Amount_Of_Money_need_to_PayBack_Left,
                           PaybackDay=PaybackDay,
                           AccountMoney=AccountMoney)


@app.route('/loan', methods=['GET', 'POST'])
def Loan():
    # Grabing data
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Confirm_Msg = ''
    UserID = 0
    Pay_BackDay_Period = 0
    checkLoansucess = True
    checkUserHasLoan = False

    cursor.execute('SELECT trading_ID FROM trading_Profile where username = %s', (session['username'],))
    User = cursor.fetchone()
    UserID = int(User['trading_ID'])

    cursor.execute('SELECT * FROM Loan WHERE UserID = % s', (UserID,))
    CheckHasloan = cursor.fetchone()

    if not CheckHasloan == None:
        cursor.execute('SELECT Amount_Of_Money_PayBack_Left FROM Loan Where UserID = % s', (UserID,))
        AmountOfMoneyLeft = cursor.fetchone()['Amount_Of_Money_PayBack_Left']
        if AmountOfMoneyLeft != 0:
            checkUserHasLoan = True
            return PayBack()
    else:
        if request.method == 'POST' and 'Loan_Amount' in request.form:

            Amount_OF_Loan = float(request.form['Loan_Amount'])
            if get_locale != "en":
                Amount_OF_Loan = checkingNumber(Amount_OF_Loan)
            Amount_OF_Loan = Amount_OF_Loan[:-2].split(',')
            Amount_OF_Loan = float('.'.join([Amount_OF_Loan[0].replace('.', ''), Amount_OF_Loan[1]]))

            Interest_Rate = 0.05
            Pay_Back_Money_Per_Time = round(float(Amount_OF_Loan), 2)  # How much money user have to pay back
            Interest_Amount = float(Amount_OF_Loan) * Interest_Rate
            Total_Pay_Back = round(Interest_Amount, 2) + Pay_Back_Money_Per_Time
            Loan_Date = today

            # Check how many days user have to pay back the loan based on the price
            if Amount_OF_Loan > 1000000 or Amount_OF_Loan < 1000:
                checkLoansucess = False
            elif 800000 <= Amount_OF_Loan <= 1000000:
                Pay_BackDay_Period = 730
            elif 650000 <= Amount_OF_Loan <= 800000:
                Pay_BackDay_Period = 600
            elif 500000 < Amount_OF_Loan <= 650000:
                Pay_BackDay_Period = 500
            elif 300000 < Amount_OF_Loan <= 500000:
                Pay_BackDay_Period = 400
            elif 100000 < Amount_OF_Loan <= 300000:
                Pay_BackDay_Period = 365
            elif 50000 < Amount_OF_Loan <= 100000:
                Pay_BackDay_Period = 300
            elif 10000 < Amount_OF_Loan <= 50000:
                Pay_BackDay_Period = 180
            elif 5000 < Amount_OF_Loan <= 10000:
                Pay_BackDay_Period = 90
            elif 1000 <= Amount_OF_Loan <= 5000:
                Pay_BackDay_Period = 60

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT amount_Money FROM trading_Profile WHERE trading_ID = %s',
                           (session['id'],))
            account = cursor.fetchone()
            moneyAvalaible = account['amount_Money']

            Pay_Back_Day = datetime.datetime.now() + datetime.timedelta(days=Pay_BackDay_Period)

            if checkLoansucess:
                cursor.execute('INSERT INTO Loan VALUES (NULL, %s,%s,%s,%s,%s, %s, %s, %s, %s)',
                               (UserID, Amount_OF_Loan, Interest_Amount, Total_Pay_Back, Interest_Rate,
                                Pay_BackDay_Period, Loan_Date, Pay_Back_Day, Total_Pay_Back))
                cursor.fetchall()

                NewAmountOfMoney = moneyAvalaible + Amount_OF_Loan
                cursor.execute('UPDATE trading_Profile SET amount_Money = %s WHERE trading_ID = %s',
                               (NewAmountOfMoney, session['id'],))
                cursor.fetchall()

                Confirm_Msg = _('You had loan $') + str(ConvertNumberToEuros(Amount_OF_Loan)) + \
                              _(', in next ') + str(Pay_BackDay_Period) + _(' days, you have to pay back $') \
                              + str(ConvertNumberToEuros(Total_Pay_Back)) + _(' include interest')
                mysql.connection.commit()
            else:
                Confirm_Msg = _('Amount of loan range is 1000 - 1000000')

            return render_template('loan.html', Amount_OF_Loan=Amount_OF_Loan, Confirm_Msg=Confirm_Msg,
                                   checkUserHasLoan=checkUserHasLoan)
        return render_template('loan.html', Confirm_Msg=Confirm_Msg, checkUserHasLoan=checkUserHasLoan)


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
        msg.body = _("You have received a new feedback from {} <{}>. Comment {}.").format(lastname, email, feedback)
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


def checkingNumber(number):
    number = number[:-2].split(',')
    number = float('.'.join([number[0].replace('.', ''), number[1]]))
    return 12


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
