from flask import Flask, Blueprint, request, jsonify, send_from_directory
from app.models import Item
from app import db  # Import db directly from app/__init__.py

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def get_items():
    items = Item.query.all()
    item_list = [{"id": item.id, "name": item.name} for item in items]
    return jsonify(item_list)

@main_bp.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()  # Expect JSON data in the request body
    name = data.get('name')
    if name:
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item added successfully"})
    return jsonify({"error": "Invalid input"}), 400  # Return a 400 Bad Request for invalid input

@main_bp.route('/images/<path:filename>')
def serve_image(filename):
    # Construct the path to the image in your static directory
    image_path = os.path.join(app.root_path, 'static', 'images', filename)
    # Serve the image
    return send_file(image_path)