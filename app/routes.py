from flask import Blueprint, request, jsonify
from .models import Apartment
from .database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import apartment_schema

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/apartments', methods=['GET'])
def list_apartments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    university = request.args.get('university')
    location = request.args.get('location')

    query = Apartment.query
    if university:
        query = query.filter_by(university_name=university)
    if location:
        query = query.filter_by(location=location)

    apartments = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "apt_id": apt.id,
            "description": apt.description,
            "location": apt.location,
            "rent": apt.rent,
            "title": apt.title,
            "utilities": apt.utilities,
            "university_name": apt.university_name,
            "photos": apt.photos,
            "contact": apt.contact,
            "user_id": apt.user_id
        } for apt in apartments
    ]
    return jsonify({"apartments": result, "total": apartments.total, "pages": apartments.pages}), 200


@auth_bp.route('/apartments', methods=['POST'])
@jwt_required()
def add_apartment():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    errors = apartment_schema.validate(data)
    if errors:
        print(f"Validation errors: {errors}")
        return jsonify({"errors": errors}), 400

    try:
        new_apartment = Apartment(
            description=data['description'],
            location=data['location'],
            rent=data['rent'],
            title=data['title'],
            utilities=data.get('utilities', ''),
            university_name=data['university_name'],
            photos=data.get('photos', ''),
            contact=data['contact'],
            user_id=current_user_id
        )

        db.session.add(new_apartment)
        db.session.commit()

        return jsonify({"message": "Apartment added successfully"}), 201
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Could not add apartment"}), 500