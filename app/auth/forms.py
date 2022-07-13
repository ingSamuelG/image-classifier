from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from ..models import RateUser

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(),Email(), Length(1,64)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8,24)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators = [DataRequired(), EqualTo('password2', "The password fields don't match")])
    password2 = PasswordField('Confirm password:', validators = [DataRequired()])
    submit = SubmitField('Change password')

# class ChangePasswordForm(FlaskForm):
#     password = PasswordField('Password:', validators = [DataRequired(), EqualTo('password2', "The password fields don't match")])
#     password2 = PasswordField('Confirm password:', validators = [DataRequired()])
#     code = StringField('Validation code: ', validators=[DataRequired()])
#     submit = SubmitField('Change password')

#     def validate_code(self, field):
#         user = User.query.filter_by(id=current_user.id).first()
#         expireDate = user.change_code_time + datetime.timedelta(minutes=30)
#         timeNow = datetime.datetime.utcnow()
#         if not user.verify_code(field.data):
#             raise ValidationError("The codes don't match")
#         if expireDate < timeNow:
#             raise ValidationError("The code expired")

# class RequestResetPasswordForm(FlaskForm):
#     email = StringField('Email:', validators=[DataRequired(),Email(), Length(1,64)])
#     submit = SubmitField('Change password')

#     def validate_email(self, field):
#         if not User.query.filter_by(email=field.data).first():
#             raise ValidationError("this is emial is not registered")

class RegistrationForm(FlaskForm):
    errors_mesagge_for_name = "use only letters and spaces" 

    email = StringField('Email:', validators = [Email(), Length(1,64), DataRequired()])
    # phone = StringField('Phone:', validators = [DataRequired(), Length(10,12)])
    
    first_name = StringField('First name:', validators = [ DataRequired() , Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])
    
    last_name = StringField('Last name:', validators = [DataRequired(), Regexp('^[A-Z a-z]*$',0, errors_mesagge_for_name)])

    # address1= StringField('Address:')
    # address2 = StringField('Apartment, suite, building:')
    # country = SelectField("Country or region:", choices = [("must be", "dinamic")])
    # state = StringField('State/Region:')
    # postal_code = StringField('Postal:')


    password = PasswordField('Password:', validators = [DataRequired(), EqualTo('password2', "The password fields don't match")])

    password2 = PasswordField('Confirm password:', validators = [DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("this is already registered")
    