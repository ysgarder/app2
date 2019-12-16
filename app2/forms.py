from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app2.models import User


class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    twofa = StringField('2FA', id='2fa', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    result = StringField('Login Result')
    submit = SubmitField('Sign In')


class RegForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    pword2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('pword')])
    twofa = StringField('2FA?', id='2fa')
    success = StringField('Registration Status', id='success')
    submit = SubmitField('Sign In')

    def validate_username(self, uname):
        user = User.query.filter_by(username=uname.data).first()
        if user is not None:
            raise ValidationError('Please use a different username. ')


class SpellCheckForm(FlaskForm):
    inputtext = StringField('Input_Text', validators=[DataRequired()])
    textout = StringField('Check Results')
    misspelled = StringField('Missspelled Words')
    submittext = SubmitField('Submit text')
