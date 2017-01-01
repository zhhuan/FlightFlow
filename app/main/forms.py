from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError


class omniSearch(FlaskForm):
    searchText = StringField(validators=[DataRequired()])
    submit = SubmitField('查询')

class routeSearch(FlaskForm):
    departure = StringField(validators=[DataRequired()])
    arrival = StringField(validators=[DataRequired()])
    submit = SubmitField('查询')

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login in')
