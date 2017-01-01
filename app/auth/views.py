from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user

from ..models import User
from .forms import LoginForm,RegistrationForm
from . import auth
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
    loginform = LoginForm()
    registerform = RegistrationForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user,loginform.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    if registerform.validate_on_submit():
        user = User(email=registerform.email.data,
                    username=registerform.username.data,
                    password=registerform.password.data)
        registerform.email.data = ''
        db.session.add(user)
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html',loginform=loginform,registerform=registerform)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


