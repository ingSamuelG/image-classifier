from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import examples
from ..models import Image, Image_Rating
from .. import db
import random


@examples.route('/rate', methods=['GET', 'POST'])
@login_required
def total():
    all_3 =  Image_Rating.query.filter_by(rating_score = 3)
    all_2 =  Image_Rating.query.filter_by(rating_score = 2)
    all_1 =  Image_Rating.query.filter_by(rating_score = 1)
    all_0 =  Image_Rating.query.filter_by(rating_score = 0)
    all_m1 =  Image_Rating.query.filter_by(rating_score = -1)
    all_m2 =  Image_Rating.query.filter_by(rating_score = -2)
    all_m3 =  Image_Rating.query.filter_by(rating_score = -3)

    ids_3 = []
    ids_2 = []
    ids_1 = []
    ids_0 = []
    ids_m1 = []
    ids_m2 = []
    ids_m3 = []
    
    for rate in all_3:
        ids_3.append(rate.image_id)

    for rate in all_2:
        ids_2.append(rate.image_id)

    for rate in all_1:
        ids_1.append(rate.image_id)

    for rate in all_0:
        ids_0.append(rate.image_id)

    for rate in all_m1:
        ids_m1.append(rate.image_id)

    for rate in all_m2:
        ids_m2.append(rate.image_id)

    for rate in all_m3:
        ids_m3.append(rate.image_id)

    ramdom_3 = random.choices(ids_3, k=10)
    ramdom_2 = random.choices(ids_2, k=10)
    ramdom_1 = random.choices(ids_1, k=10)
    ramdom_0 = random.choices(ids_0, k=10)
    ramdom_m1 = random.choices(ids_m1, k=10)
    ramdom_m2 = random.choices(ids_m2, k=10)
    ramdom_m3 = random.choices(ids_m3, k=10)

    result_3 = Image.query.filter(Image.id.in_(ramdom_3)).all()
    result_2 = Image.query.filter(Image.id.in_(ramdom_2)).all()
    result_1 = Image.query.filter(Image.id.in_(ramdom_1)).all()
    result_0 = Image.query.filter(Image.id.in_(ramdom_0)).all()
    result_m1 = Image.query.filter(Image.id.in_(ramdom_m1)).all()
    result_m2 = Image.query.filter(Image.id.in_(ramdom_m2)).all()
    result_m3 = Image.query.filter(Image.id.in_(ramdom_m3)).all()

    return render_template('examples/summaries.html' , result_3 = result_3, result_2 = result_2, result_1 = result_1,result_0 = result_0, result_m1 = result_m1, result_m2 = result_m2, result_m3 = result_m3 )
    

    # print(image_wo_rating)


    # if image_wo_rating:
    #     if form.validate_on_submit():
    #         label = Image_label(rating_score = form.radio.data, user_id = current_user.id)
    #         image_wo_rating.image_label_rating.append(label)
    #         db.session.add(image_wo_rating)
    #         db.session.commit()
    #         return redirect(url_for('classifier.rate'))

    #     return render_template('classifier/index.html' , form = form, image_wo_rating = image_wo_rating)
    
    # else:
    #     return render_template('classifier/noImg.html')