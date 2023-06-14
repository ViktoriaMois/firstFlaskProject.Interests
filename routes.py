from sqlalchemy.sql.functions import user

import forms
import models
from app import app, db, mail
from flask import redirect, flash, url_for
from flask import render_template, request
from flask_login import current_user, login_user, login_required, logout_user
from forms import LoginForm, RegistrationForm, AvatarForm, InterestForm, MessageForm
from logic import get_concate_username
from models import User, Interest
from flask_mail import Message
from oauth import OAuthSignIn


@app.route('/')
def index():
    interests = Interest.query.all()
    return render_template('index.html', title="Home", user=current_user, interests=interests)


def send_mail(address):
    user = User.query.filter_by(username=current_user.username).first()
    with mail.connect() as conn:
        msg = Message("You were added to friends!", sender="your_email", recipients=[address])
        msg.body = "Hello boddy"
        msg.html = "<h1>User " + user.username + " has added you to friends</h1>"
        conn.send(msg)


@app.route('/message/<username>', methods=['GET', 'POST'])
@login_required
def contact(username):
    user = User.query.filter_by(username=username).first()
    form = MessageForm()
    if form.validate_on_submit():
        address = user.email
        message = form.message.data

        try:
            private_email(address, message)
            flash('Message sent successfully', 'success')
            form.message.data = ''

        except Exception as e:
            print(e)
            flash('Error occurred while sending the message', 'danger')

    return render_template('message.html', form=form)


def private_email(address, message):
    user = User.query.filter_by(username=current_user.username).first()
    msg = Message('Contact Form Message', sender='your_email', recipients=[address])
    msg.body = f'Name: {user.username}\nEmail: {user.email}\nMessage: {message}'
    mail.send(msg)


@app.route('/users')
@login_required
def show_all_users():
    all_users = User.query.all()
    return render_template('allUsersList.html', users=all_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for("index")))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect((url_for("index")))
        login_user(user, remember=True)
        return redirect((url_for("index")))
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect((url_for("index")))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! Registration is completed!')
        return redirect((url_for('login')))
    return render_template("registration.html", form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect((url_for("index")))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="Profile", user=current_user)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = AvatarForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.set_avatar(avatar=form.avatar.data)
        user.set_email(email=form.email.data)
        db.session.commit()
        return redirect((url_for('profile')))
    return render_template('avatar.html', title="Settings", form=form)


@app.route('/interest', methods=['GET', 'POST'])
@login_required
def interests():
    form = InterestForm()
    if form.validate_on_submit():
        interest = Interest(user_id=current_user.id, username=current_user.username, theme=form.theme.data,
                            description=form.description.data)
        db.session.add(interest)
        db.session.commit()
        return redirect((url_for('index')))
    return render_template('interest.html', title="Interest", form=form)


@app.route('/add_friend/<username>')
@login_required
def add_friend(username):
    user = User.query.filter_by(username=username).first()
    if not user is None:
        current_user.add_friend(user)
        db.session.commit()
        # send_mail(user.email)
    all_users = User.query.all()
    return render_template('allUsersList.html', users=all_users)


@app.route('/remove_friend/<username>')
@login_required
def remove_friend(username):
    user = User.query.filter_by(username=username).first()
    if not user is None:
        current_user.delete_friend(user)
        db.session.commit()
    all_users = User.query.all()
    return render_template('allUsersList.html', users=all_users)


@app.route('/friends_interests')
@login_required
def friends_interests():
    users = User.query.all()
    interests = Interest.query.all()
    return render_template('friendsInterests.html', title="Friends' Interests", interests=interests, users=users)


@app.route('/profile/<username>')
@login_required
def see_profile(username):
    user = User.query.filter_by(username=username).first()
    interests = Interest.query.all()
    return render_template('otherUserProfile.html', user=user, interests=interests)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    user_id, token = oauth.callback()
    if user_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        username = get_concate_username(token, user_id)

        user = User(user_id=user_id, token=token, username=username)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for('login'))
