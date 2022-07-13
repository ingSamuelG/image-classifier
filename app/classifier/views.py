from email.mime import image
from numpy import imag
from  sqlalchemy.sql.expression import func
from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import classifier
from ..models import Image_label,Image
from .form import RateForm
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