import datetime
import re
import MySQLdb.cursors
from flask_mail import Mail, Message
from flask import Flask, flash
from flask import render_template, request, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user

login_manager = LoginManager()
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
        if account:
            currentUser = username
            session['loggedin'] = True
            session['id'] = account['trading_ID']
            session['username'] = account['username']
            session['email'] = account['email']

            return render_template('Home_page.html', msg=account)
        else:
            msg = 'Incorrect username / password!'
    return render_template('Login_page.html', msg=msg)


def Updating():
    # if request.method == "POST":
    if request.method == 'POST':
        # if request.form['Save_Button'] == 'Save':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE trading_Profile SET email = %s WHERE username = %s", ('Oumar', 'Oumar',))
        return render_template('Home_page.html', )


from forms import EditProfileForm


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if 'loggedin' in session:
        if form.validate_on_submit():
            session['username'] = form.username.data
            session['username'] = form.about_me.data
            flash('Your changes have been saved.')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE trading_Profile SET email = %s WHERE username = %s", ('Oumar', 'Oumar',))
            cursor2.execute('SELECT * FROM trading_Profile WHERE username = % s',
                           (form.username.data,))
            account = cursor2.fetchone()
            return render_template('Home_page.html',msg =account)
        elif request.method == 'GET':
            form.username.data = session['username']
            form.about_me.data = session['email']
        return render_template('Profile.html', title='Edit Profile', form=form)


# def Updating():
#     if request.method == 'POST':
#         if request.form['Save_Button'] == 'Save':
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute("UPDATE trading_Profile SET email = %s WHERE username = %s", ('Oumar', 'Oumar',))
#             return render_template('Home_page.html', )
#     else:
#         pass
#         return render_template('Home_page.html', )


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


@app.route('/ForgetPassword', methods=['GET', 'POST'])
def forgetPassword_page():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trading_Profile WHERE email = % s', (email,))
        account = cursor.fetchone()
        msg = Message(
            'Hello',
            sender=email,
            recipients=[email]
        )
        msg.html = render_template('msg.html', result=account)
        mail.send(msg)
    return render_template('ForgetPassword_page.html')


@app.route('/Home', methods=['GET', 'POST'])
def home_page():
    if request.form['Save_Button'] == 'Save':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE trading_Profile SET email = %s WHERE username = %s", ('Oumar', 'Oumar',))
        return render_template('Home_page.html', )
        # return render_template('Home_page.html')


@app.route('/StockMarket')
def stock_page():
    return render_template('StockMarket_page.html', )


@app.route('/ChangePassword')
def changePassword_page():
    return render_template('ChangePassword.html', )


@app.route('/Update', methods=['POST'])
def Update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM trading_Profile WHERE username = %s", ('Oumar',))
    data = cursor.fetchone()
    return render_template('Home_page.html', msg=data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        return '<h1>Form submitted!</h1>'
    else:
        #         msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['your reciepients gmail id'])
        #         msg.body = """
        #     	from: %s &lt;%s&gt
        # 		%s
        # 		""" % (form.name.data, form.email.data, form.message.data)
        #         mail.send(msg)
        #         return render_template('Home_page.html')
        return '<h1>Form submitted!</h1>'


@app.route('/ProfilePage')
def pro_page():
    return render_template('Profile.html', )


@app.route('/Updating', methods=['GET', 'POST'])
def Updating():
    # if request.method == "POST":
    if request.method == 'POST':
        if request.form['Save_Button'] == 'Save':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE trading_Profile SET email = %s WHERE username = %s", ('Oumar', 'Oumar',))
            return render_template('Home_page.html', )
    else:
        pass
        return render_template('Home_page.html', )
    # else:
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute("SELECT * FROM trading_Profile WHERE username = %s", ('Oumar',))
    #     data = cursor.fetchone()
    #     return render_template('Home_page.html',result=data)


if __name__ == '__main__':
    app.run(debug=True)
