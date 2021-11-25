import jwt
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model class, which represent basic user entity
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    balance = db.Column(db.Float, nullable=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.balance = 0

    """
    Generates the Auth Token
        :return: string
    """

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=100),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'SECRET',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    """
    Decodes the auth token
       :param auth_token:
       :return: integer|string
    """

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, 'SECRET')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


# Transaction model class, which represent basic transaction entity
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    total = db.Column(db.Float, nullable=False)
    state = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, title, description, location, total, state, date, duration):
        self.title = title
        self.description = description
        self.location = location
        self.total = total
        self.state = state
        self.date = date
        self.duration = duration


# Category model class, which represent basic category entity
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __int__(self, name, icon, color):
        self.name = name
        self.icon = icon
        self.color = color
