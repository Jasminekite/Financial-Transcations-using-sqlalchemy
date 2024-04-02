from config import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    pan_card = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=0.0)  # Add balance attribute with default value
    add_on = db.Column(db.DateTime, default=datetime.utcnow)
    update_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, account_name, username, first_name, last_name, email, mobile_no, pan_card):
        self.account_name = account_name
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile_no = mobile_no
        self.pan_card = pan_card

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, amount, transaction_type):
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type

