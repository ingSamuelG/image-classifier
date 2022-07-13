from flask import render_template, redirect, url_for, abort, flash, request,\
    session
from flask_login import login_user, logout_user
from ..models import RateUser
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email  = form.email.data, first_name = form.first_name.data , last_name = form.last_name.data, password = form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('You can now login.', 'alert-success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = RateUser.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.', 'alert-danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    flash('You have been logged out.', 'alert-success')
    return redirect(url_for('main.index'))