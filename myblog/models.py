from datetime import datetime
from myblog import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Create_token
from myblog.config import S3Config


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    image_file = db.Column(db.String(100), nullable=False, default=f"{S3Config.S3_LOCATION}default.jpg")
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('Project', backref='author', lazy=True)
    articles = db.relationship('Article', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1200):
        s = Create_token(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Create_token(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data_posted = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    replies = db.relationship('Reply', backref='project', lazy=True)

    def __repr__(self):
        return f"Project('{self.title}','{self.data_posted},,'{self.user_id}')"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data_posted = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Article('{self.title}','{self.data_posted}')"


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    repliesto = db.relationship('Tore', backref='replies', lazy=True)

    def __repr__(self):
        return f"Reply('{self.content}','{self.date_posted}','{self.project_id},{self.username}')"


class Tore(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=False)

    def __repr__(self):
        return f"ReplyTo('{self.content}','{self.date_posted}','{self.reply_id}')"


