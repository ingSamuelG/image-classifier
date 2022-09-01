from flask_wtf import FlaskForm
from wtforms import  SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import datetime
from flask_login import current_user
from ..models import RateUser

class RegistrationForm(FlaskForm):
    errors_mesagge_for_name = "use only letters and spaces" 

    email = StringField('Email:', validators = [Email(), Length(1,64), DataRequired()])
    # phone = StringField('Phone:', validators = [DataRequired(), Length(10,12)])
    
    first_name = StringField('First name:', validators = [ DataRequired() , Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])
    
    last_name = StringField('Last name:', validators = [DataRequired(), Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])

    organization = StringField('Organitation:', validators = [DataRequired()], default="Rate user")

    password = PasswordField('Password:', validators = [DataRequired(), EqualTo('password2', "The password fields don't match")])

    password2 = PasswordField('Confirm password:', validators = [DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if RateUser.query.filter_by(email=field.data).first():
            raise ValidationError("this is already registered")

class UpdateUserForm(FlaskForm):
    errors_mesagge_for_name = "use only letters and spaces" 

    email = StringField('Email:', validators = [Email(), Length(1,64), DataRequired()])
    first_name = StringField('First name:', validators = [ DataRequired() , Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])
    organization = StringField('Change Organitation:', validators = [DataRequired()])
    last_name = StringField('Last name:', validators = [DataRequired(), Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])
    password = PasswordField('Password:', validators = [ EqualTo('password2', "The password fields don't match")])
    password2 = PasswordField('Confirm password:')

    update = SubmitField('Update')
