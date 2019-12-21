from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app2.models import User, SpellQueries


class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    twofa = StringField('2FA', id='2fa', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    result = StringField('Login Result', id='result')
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

class HistoryForm(FlaskForm):
    num_queries = IntegerField('Total Queries', id='numqueries')
    user_query = StringField('Find User Queries', id='userquery', validators=[DataRequired])
    submit_query = SubmitField('Search User History')
    history = FieldList('Results',id='query' )

    def gethistory(self):
        user = User.query.filter_by(username=self.user_query).first()

        return SpellQueries.query.filter_by(user_id=User.id)
