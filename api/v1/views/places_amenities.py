#!/usr/bin/python3
"""Place - Amenity"""
from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


r = '/places/<place_id>/amenities'


@app_views.route(r, methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Retrieve list of all Amenities objects based on place id"""
    amenities = storage.get(Place, place_id).amenities
    if amenities is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        list = [amenity.to_dict() for amenity in amenities]
    else:
        list = [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
    return jsonify(list)


@app_views.route(r + '/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """delete amenity objects based on place id"""
    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                abort(404)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            i = place.amenity_ids.index(amenity_id)
            place.amenity_ids.pop(i)
        amenity.delete()
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
        if amenity is None:
            abort(404)

        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
