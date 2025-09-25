from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from app import products_df, orders_df # Import products_df as well
import pandas as pd
from datetime import datetime

orders_bp = Blueprint('orders', __name__, template_folder='templates')

# --- Order History Page ---
@orders_bp.route('/')
def list_orders():
    """Displays a list of orders based on the user's role."""
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))

    user_role = session['user']['Role']
    user_id = session['user']['UserID']
    
    # Merge orders with products to get product details like name and price
    # This is the key step to make all data available
    merged_df = pd.merge(orders_df, products_df, on='ProductID', how='left')
    
    # Calculate TotalPrice for each order
    merged_df['TotalPrice'] = merged_df['Quantity'] * merged_df['Price']

    if user_role == 'customer':
        user_orders = merged_df[merged_df['UserID'] == user_id]
    elif user_role == 'seller':
        user_orders = merged_df[merged_df['SellerID'] == user_id]
    elif user_role == 'admin':
        user_orders = merged_df
    else:
        user_orders = pd.DataFrame() # Empty dataframe for unknown roles

    orders_list = user_orders.to_dict(orient='records')
    
    # FIX: Specify the correct template path
    return render_template('orders/orders.html', orders=orders_list, role=user_role)


# --- Shopping Cart Logic ---

@orders_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)

    # Add item or increment quantity
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session.modified = True
    flash('Product added to cart!', 'success')
    return redirect(url_for('products.all_products'))

@orders_bp.route('/cart')
def view_cart():
    if 'cart' not in session or not session['cart']:
        return render_template('orders/cart.html', cart_items=[], total_price=0)

    cart_product_ids = [int(pid) for pid in session['cart'].keys()]
    cart_products_df = products_df[products_df['ProductID'].isin(cart_product_ids)].copy()
    
    cart_items = cart_products_df.to_dict('records')
    total_price = 0

    for item in cart_items:
        product_id_str = str(item['ProductID'])
        item['quantity'] = session['cart'][product_id_str]
        item['subtotal'] = item['Price'] * item['quantity']
        total_price += item['subtotal']
        
    return render_template('orders/cart.html', cart_items=cart_items, total_price=total_price)


@orders_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    product_id_str = str(product_id)
    if 'cart' in session and product_id_str in session['cart']:
        session['cart'].pop(product_id_str)
        session.modified = True
        flash('Item removed from cart.', 'info')
    return redirect(url_for('orders.view_cart'))


@orders_bp.route('/checkout', methods=['POST'])
def checkout():
    global orders_df
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('orders.view_cart'))

    user_id = session['user']['UserID']
    
    new_orders = []
    for product_id_str, quantity in session['cart'].items():
        new_order = {
            'OrderID': orders_df['OrderID'].max() + 1 + len(new_orders),
            'UserID': user_id,
            'ProductID': int(product_id_str),
            'Quantity': quantity,
            'OrderDate': datetime.now().strftime('%Y-%m-%d')
        }
        new_orders.append(new_order)
    
    new_orders_df = pd.DataFrame(new_orders)
    orders_df = pd.concat([orders_df, new_orders_df], ignore_index=True)
    
    # Clear the cart
    session.pop('cart', None)
    
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('orders.list_orders'))

