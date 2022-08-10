from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import datetime
from flask_login import current_user

class RateForm(FlaskForm):
    radio = RadioField("Image Rating:" , choices=[(-3, "-3"), (-2, "-2"), (-1, "-1"), (0, "0"), (1, "1"),(2,"2"),(3,"3")], validators=[DataRequired()])
    contentType = BooleanField("Inappropriate content" ,default = False)
    nextBtn = SubmitField('Next page')

class DatePerformanceForm(FlaskForm):
    date = DateField("Select the date:")
    checkBtn = SubmitField('check')