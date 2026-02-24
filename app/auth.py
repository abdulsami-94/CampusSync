import re
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

def validate_email_domain(email):
    """Validate email ends with @asmedu.org for ASM CSIT students."""
    allowed_domain = current_app.config['ALLOWED_EMAIL_DOMAIN']
    email = email.strip().lower()
    return email.endswith(f'@{allowed_domain}') and '@' in email

def validate_password(password):
    """Validate password has minimum length."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email domain - only @asmedu.org allowed
        if not validate_email_domain(email):
            flash('Only official ASM CSIT email addresses (@asmedu.org) are allowed for registration.', 'danger')
            return redirect(url_for('auth.register'))

        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'danger')
            return redirect(url_for('auth.register'))

        # Check if user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('auth.register'))

        # Create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, role='student')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'staff':
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            remember_val = bool(request.form.get('remember'))
            login_user(user, remember=remember_val)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('auth/login.html', title='Login')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
