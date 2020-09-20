from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'osetrading.ck8xkz5g94jg.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'OSE_Trading'

mysql = MySQL(app)

currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")

@app.route('/',methods =['GET', 'POST'])
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
            return render_template('Home_page.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('Login_page.html', msg=msg)



@app.route('/Signup', methods=['GET', 'POST'])
def signup_page():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO trading_Profile VALUES (NULL, % s, % s,% s,% s,% s,% s,% s)', ('Null','Null', username, email, password,'150',today))
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


if __name__ == '__main__':
    app.run(debug=True)
