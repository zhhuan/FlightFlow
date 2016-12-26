# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,session,url_for,redirect,flash
from flask.ext.wtf import Form
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import Required,Length
from urllib.request import urlopen
from bs4 import BeautifulSoup
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString

class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return HTMLString('<button %s>' % self.html_params(name=field.name, **kwargs))


class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

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

@app.route('/',methods=['GET','POST'])
def index():
    omniform = omniSearch()
    routeform = routeSearch()
    
    if omniform.validate_on_submit():
        session['searchText'] = omniform.searchText.data
        searchFlight = session.get('searchText')
        html = urlopen("http://flight.qunar.com/status/fquery.jsp?flightCode=" + searchFlight)
        soup = BeautifulSoup(html)
        details = soup.find('dl', {'class': 'state_detail'}).findAll('span')
        flight_general = {
            'Name': soup.find('dl',{'class','state_detail'}).find('dt').get_text(),
            'Duration': details[5].get_text().strip()[5:],
            'Aircraft': details[4].get_text().strip()[3:],
            'Status': details[2].get_text().strip()[5:],
            'Food': details[7].get_text().strip()[3:]
        }
        flight_departure = {
            'Airport': details[1].get_text().strip()[5:9],
            'Time': details[6].get_text().strip()[16:],
            'ScheduledTime': details[6].get_text().strip()[5:16]
        }
        flight_arrive = {
            'Airport': details[1].get_text().strip()[11:],
            'Time': details[9].get_text().strip()[16:],
            'ScheduledTime': details[9].get_text().strip()[5:16]
        }

        return render_template('flight.html',general = flight_general,departure = flight_departure ,arrive = flight_arrive \
                               ,omniform=omniform, routeform=routeform,name=session.get('username'))

    if routeform.validate_on_submit():
        session['departure_city'] = routeform.departure.data
        session['arrive_city'] = routeform.arrival.data
        departure_city = session.get('departure_city')
        arrive_city = session.get('arrive_city')
        print(departure_city)
        html = urlopen("http://flight.qunar.com/schedule/fsearch_list.jsp?departure="+departure_city+\
                       "&arrival="+arrive_city)
        soup = BeautifulSoup(html)
        results = soup.find('div',{'class':'result_content'}).findAll('li')
        search_results = []
        for result in results:
            one = {}
            one['title'] = result.find('span',{'class':'title'}).get_text()
            one['time'] = result.find('span',{'class':'c2'}).get_text()
            one['airport'] = result.find('span',{'class':'c3'}).get_text()
            one['punctuality'] = result.find('span',{'class':'c4'}).get_text()
            print(one['punctuality'])
            search_results.append(one)
        return render_template('route.html',search_results = search_results, \
            omniform=omniform, routeform=routeform,name=session.get('username'))


    return render_template('flightflow.html',omniform = omniform,routeform = routeform,\
                           name=session.get('username'))



@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        old_name = session.get('username')
        if old_name is not None and old_name != form.username.data:
            flash('Looks like you have changed your name!')
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('index'))
    return render_template('login.html',form = form)



if __name__ == "__main__":
    app.run(debug=True)