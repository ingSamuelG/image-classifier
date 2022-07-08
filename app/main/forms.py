from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import datetime
from ..models import User, Scenario
from flask_login import current_user
from ..models import User


class SendEmailForm(FlaskForm):
    email = StringField('to:', validators=[DataRequired(),Email(), Length(1,64)])
    subject = StringField('subject:', validators=[DataRequired(), Length(1,64)])
    body = TextAreaField('body:', validators=[DataRequired()])
    submit = SubmitField('Send')

def get_scenarios_list(request):
    scenarios = Scenario.query.all()
    form = SelectScenario(request.POST, obj = scenarios)
    form.scenario.choices =[(sce.id, sce.label) for sce in scenarios]

class SelectScenario(FlaskForm):
    scenario = SelectField('Select your scenario:', choices = [], coerce=int)
    viewBtn = SubmitField('View')

class CompareScenario(FlaskForm):
    scenario_1 = SelectField('Select your first scenario:', choices = [], coerce=int)
    scenario_2 = SelectField('Select your second scenario:', choices = [], coerce=int)
    compareBtn = SubmitField('Compare')

    def validate_scenario_1(form, field):
        if field.data == form.scenario_2.data:
            raise ValidationError('You are selecting the same scenario to compare')

    def validate_scenario_2(form, field):
        if field.data == form.scenario_1.data:
            raise ValidationError('You are selecting the same scenario to compare')