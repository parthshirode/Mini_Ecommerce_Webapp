from flask import Flask, session, redirect, url_for, render_template
import pandas as pd
import os

# --- Data Loading and Cleaning ---
# Load data from Excel sheets into pandas DataFrames
try:
    excel_file = 'data.xlsx'
    users_df = pd.read_excel(excel_file, sheet_name='Users', dtype={'Password': str})
    products_df = pd.read_excel(excel_file, sheet_name='Products')
    orders_df = pd.read_excel(excel_file, sheet_name='Orders')

    # Data Cleaning: Remove leading/trailing whitespace from crucial columns
    if 'Email' in users_df.columns:
        users_df['Email'] = users_df['Email'].str.strip()
    if 'Password' in users_df.columns:
        users_df['Password'] = users_df['Password'].str.strip()

except FileNotFoundError:
    print(f"Error: The data file '{excel_file}' was not found. Please ensure it is in the same directory as app.py.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the Excel file: {e}")
    exit()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_super_secret_key' # Change this in a real application

    # --- Main Redirect Route ---
    @app.route('/')
    def index():
        # This now redirects the root URL to the login page.
        return redirect(url_for('users.login'))

    # Import and register blueprints inside the factory
    from routes.users.users import users_bp
    from routes.products.products import products_bp
    from routes.orders.orders import orders_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

