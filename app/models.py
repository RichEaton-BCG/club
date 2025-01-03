from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_member = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(250), unique=False, nullable=False)
    lastname = db.Column(db.String(250), unique=False, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    postalcode = db.Column(db.String(10), nullable=False)
    skill_ranking = db.Column(db.String(2), nullable = True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_played = db.Column(db.DateTime, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price in dollars
    description = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    # Stripe Price ID for Checkout integration
    stripe_price_id = db.Column(db.String(255), nullable=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)  # Nullable for guest orders
    total_price = db.Column(db.Float, nullable=False)
    # Pending, Completed, Failed
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # Price per unit at the time of order
    price = db.Column(db.Float, nullable=False)
