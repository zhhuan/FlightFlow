# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,session,url_for,redirect,flash
from flask_script import Manager,Shell
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import Required,Length
from urllib.request import urlopen
from bs4 import BeautifulSoup
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString
from threading import Thread
import os
import logging

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://johan:123456@localhost:3306/flightflow'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'huan_zhong2@126.com'
app.config['MAIL_PASSWORD'] = 'zh520596'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '<huan_zhong2@126.com>'
app.config['FLASKY_ANDMIN'] = '13251183@bjtu.edu.cn'

# 把程序实例作为参数传给构造函数，初始化主类的实例
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)

# 为shell命令添加一个上下文

def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

manager.add_command("shell",Shell(make_context = make_shell_context))
manager.add_command('db',MigrateCommand)

# 定义Role和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' %self.name

class User(db.Model):
    __tablename__ = 'users'   
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' %self.username

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
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                user = User(username = form.username.data,password = form.password.data)
                db.session.add(user)
                session['known'] = False
                if app.config['FLASKY_ANDMIN']:
                    send_email(app.config['FLASKY_ANDMIN'],'NEW User',\
                               'mail/new_user',user=user)
                    form.username.data = ''
                    form.password.data = ''
                    return redirect(url_for('login'))
            else :
                session['known'] = True
            session['username'] = form.username.data
            session['password'] = form.password.data
            form.username.data = ''
            form.password.data = ''
            return redirect(url_for('index'))
        return render_template('login.html',form = form,name = session.get('username'),\
            known = session.get('known',False))
    except Exception as e:
        logging.exception(e)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/flow')
def flow():
    return render_template('flow.html')


# @app.route("/mail")
# def ok():
# 	msg = Message(
#               'Hello',
# 	       sender='huan_zhong2@126.com',
# 	       recipients=
#                ['13251183@bjtu.edu.cn'])
# 	msg.body = "This is the email body"
# 	mail.send(msg)
# 	return "Sent"

if __name__ == "__main__":
    manager.run()   # 服务器由manager.run() 启动，启动后就能解析命令行