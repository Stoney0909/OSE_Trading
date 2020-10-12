from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@database.ck8xkz5g94jg.us-east-2.rds.amazonaws.com/OSE_Trading'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'flasksqlalchemy'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

# msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'password1' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         password1 = request.form['password1']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM trading_Profile WHERE username = % s', (username,))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'name must contain only characters and numbers !'
#         elif not password == password1:
#             msg = 'Password does not match'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO trading_Profile VALUES (NULL, % s, % s,% s,% s,% s,% s,% s)',
#                            ('Null', 'Null', username, email, password, '150', today))
#             mysql.connection.commit()
#             msg = 'You have successfully registered!'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'