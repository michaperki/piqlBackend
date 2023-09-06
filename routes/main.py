from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Item  # Import the model from the app package

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@main_bp.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    if name:
        db = current_app.config['db']  # Access the db object using current_app
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('main.index'))
