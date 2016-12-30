from datetime import datetime
from flask import render_template,session, redirect, url_for,current_app
from urllib.request import urlopen
from bs4 import BeautifulSoup

from . import main
from .forms import omniSearch,routeSearch,LoginForm
from .. import db
from ..models import User
from ..email import *
import logging


@main.route('/', methods=['GET', 'POST'])
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
            'Name': soup.find('dl', {'class', 'state_detail'}).find('dt').get_text(),
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

        return render_template('flight.html', general=flight_general, departure=flight_departure, arrive=flight_arrive \
                               , omniform=omniform, routeform=routeform, name=session.get('username'))

    if routeform.validate_on_submit():
        session['departure_city'] = routeform.departure.data
        session['arrive_city'] = routeform.arrival.data
        departure_city = session.get('departure_city')
        arrive_city = session.get('arrive_city')
        print(departure_city)
        html = urlopen("http://flight.qunar.com/schedule/fsearch_list.jsp?departure=" + departure_city + \
                       "&arrival=" + arrive_city)
        soup = BeautifulSoup(html)
        results = soup.find('div', {'class': 'result_content'}).findAll('li')
        search_results = []
        for result in results:
            one = {}
            one['title'] = result.find('span', {'class': 'title'}).get_text()
            one['time'] = result.find('span', {'class': 'c2'}).get_text()
            one['airport'] = result.find('span', {'class': 'c3'}).get_text()
            one['punctuality'] = result.find('span', {'class': 'c4'}).get_text()
            print(one['punctuality'])
            search_results.append(one)
        return render_template('route.html', search_results=search_results, \
                               omniform=omniform, routeform=routeform, name=session.get('username'))

    return render_template('flightflow.html', omniform=omniform, routeform=routeform, \
                           name=session.get('username'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                user = User(username=form.username.data, password=form.password.data)
                db.session.add(user)
                session['known'] = False
                if current_app.config['FLASKY_ANDMIN']:
                    send_email(current_app.config['FLASKY_ANDMIN'], 'NEW User', \
                               'mail/new_user', user=user)
                    form.username.data = ''
                    form.password.data = ''
                    return redirect(url_for('.login'))
            else:
                session['known'] = True
            session['username'] = form.username.data
            session['password'] = form.password.data
            form.username.data = ''
            form.password.data = ''
            return redirect(url_for('.index'))
        return render_template('login.html', form=form, name=session.get('username'), \
                               known=session.get('known', False))
    except Exception as e:
        logging.exception(e)


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/flow')
def flow():
    return render_template('flow.html')

