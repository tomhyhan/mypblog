from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from myblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators={DataRequired(), Length(min=2, max=20)})
    email = StringField('Email',
                        validators={DataRequired(), Email()})
    password = PasswordField('Password',
                             validators={DataRequired(), Length(min=6)})
    confirm_password = PasswordField('Confirm Password',
                             validators={DataRequired(), Length(min=6), EqualTo('password')})
    submit = SubmitField('Create your own Blog')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exist.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exist.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators={DataRequired(), Email()})
    password = PasswordField('Password',
                             validators={DataRequired(), Length(min=6)})
    remember = BooleanField('Stay Signed in')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators={DataRequired(), Length(min=2, max=20)})
    email = StringField('Email',
                        validators={DataRequired(), Email()})
    description = TextAreaField('Description')
    picture = FileField('Upload Profile Picture', validators={FileAllowed(['jpg','png'])})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exist.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already exist.')


class ForgotEmailForm(FlaskForm):

    email = StringField('Please Enter your email', validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with the email you provided')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password',
                             validators={DataRequired(), Length(min=6)})
    confirm_password = PasswordField('Confirm Password',
                             validators={DataRequired(), Length(min=6), EqualTo('password')})
    submit = SubmitField('Submit')

