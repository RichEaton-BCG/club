from flask import Blueprint, render_template

bp = Blueprint('public', __name__, url_prefix='/')


@bp.route('/')
def home():
    return render_template('public/home.html')


@bp.route('/about')
def about():
    return render_template('public/about.html')
