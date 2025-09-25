from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd
from app import users_df # This import is now correct
import uuid

users_bp = Blueprint('users', __name__, template_folder='../../templates/users')

# --- AUTHENTICATION ROUTES ---

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('users.dashboard'))

    if request.method == 'POST':
        # MODIFIED: Get form data and strip any extra whitespace
        email_from_form = request.form.get('email', '').strip()
        password_from_form = request.form.get('password', '').strip()

        # MODIFIED: Perform a case-insensitive search for the user by converting both to lowercase
        user_record = users_df[users_df['Email'].str.lower() == email_from_form.lower()]

        if not user_record.empty:
            # User found, now check the password (this should be case-sensitive)
            user_data = user_record.iloc[0]
            if user_data['Password'] == password_from_form:
                # Password matches, log them in
                session['logged_in'] = True
                session['user'] = user_data.to_dict()
                flash('Login successful!', 'success')
                return redirect(url_for('users.dashboard'))

        # If we reach here, either user was not found or password was wrong
        flash('Invalid email or password. Please try again.', 'danger')
        
    return render_template('login.html')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    global users_df
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        role = request.form.get('role', 'customer')

        # Check if user already exists
        if not users_df[users_df['Email'].str.lower() == email.lower()].empty:
            flash('An account with this email already exists.', 'danger')
            return render_template('register.html')

        new_user_id = users_df['UserID'].max() + 1
        new_user = pd.DataFrame([{
            'UserID': new_user_id,
            'Username': username,
            'Email': email,
            'Password': password,
            'Role': role
        }])
        
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        # In a real app, you would save this back to the Excel/DB
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('users.login'))
        
    return render_template('register.html')

@users_bp.route('/logout')
def logout():
    """Logs the user out."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/dashboard')
def dashboard():
    """Displays the user's dashboard."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('You must be logged in to view the dashboard.', 'warning')
        return redirect(url_for('users.login'))
    return render_template('dashboard.html')

# --- USER MANAGEMENT (CRUD) ROUTES ---
# Kept for admin functionality, but not the focus of the fix

@users_bp.route('/')
def list_users():
    """Renders a page listing all users from the DataFrame."""
    if 'user' not in session or session['user'].get('Role') != 'admin':
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('products.all_products'))
        
    user_list = users_df.to_dict(orient='records')
    return render_template('users.html', users=user_list)

@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    """Adds a new user to the DataFrame."""
    global users_df
    if request.method == 'POST':
        # Logic to add a user
        pass
    return render_template('add_user.html')

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edits an existing user."""
    global users_df
    # Logic to edit a user
    pass

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Deletes a user from the DataFrame."""
    global users_df
    # Logic to delete a user
    pass

