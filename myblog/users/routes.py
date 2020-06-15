from flask import Blueprint, render_template, flash, redirect, url_for, request
from myblog.users.forms import (RegistrationForm, LoginForm,
                                UpdateProfileForm ,ForgotEmailForm,
                                ResetPasswordForm)
from myblog import db, bcrypt
from myblog.models import User, Project
from flask_login import login_user, current_user, logout_user, login_required
from myblog.users.utils import save_picture, send_email
from myblog.config import S3Config

users = Blueprint("users",__name__)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.project', user=current_user.username))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash('Logged in Successfully','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.project', user=current_user.username)) # depending on the user
        else:
            flash("The email or password you entered is incorrect" , 'danger')
    return render_template('login.html',form = login_form,title='Login')


@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.project', user=current_user.username))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        user = User(username=registration_form.username.data, email=registration_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created! Please Login", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form = registration_form,title='Register')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# 'static', filename='profile_picture/' +
@users.route('/profile/', methods= ['GET','POST'])
@login_required
def profile():
    username = User.query.filter_by(username=current_user.username).first_or_404()
    image_file = current_user.image_file
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data, S3Config.S3_BUCKET)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.description = profile_form.description.data
        db.session.commit()
        flash('Your profile has been updated','success')
        return redirect(url_for('users.profile'))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.description.data = current_user.description
    return render_template('profile.html',title='Profile',
                                   user=username, image_file=image_file, form =profile_form)


@users.route('/profile/<user>')
def static_profile(user):
    username = User.query.filter_by(username=user).first_or_404()
    return render_template('static_profile.html', title='Profile Info', user = username)


@users.route('/forgot_password', methods= ['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.project', user=current_user.username))
    forgot_form = ForgotEmailForm()
    if forgot_form.validate_on_submit():
        user = User.query.filter_by(email=forgot_form.email.data).first()
        send_email(user)
        flash('Email has been sent to your account','success')
        return redirect(url_for('users.login'))
    return render_template('forgot_password.html',form=forgot_form, title='Forgot Password')


@users.route('/reset_password/<token>', methods= ['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.project', user=current_user.username))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('users.forgot_password'))
    reset_form = ResetPasswordForm()
    if reset_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reset_form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',form=reset_form, title='Reset Password')


@users.route('/blog_history/<user>')
def blog_history(user):
    username = User.query.filter_by(username=user).first_or_404()
    posts = Project.query.filter_by(user_id=username.id).order_by(Project.data_posted.desc()).all()
    post_dict = {}
    for post in posts:
        post = [post.title, post.id, post.data_posted.strftime("%m %d %Y")]
        title, id, date = post
        if date in post_dict.keys():
            post_dict[date].append([id,title])
        else:
            post_dict[date] = [[id, title]]
    return render_template('blog_history.html', title='Blog history', posts=post_dict, user=username)
