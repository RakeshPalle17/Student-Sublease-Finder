from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db, photos
from app.models import Listing

main = Blueprint('main', __name__)

@main.route('/listings', methods=['GET'])
def get_listings():
    university = request.args.get('university')
    location = request.args.get('location')

    query = Listing.query
    if university:
        query = query.filter_by(university=university)
    if location:
        query = query.filter(Listing.location.contains(location))

    listings = query.all()
    return jsonify([{
        'id': listing.id,
        'title': listing.title,
        'description': listing.description,
        'rent': listing.rent,
        'utilities': listing.utilities,
        'location': listing.location,
        'university': listing.university
    } for listing in listings])


@main.route('/listings', methods=['POST'])
@jwt_required()
def add_listing():
    current_user = get_jwt_identity()
    data = request.form  # Use form data to handle file upload
    file = request.files.get('photo')  # Retrieve the uploaded file

    photo_filename = None
    if file:
        photo_filename = photos.save(file)  # Save the file
        photo_filename = photos.path(photo_filename)  # Get the file path

    new_listing = Listing(
        title=data['title'],
        description=data['description'],
        rent=data['rent'],
        utilities=data.get('utilities'),
        location=data['location'],
        university=data['university'],
        photos=photo_filename,
        user_id=current_user['id']
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({'message': 'Listing created successfully!'}), 201

@main.route('/listings/<int:id>', methods=['PUT'])
@jwt_required()
def update_listing(id):
    current_user = get_jwt_identity()
    listing = Listing.query.get_or_404(id)

    if listing.user_id != current_user['id']:
        return jsonify({'error': 'You are not authorized to edit this listing'}), 403

    data = request.form  # Use form data to handle file upload
    file = request.files.get('photo')

    photo_filename = None
    if file:
        photo_filename = photos.save(file)
        photo_filename = photos.path(photo_filename)

    listing.title = data['title']
    listing.description = data['description']
    listing.rent = data['rent']
    listing.utilities = data.get('utilities')
    listing.location = data['location']
    listing.university = data['university']
    if photo_filename:
        listing.photos = photo_filename

    db.session.commit()
    return jsonify({'message': 'Listing updated successfully!'})

@main.route('/listings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_listing(id):
    current_user = get_jwt_identity()
    listing = Listing.query.get_or_404(id)

    if listing.user_id != current_user['id']:
        return jsonify({'error': 'You are not authorized to delete this listing'}), 403

    db.session.delete(listing)
    db.session.commit()
    return jsonify({'message': 'Listing deleted successfully!'})
