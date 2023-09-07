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

# Add more routes for creating, updating, or deleting courts as needed (all requiring authentication)
# Example:
# @courts_bp.route('/courts', methods=['POST'])
# @login_required
# def create_court():
#     # Add code to create a new court here
