from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import datetime
from flask_login import current_user

class RateForm(FlaskForm):
    radio = RadioField("Image Rating:" , choices=[(-3, "-3"), (-2, "-2"), (-1, "-1"), (0, "0"), (1, "1"),(2,"2"),(3,"3")], validators=[DataRequired()])
    nextBtn = SubmitField('Next page')
