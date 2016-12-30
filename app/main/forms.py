from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, PasswordField,SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError


class omniSearch(Form):
    searchText = StringField(validators=[Required()])
    submit = SubmitField('查询')

class routeSearch(Form):
    departure = StringField(validators=[Required()])
    arrival = StringField(validators=[Required()])
    submit = SubmitField('查询')

class LoginForm(Form):
    username = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField('Login in')
