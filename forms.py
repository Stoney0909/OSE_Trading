import MySQLdb
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, validators, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError, Email, NumberRange
from wtforms import ValidationError
import phonenumbers
from app import session, mysql
import re
from wtforms.fields.html5 import EmailField


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_Name = StringField('First_Name', validators=[DataRequired()])
    last_Name = StringField('Last_Name', validators=[DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    category = SelectField('Gender', choices=[(1, 'Male'), (2, 'Female')])
    phone = StringField('Phone', validators=[DataRequired(), Length(10)])
    submit = SubmitField('Submit')

    # def validate_phone(self, phone):
    #     try:
    #         p = phonenumbers.parse(phone.data)
    #         if not phonenumbers.is_valid_number(p):
    #             raise ValueError()
    #     except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    #         raise ValidationError('Invalid phone number')


    def validate_username(form, username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM trading_Profile WHERE trading_ID != %s AND username = %s',
                       (session['id'], username.data))
        account = cursor.fetchone()
        if account:
            raise ValidationError(account)


class BuyStock(FlaskForm):
    symbolOfStock = StringField('symbolOfStock', validators=[DataRequired()])
    numberOfShare = IntegerField('numberOfShare', validators=[NumberRange(min=1, max=10000000000)])
    priceOfShare = StringField('priceOfShare', validators=[DataRequired()])
    submit = SubmitField('Buy')
