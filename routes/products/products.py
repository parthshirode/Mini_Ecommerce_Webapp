from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from app import products_df
import pandas as pd

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/', methods=['GET', 'POST'])
def all_products():
    """
    Handles both displaying the products list (GET) and
    processing the add/edit product forms (POST).
    """
    global products_df
    
    # Handle the 'Add Product' form submission
    if request.method == 'POST' and 'add_product' in request.form:
        if session.get('user') and session['user']['Role'] in ['admin', 'seller']:
            new_id = products_df['ProductID'].max() + 1
            new_product = {
                'ProductID': new_id,
                'Name': request.form['name'],
                'Price': float(request.form['price']),
                'Stock': int(request.form['stock']),
                'SellerID': session['user']['UserID']
            }
            new_product_df = pd.DataFrame([new_product])
            products_df = pd.concat([products_df, new_product_df], ignore_index=True)
            flash('New product added successfully!', 'success')
        else:
            flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('products.all_products'))

    # Prepare data for displaying the page (GET request)
    product_list = products_df.to_dict(orient='records')
    product_to_edit = None
    
    if 'edit' in request.args:
        try:
            edit_id = int(request.args.get('edit'))
            product_series = products_df[products_df['ProductID'] == edit_id].iloc[0]
            product_to_edit = product_series.to_dict()
        except (ValueError, IndexError):
            flash('Product not found for editing.', 'error')

    return render_template('products/products.html', products=product_list, product_to_edit=product_to_edit)


@products_bp.route('/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    global products_df
    if session.get('user') and session['user']['Role'] in ['admin', 'seller']:
        # Find the index of the product to edit
        product_index = products_df.index[products_df['ProductID'] == product_id].tolist()
        if product_index:
            idx = product_index[0]
            # Update the DataFrame at the specific index
            products_df.at[idx, 'Name'] = request.form['name']
            products_df.at[idx, 'Price'] = float(request.form['price'])
            products_df.at[idx, 'Stock'] = int(request.form['stock'])
            flash('Product updated successfully!', 'success')
        else:
            flash('Product not found.', 'error')
    else:
        flash('You are not authorized to perform this action.', 'error')
    return redirect(url_for('products.all_products'))


@products_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products_df
    if session.get('user') and session['user']['Role'] in ['admin', 'seller']:
        products_df = products_df[products_df['ProductID'] != product_id]
        flash('Product deleted successfully!', 'success')
    else:
        flash('You are not authorized to perform this action.', 'error')
    return redirect(url_for('products.all_products'))

