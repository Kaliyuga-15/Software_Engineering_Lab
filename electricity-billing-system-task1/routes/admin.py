from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from models import User, Bill, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin():
    if not g.get('user') or g.user.role != 'admin':
        return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
def dashboard():
    consumers = User.query.filter_by(role='consumer').all()
    employees = User.query.filter_by(role='employee').all()
    bills = Bill.query.order_by(Bill.bill_date.desc()).all()
    return render_template('admin_dashboard.html', consumers=consumers, employees=employees, bills=bills)

import re

@admin_bp.route('/register_employee', methods=['GET', 'POST'])
def register_employee():
    if request.method == 'POST':
        username = request.form.get('username')
        employee_id = request.form.get('employee_id')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        errors = []
        if not username or not employee_id or not phone or not password:
            errors.append("All fields are required")
        if not re.match(r'^\d{10}$', phone):
            errors.append("Phone must be 10 digits")
            
        if User.query.filter_by(username=username).first():
            errors.append('Username exists')
        elif User.query.filter_by(employee_id=employee_id).first():
            errors.append('Employee ID exists')
            
        if errors:
            for e in errors: flash(e)
        else:
            new_emp = User(username=username, phone=phone, password=password, role='employee', employee_id=employee_id)
            db.session.add(new_emp)
            db.session.commit()
            flash('Employee Registered')
            return redirect(url_for('admin.dashboard'))
            
    return render_template('register_employee.html')

@admin_bp.route('/register_consumer', methods=['GET', 'POST'])
def register_consumer():
    from utils import validate_consumer_input
    
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        meter_number = request.form.get('meter_number')
        connection_type = request.form.get('connection_type')
        
        errors = []
        
        # 1. Modular Validation Call
        is_valid, error_msg = validate_consumer_input(username, phone, meter_number)
        if not is_valid:
            errors.append(error_msg)
            
        # 2. Duplicate Validation
        if User.query.filter_by(meter_number=meter_number).first():
            errors.append('Service Number (Meter Number) already exists')
        
        # Additional input check
        if not password:
            errors.append("Password is required")
            
        if errors:
            for e in errors: flash(e)
        else:
            new_con = User(
                username=username, phone=phone, password=password, 
                role='consumer', meter_number=meter_number, connection_type=connection_type
            )
            db.session.add(new_con)
            db.session.commit()
            flash('Consumer Registered Successfully')
            return redirect(url_for('admin.dashboard'))

    return render_template('register_consumer.html')


