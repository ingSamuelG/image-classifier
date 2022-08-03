from  sqlalchemy.sql.expression import func, and_
from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import classifier
from ..models import Image_label,Image, RateUser
from .form import RateForm, DatePerformanceForm
from .. import db
import random


@classifier.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    form = RateForm()
    all =  Image.query.filter(~Image.image_label_rating.any()).limit(1000)
    
    ids = []
    for image in all:
        ids.append(image.id)
    
    ramdom = random.choices(ids, k=1)[0]
    for image in all:
        if image.id == ramdom:
            image_wo_rating = image

    print(image_wo_rating)


    if image_wo_rating:
        if form.validate_on_submit():
            label = Image_label(rating_score = form.radio.data, user_id = current_user.id)
            image_wo_rating.image_label_rating.append(label)
            db.session.add(image_wo_rating)
            db.session.commit()
            return redirect(url_for('classifier.rate'))

        return render_template('classifier/index.html' , form = form, image_wo_rating = image_wo_rating)
    
    else:
        return render_template('classifier/noImg.html')

@classifier.route('/performance/user/<id>', methods=['GET', 'POST'])
@login_required
def rate_performance(id):
    form = DatePerformanceForm()
    date= None
    if form.validate_on_submit():
        date = form.date.data
        # Image_label.query.filter_by( cre= 3, user_id = int(id))
        # alls = Image_label.query.filter(Image_label.created_at.(date, date)).all()

        user = RateUser.query.filter_by(id = int(id)).first()
        
        query = Image_label.query.filter(and_(and_(func.date(Image_label.created_at) >= date),\
                                              func.date(Image_label.created_at) <= date),Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).all()
        ratings = []
        rated_m3 = 0
        rated_m2 = 0
        rated_m1 = 0
        rated_0 = 0
        rated_3 = 0
        rated_2 = 0
        rated_1 = 0
        for rating in query:
            json = rating.to_json()
            ratings.append(json)
            
            if rating.rating_score == -3:
                rated_m3+=1
            if rating.rating_score == -2:
                rated_m2+=1
            if rating.rating_score == -1:
                rated_m1+=1
            if rating.rating_score == 0:
                rated_0+=1
            if rating.rating_score == 3:
                rated_3+=1
            if rating.rating_score == 2:
                rated_2+=1
            if rating.rating_score == 1:
                rated_1+=1

        describe_ratings = {"rated_m3":rated_m3, 
                            "rated_m2":rated_m2,
                            "rated_m1":rated_m1,
                            "rated_0":rated_0,
                            "rated_3":rated_3,
                            "rated_2":rated_2,
                            "rated_1":rated_1
        }
        start_date = 0
        end_date = 0
        total_x_hour =0 
        dif = 0
        amount = 0
        if query:
            start_date = query[0].created_at
            end_date = query[-1].created_at

            dif = end_date - start_date
        
            amount = len(query)

            total_x_hour = (amount / dif.total_seconds()) * 3600

            print(total_x_hour)

    return render_template('classifier/performance.html' , form = form, date = date, id= id, ratings= ratings, total_x_hour = total_x_hour, dif = dif, amount = amount, describe_ratings = describe_ratings, user = user, query = query)