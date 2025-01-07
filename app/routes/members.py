from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        postalcode = request.form.get('postalcode')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(
            username=username,
            password=hashed_password,
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postalcode=postalcode,
            is_member=False,  # Default value
            is_active=True,  # Default value
            skill_ranking=None  # Optional field
        )

        # Save to the database
        try:
            db.session.add(new_user)
            db.session.commit()

            # Automatically log the user in after creating their account
            login_user(new_user)

            flash('Your account has been created successfully!', 'success')

            # Adjust the redirect if login is implemented
            return redirect(url_for('members.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating your account. Please try again.', 'danger')
            print(f"Error: {e}")

    # Render the signup form for GET requests
    return render_template('members/signup.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Pass any required context variables to the template
    return render_template('members/dashboard.html', user=current_user)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('members.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect to the dashboard if already logged in
        return redirect(url_for('members.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            # Redirect to dashboard
            return redirect(url_for('members.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('members/login.html')
