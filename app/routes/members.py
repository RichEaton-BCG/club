from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User
from werkzeug.security import generate_password_hash

bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(username=username, email=email,
                        password=hashed_password)

        # Save to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created successfully!', 'success')
            # Adjust the redirect if login is implemented
            return redirect(url_for('members.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating your account. Please try again.', 'danger')
            print(f"Error: {e}")

    # Render the signup form for GET requests
    return render_template('members/signup.html')
