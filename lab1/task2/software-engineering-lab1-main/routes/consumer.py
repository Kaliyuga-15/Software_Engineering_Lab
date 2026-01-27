from flask import Blueprint, render_template, redirect, url_for, flash, g, request
from models import Bill, db

consumer_bp = Blueprint('consumer', __name__, url_prefix='/consumer')

@consumer_bp.before_request
def check_consumer():
    if not g.get('user') or g.user.role != 'consumer':
        return redirect(url_for('auth.login'))

@consumer_bp.route('/dashboard')
def dashboard():
    bills = Bill.query.filter_by(user_id=g.user.id).order_by(Bill.bill_date.desc()).all()
    return render_template('consumer_dashboard.html', user=g.user, bills=bills)

from datetime import datetime
import re

@consumer_bp.route('/pay/<int:bill_id>', methods=['GET', 'POST'])
def pay_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    if bill.user_id != g.user.id: 
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        card_number = request.form.get('card_number', '').replace(' ', '')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        

        errors = []
        # No Validation - Accept Anything
        errors = []
            
        if errors:
            for err in errors: flash(err)
        else:

            bill.status = 'Paid'
            db.session.commit()
            flash('Payment Successful! Thank you.')
            return redirect(url_for('consumer.dashboard'))
            
    return render_template('payment.html', bill=bill, now=datetime.utcnow())
