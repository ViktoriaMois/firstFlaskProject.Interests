from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

friends = db.Table('friends', db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
                   db.Column('friend_id', db.Integer, db.ForeignKey("user.id")))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), index=True, unique=True)
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    avatar = db.Column(db.String(256))
    token = db.Column(db.String(256), nullable=True, unique=True)
    friends_added = db.relationship('User', secondary=friends,
                                    primaryjoin=(friends.c.user_id == id),
                                    secondaryjoin=(friends.c.friend_id == id),
                                    backref=db.backref('friends', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_avatar(self, avatar):
        self.avatar = avatar

    def set_email(self, email):
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_added_friend(self, user):
        return self.friends_added.filter(friends.c.friend_id == user.id).count() > 0

    def add_friend(self, user):
        if not self.is_added_friend(user):
            self.friends_added.append(user)

    def delete_friend(self, user):
        if self.is_added_friend(user):
            '''
            tmp = delete(friends).where(friends.c.friend_id == user.id)
            db.session.execute(tmp)
            db.session.commit()
            '''
            self.friends_added.remove(user)

    def __repr__(self):
        return 'User - {} with email {}'.format(self.username, self.email)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), index=True)
    theme = db.Column(db.String(40), index=True)
    description = db.Column(db.String(1000))

    def __init__(self, user_id, theme, description, username):
        self.user_id = user_id
        self.theme = theme
        self.description = description
        self.username = username

    def __repr__(self):
        return 'Interest - {}'.format(self.theme, self.description, self.username)

