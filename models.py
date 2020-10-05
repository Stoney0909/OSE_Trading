# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@database.ck8xkz5g94jg.us-east-2.rds.amazonaws.com/OSE_Trading'
# db = SQLAlchemy(app)
#
# class Category(db.Model):
#     __tablename__ = 'trading_Profile'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     slug = db.Column(db.String(255), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#
#     def __repr__(self):
#         return "<{}:{}>".format(id, self.name)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username