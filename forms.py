import MySQLdb
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms import ValidationError
import phonenumbers
from app import session, mysql
import re
from wtforms.fields.html5 import EmailField


class ChangePassword(FlaskForm):
    oldPassword = StringField('old_password', validators=[DataRequired()])
    newPassword = StringField('new_password', validators=[DataRequired()])
    newPassword2 = StringField('new_password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_Password(form, newPassword, newPasword2):
        if newPassword != newPasword2:
            raise ValidationError("The New password does not match")

    def validate_Old_Password(form, oldPassword):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT passwrod FROM trading_Profile WHERE trading_ID = %s',
                       (session['id']))
        account = cursor.fetchone()
        if not account:
            raise ValidationError("Your old password does not match")


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
