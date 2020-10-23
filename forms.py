import MySQLdb
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError, Email
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

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_username(form, username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM trading_Profile WHERE trading_ID != %s AND username = %s',
                       (session['id'], username.data))
        account = cursor.fetchone()
        if account:
            raise ValidationError(account)
