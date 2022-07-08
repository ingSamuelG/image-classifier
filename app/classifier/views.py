import imp
from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import classifier
from .form import RateForm


@classifier.route('/protected')

def protected():
    form = RateForm()
    return render_template('classifier/index.html' , form = form)