from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
# from werkzeug.security import check_password_hash, generate_password_hash
import hashlib
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.md5(password.encode()).hexdigest()

    def set_password(self, password):
        self.password_hash =  hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash ==  hashlib.md5(password.encode()).hexdigest()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.String(140), unique=False, nullable=False)
    text_hash=db.Column(db.String(80), unique=False, nullable=False)
    postdate = db.Column(db.String(80))

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.username