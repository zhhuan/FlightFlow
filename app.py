# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,session,url_for,redirect
from flask.ext.wtf import Form
from wtforms import SubmitField,StringField
from wtforms.validators import Required
from urllib.request import urlopen
from bs4 import BeautifulSoup



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

class omniSearch(Form):
    searchText = StringField(validators=[Required()])
    submit = SubmitField('查询')

class routeSearch(Form):
    departure = StringField(validators=[Required()])
    arrival = StringField(validators=[Required()])
    submit = SubmitField('查询')

class logform(Form):
    username = StringField(validators=[Required()])
    submit = SubmitField('登陆')

@app.route('/',methods=['GET','POST'])
def index():
    username = None
    omniform = omniSearch()
    routeform = routeSearch()
    form = logform()
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

        return render_template('flight.html',general = flight_general,departure = flight_departure \
                         ,arrive = flight_arrive)

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
        return render_template('route.html',search_results = search_results)

    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('index'))

    return render_template('flightflow.html',omniform = omniform,routeform = routeform,\
                           form = form,name=session.get('username'))


if __name__ == "__main__":
    app.run(debug=True)