#!/usr/bin/python3
"""A script that creates view for amenity object"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Renders all amenities view"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Displays an endpoint for one amenity by id"""
    per_amenity = storage.get(Amenity, amenity_id)

    if per_amenity is None:
        abort(404)

    if per_amenity.id == amenity_id:
        return jsonify(per_amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes an amenity by its id"""
    per_amenity = storage.get(Amenity, amenity_id)
    
    if per_amenity is None:
        abort(404)
    
    storage.delete(per_amenity)
    storage.save()

    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an additional amenity"""
    data = request.get_json()

    if 'name' not in data:
        return ("Missing name"), 400

    if not request.is_json:
        return ("Not a JSON"), 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an amenity instance"""
    per_amenity = storage.get(Amenity, amenity_id)

    if per_amenity is None:
        return jsonify({'error': 'Not found'}), 404

    put_args = request.get_json()

    if not request.is_json:
        return ("Not a JSON"), 400

    for key, value in put_args.items():
        if not key in ['id', 'created_at', 'updated_at']:
            setattr(per_amenity, key, value)
    storage.save()
    return jsonify(per_amenity.to_dict())
