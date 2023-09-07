from flask import Blueprint, request, jsonify
from app.models import Court
from app import db

courts_bp = Blueprint('courts', __name__)

# Route to get all courts (requires authentication)
@courts_bp.route('/courts', methods=['GET'])
def get_courts():
    courts = Court.query.all()
    court_list = [{"id": court.id, "name": court.name, "address": court.address} for court in courts]
    return jsonify(court_list)

# Route to get a single court by ID (requires authentication)
@courts_bp.route('/courts/<int:court_id>', methods=['GET'])
def get_court(court_id):
    court = db.session.get(Court, court_id)  # Use Session.get() instead of Query.get()
    if court:
        court_data = {
            "id": court.id,
            "name": court.name,
            "address": court.address,
            "is_public": court.is_public,
            "image_url": court.image_url,
            "number_of_courts": court.number_of_courts,
            "hours_of_operation": [{"day_of_week": h.day_of_week, "opening_time": str(h.opening_time), "closing_time": str(h.closing_time)} for h in court.hours_of_operation]
        }
        return jsonify(court_data)
    return jsonify({"error": "Court not found"}), 404  # Return a 404 Not Found for missing court

@courts_bp.route('/courts', methods=['POST'])
def create_court():
    # Get the request data
    data = request.get_json()
    
    # Extract the court information from the request data
    court_data = {
        "name": data.get("name"),
        "address": data.get("address"),
        "is_public": data.get("is_public"),
        "image_url": data.get("image_url"),
        "number_of_courts": data.get("number_of_courts"),
    }
    
    # Create a new court using the extracted data
    court = Court(**court_data)
    
    # Add the court to the database
    db.session.add(court)
    db.session.commit()
    
    # Return a success message
    return jsonify({"message": "Court created successfully"})
