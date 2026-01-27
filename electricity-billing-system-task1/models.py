from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)

    role = db.Column(db.String(20), nullable=False, default='consumer')
    

    meter_number = db.Column(db.String(50), unique=True, nullable=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=True)
    connection_type = db.Column(db.String(20), nullable=True)
    
    password = db.Column(db.String(255), nullable=False)
    
    bills = db.relationship('Bill', backref='user', lazy=True)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    previous_reading = db.Column(db.Float, nullable=False)
    current_reading = db.Column(db.Float, nullable=False)
    units_consumed = db.Column(db.Float, nullable=False)
    
    total_amount = db.Column(db.Float, nullable=False)
    bill_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    penalty_amount = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='Unpaid')
