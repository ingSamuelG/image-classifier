from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import examples
from ..models import Image, Image_Rating, Image_label
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


@examples.route('/see/<type>/<id>', methods=['GET', 'POST'])
@login_required
def showType(type,id):
    
    if current_user.role_id != 1:
        if current_user.role_id != int(id):
            return redirect(url_for('main.index'))


    if type == 'user_id':
        all_3 =  Image_label.query.filter_by(rating_score = 3, user_id = int(id))
        all_2 =  Image_label.query.filter_by(rating_score = 2, user_id = int(id))
        all_1 =  Image_label.query.filter_by(rating_score = 1, user_id = int(id))
        all_0 =  Image_label.query.filter_by(rating_score = 0, user_id = int(id))
        all_m1 =  Image_label.query.filter_by(rating_score = -1, user_id = int(id))
        all_m2 =  Image_label.query.filter_by(rating_score = -2, user_id = int(id))
        all_m3 =  Image_label.query.filter_by(rating_score = -3, user_id = int(id))
    
    if type == 'combined':
        all_3 =  Image_label.query.filter_by(rating_score = 3)
        all_3_old  = Image_Rating.query.filter_by(rating_score = 3)

        all_2 =  Image_label.query.filter_by(rating_score = 2)
        all_2_old = Image_Rating.query.filter_by(rating_score = 2)


        all_1 =  Image_label.query.filter_by(rating_score = 1)
        all_1_old = Image_Rating.query.filter_by(rating_score = 1)

        all_0 =  Image_label.query.filter_by(rating_score = 0)
        all_0_old = Image_Rating.query.filter_by(rating_score = 0)

        all_m1 =  Image_label.query.filter_by(rating_score = -1)
        all_m1_old = Image_Rating.query.filter_by(rating_score = -1)

        all_m2 =  Image_label.query.filter_by(rating_score = -2)
        all_m2_old = Image_Rating.query.filter_by(rating_score = -2)

        all_m3 =  Image_label.query.filter_by(rating_score = -3)
        all_m3_old =  Image_Rating.query.filter_by(rating_score = -3)

    ids_3 = []
    ids_2 = []
    ids_1 = []
    ids_0 = []
    ids_m1 = []
    ids_m2 = []
    ids_m3 = []

    if type == 'combined':
        for rate in all_3.limit(20):
            ids_3.append(rate.image_id)
        for rate in all_3_old.limit(20):
            ids_3.append(rate.image_id)
        
        for rate in all_2.limit(20):
            ids_2.append(rate.image_id)
        for rate in all_2_old.limit(20):
            ids_2.append(rate.image_id)   

        for rate in all_1.limit(20):
            ids_1.append(rate.image_id)
        for rate in all_1_old.limit(20):
            ids_1.append(rate.image_id)

        for rate in all_0.limit(20):
            ids_0.append(rate.image_id)
        for rate in all_0_old.limit(20):
            ids_0.append(rate.image_id) 

        for rate in all_m1.limit(20):
            ids_m1.append(rate.image_id)
        for rate in all_m1_old.limit(20):
            ids_m1.append(rate.image_id)    

        for rate in all_m2.limit(20):
            ids_m2.append(rate.image_id)
        for rate in all_m2_old.limit(20):
            ids_m2.append(rate.image_id)

        for rate in all_m3.limit(20):
            ids_m3.append(rate.image_id)
        for rate in all_m3_old.limit(20):
            ids_m3.append(rate.image_id)

    else:
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

