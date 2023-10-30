#!/usr/bin/python3
"""Place - Amenity"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place, place_amenity
from models.amenity import Amenity


r = '/places/<place_id>/amenities'


@app_views.route(r, methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Retrieve list of all Amenities objects based on place id"""
    amenities = storage.get(Place, place_id).amenities
    if amenities is None:
        abort(404)
    list_ameniy = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_ameniy)


@app_views.route(r + '/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """delete amenity objects based on place id"""
    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                storage.delete(amenity)
                break
        storage.save()
        return jsonify({}), 200


@app_views.route(r + '/<amenity_id>', methods=['POST'], strict_slashes=False)
def add_amenity(place_id, amenity_id):
    """post objects"""
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        if amenity is None:
            abort(404)

        place.amenities.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
