import re
import datetime
import MySQLdb
import mail

from flask import request, session, render_template, flash

from flask import Blueprint
import random
import string


from flask_mail import Mail, Message

from app import mysql
from forms import EditProfileForm

account_api = Blueprint('account_api', __name__)
currentDT = datetime.datetime.now()
today = currentDT.strftime("%Y-%m-%d")


@account_api.route('/Signup', methods=['GET', 'POST'])
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


@account_api.route('/edit_profile', methods=['GET', 'POST'])
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


@account_api.route('/ChangePassword', methods=['GET', 'POST'])
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


@account_api.route('/ForgetPassword', methods=['GET', 'POST'])
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


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
