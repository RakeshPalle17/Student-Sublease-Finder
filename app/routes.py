from flask import Blueprint, request, jsonify
from .models import Apartment
from .database import db

auth_bp = Blueprint('bp', __name__)

@auth_bp.route('/apartments', methods=['GET'])
def list_apartments():
    university = request.args.get('university')
    location = request.args.get('location')

    query = Apartment.query
    if university:
        query = query.filter_by(university_name=university)
    if location:
        query = query.filter_by(location=location)

    apartments = query.all()
    result = [
        {
            "id": apt.id,
            "description": apt.description,
            "location": apt.location,
            "rent": apt.rent,
            "title": apt.title,
            "utilities": apt.utilities,
            "university_name": apt.university_name,
            "photos": apt.photos,
            "contact": apt.contact
        } for apt in apartments
    ]
    return jsonify(result), 200

@auth_bp.route('/apartments', methods=['POST'])
def add_apartment():
    data = request.get_json()
    new_apartment = Apartment(
        id=data['id'],
        description=data['description'],
        location=data['location'],
        rent=data['rent'],
        title=data['title'],
        utilities=data['utilities'],
        university_name=data['university_name'],
        photos=data['photos'],
        contact=data['contact']
    )
    
    db.session.add(new_apartment)
    db.session.commit()
    
    return jsonify({"message": "Apartment added successfully"}), 201