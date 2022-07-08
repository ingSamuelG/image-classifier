from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/protected')
@login_required
def protected():
    return render_template('user.html')