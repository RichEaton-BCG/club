from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Product, Order, OrderItem, db
import stripe


#stripe.api_key = current_app.config['STRIPE_SECRET_KEY']


bp = Blueprint('store', __name__, url_prefix='/store')

#@bp.before_app_first_request
#def initialize_stripe():
    #stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@bp.route('/')
def store():
    products = Product.query.all()
    return render_template('store/index.html', products=products)


@bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': product.price * quantity
            })
            total_price += product.price * quantity

    return render_template('store/cart.html', cart_items=cart_items, total_price=total_price)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart
    return redirect(url_for('store.cart'))


@bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('store.cart'))

    line_items = []
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product and product.stripe_price_id:
            line_items.append({
                'price': product.stripe_price_id,
                'quantity': quantity
            })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('store.success', _external=True),
            cancel_url=url_for('store.cart', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400

@bp.route('/order_summary/<int:order_id>')
def order_summary(order_id):
    order = Order.query.get(order_id)
    return render_template('store/order_summary.html', order=order)


@bp.route('/success')
def success():
    session.pop('cart', None)  # Clear the cart
    return render_template('store/success.html', message="Your payment was successful!")
