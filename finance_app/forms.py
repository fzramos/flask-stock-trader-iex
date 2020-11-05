from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange

class UserInfoForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()

class QuoteForm(FlaskForm):
    symbol = StringField('Stock Symbol', validators = [DataRequired()])
    submit = SubmitField('Quote')

class BuyForm(FlaskForm):
    symbol = StringField('Stock Symbol', validators = [DataRequired()])
    shares = IntegerField('Shares', validators = [NumberRange(min=0, max=1000)])
    submit = SubmitField('Buy')
