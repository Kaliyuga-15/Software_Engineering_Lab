from flask import Blueprint, render_template, redirect, url_for, request, session, flash, g
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', endpoint='index')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.get('user'): 
        if g.user.role == 'admin': return redirect(url_for('admin.dashboard'))
        if g.user.role == 'employee': return redirect(url_for('employee.dashboard'))
        return redirect(url_for('consumer.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session.clear()
            session['user_id'] = user.id
            if user.role == 'admin': return redirect(url_for('admin.dashboard'))
            if user.role == 'employee': return redirect(url_for('employee.dashboard'))
            return redirect(url_for('consumer.dashboard'))
        else:
            flash('Invalid credentials')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
