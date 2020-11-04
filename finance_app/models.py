from finance_app import app, db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique = True)
    hash = db.Column(db.String(256), nullable = False)
    cash_cent = db.Column(db.Integer, default = 1000000)
    # cash_cent DEFAULT 1000000

    # relationships
    transact_id = db.relationship('Transact', backref='owner', lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.hash = self.set_password(password)
        # self.cash_cent = cash_cent

    def set_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f'{self.username} has been created with {self.cash_cent/100}.'


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.String(50), nullable = False, unique = True)
    name = db.Column(db.String(150), nullable = False)

    # relationships
    transact_id = db.relationship('Transact', backref='business', lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.hash = self.set_password(password)
        # self.cash_cent = cash_cent

    def set_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f'{self.username} has been created with {self.cash_cent/100}.'


class Transact(db.Model):
    __tablename__ = 'transact'

    id = db.Column(db.Integer, primary_key = True)
    shares = db.Column(db.Integer, nullable = False)
    price_each_cent = db.Column(db.Integer, nullable = False)
    time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable = False)

    # relationships
    # user = db.relationship('User', foreign_keys='Transact.user_id')
    # company = db.relationship('Company', foreign_keys='Transact.company_id')

    def __init__(self, shares, price_each_cent, time, company_id, user_id):
        self.shares = shares
        self.price_each_cent = price_each_cent
        self.time = time
        self.company_id = company_id
        self.user_id = user_id

    def __repr__(self):
        return f'{self.shares} share transaction for ${self.price_each_cent/100}.'


