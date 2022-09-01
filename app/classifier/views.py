from  sqlalchemy.sql.expression import func, and_
from flask import render_template, redirect, url_for, abort, flash, request, session,\
    current_app, make_response
from flask_login import login_required, current_user
from . import classifier
import calendar
from ..models import Image_label,Image, RateUser
from .form import RateForm
from datetime import datetime, date, timedelta
from .. import db
import random

def describe_rates(rates):
    ratings = []
    rated_m3 = 0
    rated_m2 = 0
    rated_m1 = 0
    rated_0 = 0
    rated_3 = 0
    rated_2 = 0
    rated_1 = 0
    for rating in rates:
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

    return ratings ,describe_ratings


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
            label = Image_label(rating_score = form.radio.data, inappropriate_ct = form.contentType.data, user_id = current_user.id)
            image_wo_rating.image_label_rating.append(label)
            db.session.add(image_wo_rating)
            db.session.commit()
            return redirect(url_for('classifier.rate'))

        return render_template('classifier/index.html' , form = form, image_wo_rating = image_wo_rating)
    
    else:
        return render_template('classifier/noImg.html')

@classifier.route('/performance/user/<id>/', methods=['GET', 'POST'])
@login_required
def rate_performance(id):
    
    if current_user.role_id != 1:
        return redirect(url_for('classifier.rate'))


    DEFUALT_TIME_TO_RATE = timedelta(seconds=2)
    year = request.args.get("year") 
    month = request.args.get("month")
    day= request.args.get("day")

    w_day = False
    w_year = False
    w_month = False
    yearly_stats ={}
    monthly_stats = {}
    daily_stats = {}
    hourly_stats = {}
    
    if not year:
        oldest_rating= Image_label.query.filter(Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).first()
        if oldest_rating:
            placeholder_year = oldest_rating.created_at.year
        else:
            placeholder_year = datetime.utcnow().year
    else:
        placeholder_year = int(year)

    user = RateUser.query.filter_by(id = int(id)).first()
    current_year = datetime.utcnow().year

    dif_of_years = current_year - placeholder_year

    for r in range(0,dif_of_years+1):
        eval_year = placeholder_year+r
        start_date = datetime(eval_year , 1, 1)
        end_date = datetime(eval_year , 12, 31)
        query = Image_label.query.filter(and_(and_(func.date(Image_label.created_at) >= start_date),\
                                              func.date(Image_label.created_at) <= end_date),Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).all()
        
        describe_ratings = describe_rates(query)[1]
        ratings = describe_rates(query)[0]
        dif = end_date - start_date
        amount = len(query)

        total_x_hour = (amount / dif.total_seconds()) * 3600
        yearly_stats[str(eval_year)] = {"ratings": describe_ratings, "Images rated": amount, "Images per hour": total_x_hour}

    if not month and not day and not year:
        display_stats = yearly_stats
        display_chart = False

    daysInMonth = 0
    if year and not month:
        for r in range(1,13):
            datetime_object = datetime.strptime(str(r), "%m")
            month_name = datetime_object.strftime("%B")
            start_date = datetime(int(year) , r, 1)
            daysInMonth= calendar.monthrange(int(year), r)[1]
            end_date = datetime(int(year) , r, daysInMonth)
            query = Image_label.query.filter(and_(and_(func.date(Image_label.created_at) >= start_date),\
                                                func.date(Image_label.created_at) <= end_date),Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).all()
            
            describe_ratings = describe_rates(query)[1]
            ratings = describe_rates(query)[0]
            dif = end_date - start_date
            amount = len(query)

            total_x_hour = (amount / dif.total_seconds()) * 3600

            if ratings:
                has_chart = True
            else:
                has_chart = False
            monthly_stats[month_name] = {"ratings": describe_ratings, "Images rated": amount,"Images per hour": total_x_hour, "data": ratings, "has_chart": has_chart, "month_num": r ,"daysInMonth": daysInMonth}
        
        display_stats = monthly_stats
        display_chart = True
        w_year = int(year)
    
    if year and month and not day:
        datetime_object = datetime.strptime(month, "%B")
        month_num = datetime_object.month
        daysInMonth= calendar.monthrange(int(year), month_num)[1]
        for d in range(1, daysInMonth+1):

            start_date = datetime(int(year) , month_num, d)

            if d == daysInMonth:
                end_date = datetime(int(year) , month_num, d)
            else:
                end_date = datetime(int(year) , month_num, d+1)

            query = Image_label.query.filter(and_(and_(func.date(Image_label.created_at) >= start_date),\
                                                func.date(Image_label.created_at) < end_date),Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).all()

            idle = timedelta(seconds=0)
            i = 0
            amount = len(query)
            for rt in query:
                if amount > i+1:
                    next = query[i+1]
                    dif = next.created_at - rt.created_at
                    
                    if i == 0 and dif != 0:
                        idle = (dif - DEFUALT_TIME_TO_RATE) 
                    elif i > 0 and dif != 0:
                        idle += (dif - DEFUALT_TIME_TO_RATE)
                    else:
                        idle +=  timedelta(seconds=0)
                    i+=1
                else:
                    # if not isinstance(idle,int):
                    #     idle =  timedelta(seconds=0)
                    # else:
                    #     idle +=  timedelta(seconds=0)
                    i+=1
            

            describe_ratings = describe_rates(query)[1]
            ratings = describe_rates(query)[0]

            if ratings:
                has_chart = True
            else:
                has_chart = False

            if query:
                first_date = query[0].created_at
                last_date = end_date
                dif = last_date - first_date
                
                total_x_hour = (amount / dif.total_seconds() ) * 3600
                total_x_hour_w_idle = (amount / (dif.total_seconds() - idle.total_seconds())) * 3600
                # amount = len(query)
                # total_x_hour = (amount / 86400 ) * 3600
            else:
                total_x_hour = (amount / 86400 ) * 3600
                total_x_hour_w_idle = 0
            

            daily_stats[str(d)]  = {"ratings": describe_ratings, "Images rated": amount,"Images per hour from the first rated to the last":total_x_hour ,"Images per hour without the idle time": total_x_hour_w_idle, "Idle time in rating cycle thru the day": idle ,"data": ratings,"has_chart": has_chart}
        
        display_chart = True
        display_stats = daily_stats
        # start_date = datetime(int(year) , r, 1)
        w_year = int(year)
        w_month = month
    
    if year and month and day:
        for hour in range(0, 24):
            datetime_object = datetime.strptime(month, "%B")
            month_num = datetime_object.month
            # daysInMonth= calendar.monthrange(int(year), month_num)[1]

            start_date = datetime(int(year) , month_num, int(day), hour) 

            if hour < 23:
                end_date = datetime(int(year) , month_num, int(day), hour+1)
            else:
                start_date = datetime(int(year) , month_num, int(day), 23) 
                end_date = datetime(int(year) , month_num, int(day)+1, 0)
            
            
            query = Image_label.query.filter(and_(and_(Image_label.created_at >= start_date,Image_label.created_at < end_date)),Image_label.user_id == int(id)).order_by(Image_label.created_at.asc()).all()

            idle = timedelta(seconds=0)
            hour_time= timedelta(hours=1)
            i = 0
            amount = len(query)
            for rt in query:
                if amount > i+1:
                    next = query[i+1]
                    dif = next.created_at - rt.created_at
                    
                    if i == 0 and dif != 0:
                        idle = (dif - DEFUALT_TIME_TO_RATE) 
                    elif i > 0 and dif != 0:
                        idle += (dif - DEFUALT_TIME_TO_RATE)
                    else:
                        idle +=  timedelta(seconds=0)
                    i+=1
                else:
                    # if not isinstance(idle,int):
                    #     idle =  timedelta(seconds=0)
                    # else:
                    #     id
                    i+=1

            describe_ratings = describe_rates(query)[1]
            ratings = describe_rates(query)[0]

            elapsed_time = hour_time - idle
            if query:
                first_date = query[0].created_at
                last_date = end_date
                dif = last_date - first_date
                total_x_hour = (amount  * 3600) / elapsed_time.total_seconds()
                
                # amount = len(query)
                # total_x_hour = (amount / 86400 ) * 3600
            else:
                total_x_hour = (amount / 3600 )

            describe_ratings = describe_rates(query)[1]
            ratings = describe_rates(query)[0]

            if ratings:
                has_chart = True
            else:
                has_chart = False



            hourly_stats[str(hour)]  = {"ratings": describe_ratings,"Images rated x elapsed time": "{} x {}".format(amount, elapsed_time),"Images per hour": total_x_hour , "Idle time in rating cycle thru the hour": idle ,"data": ratings,"has_chart": has_chart}
        
        w_year = int(year)
        w_month = month
        w_day = day
        display_chart =  True
        display_stats = hourly_stats
        
    return render_template('classifier/performance.html', display_stats = display_stats, display_chart = display_chart , w_year = w_year, w_month = w_month, w_day = w_day, id=id)