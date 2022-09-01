from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from ..models import RateUser,Image_label
from .form import RegistrationForm, UpdateUserForm
import datetime
from . import users
from .. import db

ITEMS_PER_PAGE = 5

@users.route('/create_user/', methods=['GET', 'POST'])
@login_required
def create_user():
    form = RegistrationForm()
    if current_user.role_id != 1:
        abort(401)
    
    if form.validate_on_submit():
        user = RateUser(email  = form.email.data, first_name = form.first_name.data , last_name = form.last_name.data, organization = form.organization.data ,password = form.password.data, role_id = 2)

        db.session.add(user)
        db.session.commit()
        flash('{} created'.format( user.first_name), 'alert-success')
        return redirect(url_for('users.create_user'))

    for field, error in form.errors.items():
        flash('{}:{}'.format(field, error[0]), 'alert-danger')
    return render_template('user/create.html', form=form)

@users.route('/page/<page>')
@login_required
def view_users(page):

    if current_user.role_id != 1:
        abort(401)
    
    users = RateUser.query.paginate(page = int(page), per_page = ITEMS_PER_PAGE)
    paginated_users= (users.items)

    return render_template('user/index.html', users = users, paginated_users = paginated_users, page = int(page))


@users.route('/update_users/id/<id>', methods=['GET', 'POST'])
@login_required
def update_users(id):

    if current_user.role_id != 1:
        abort(401)

    user = RateUser.query.get_or_404(int(id))
    user_name = user.first_name
    if user:
        form = UpdateUserForm()

        if form.validate_on_submit():
            newEmailUser = RateUser.query.filter_by(email=form.email.data).first()

            if newEmailUser and newEmailUser.id == user.id:
                user.email = form.email.data
            elif newEmailUser and newEmailUser.id != user.id:
                flash('this email is used by another user', 'alert-danger')
                return redirect(url_for("users.update_users", id = id ))
            else:
                user.email = form.email.data

            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.organization = form.organization.data
            user.updated_at = datetime.datetime.utcnow()
            
            if form.password.data != "":
                user.password  = form.password.data

            flash('{} updated'.format( user.first_name), 'alert-success')
            db.session.commit()

            return redirect(url_for("users.view_users", page = 1 ))

    for field, error in form.errors.items():
        flash('{}:{}'.format(field, error[0]), 'alert-danger')
    
    return render_template('/user/update.html', form = form, id = id, user_name = user_name, user = user)


@users.route('/delete_users/id/<id>')
@login_required
def delete_users(id):

    if current_user.role_id != 1:
        abort(401)
        
    user = RateUser.query.get_or_404(int(id))
    db.session.delete(user)
    flash('{} deleted'.format(user.role.name), 'alert-success')
    db.session.commit()
    return redirect(url_for("users.view_users", page = 1 ))


@users.route('/user/<id>/stats/')
@login_required
def stats(id):
    
    if current_user.role_id != 1:
        abort(401)

    user = RateUser.query.filter_by(id=id).first()
    ratings = Image_label.query.filter_by(user_id=id).order_by(Image_label.created_at.asc()).all()

    last = ratings[-1]
    amount_ratings = len(ratings)
    lastRatings = []
    days = {}
    for rating in ratings:
        count = 0
        for r in ratings:
            if r.created_at.day == rating.created_at.day and r.created_at.month == rating.created_at.month and r.created_at.year == rating.created_at.year:
                count+=1

                days["{}-{}-{}".format(r.created_at.year, r.created_at.month ,r.created_at.day )] = count
            else:
                continue

        if rating.created_at.day == last.created_at.day and rating.created_at.month == last.created_at.month and rating.created_at.year == last.created_at.year:
            lastRatings.append(rating)
        
    amount_lastRatings = len(lastRatings)
    
    maxDay = ("init", 0)
    daysTojson = [['Days', 'Images']]
    for key, value in  days.items():
        if value > maxDay[1]:
            maxDay = key, value
            MaxdateArray = key.split("-")
            f_month  = datetime.datetime.strptime(MaxdateArray[1], "%m").strftime("%B")
        daysTojson.append([key, value])
    
    dailyAverage = amount_ratings/ len(days.items())
    vsBestDayPerformance = (amount_lastRatings * 100)/ maxDay[1]
    vsAverage = (amount_lastRatings * 100) / dailyAverage

    return render_template('/user/stats.html', id = id, user = user, amount_ratings = amount_ratings, last = last, amount_lastRatings = amount_lastRatings, maxDay= maxDay, MaxdateArray = MaxdateArray, f_month =f_month, dailyAverage = dailyAverage, vsBestDayPerformance = vsBestDayPerformance, vsAverage = vsAverage, daysTojson= daysTojson)