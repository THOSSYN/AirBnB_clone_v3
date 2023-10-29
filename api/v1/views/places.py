#!/usr/bin/python3
"""A script that creates a place view"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Displays a list of places"""
    if request.method == 'GET':
        city = storage.get(City, city_id)

        if city is None:
            return jsonify({'error': 'Not found'}), 404

        return jsonify([item.to_dict() for item in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_by_id(place_id):
    """Displays a list of places"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)

        if place is None:
            return jsonify({'error': 'Not found'}), 404

        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_by_id(place_id):
    """Displays a list of places"""
    if request.method == 'DELETE':
        place = storage.get(Place, place_id)

        if place is None:
            return jsonify({'error': 'Not found'}), 404

        storage.delete(place)
        storage.save()

        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_places(city_id):
    """Creates a place instance"""
    if request.method == 'POST':
        city_for_place = storage.get(City, city_id)
        post_args = request.get_json()

        if city_for_place is None:
            return jsonify({'error': 'Not found'}), 404

        if not request.get_json():
            return ("Not a JSON"), 400

        if 'user_id' not in post_args:
            return ("Missing user_id"), 400

        if 'name' not in post_args:
            return ("Missing name"), 400

        user_id = post_args['user_id']
        user = storage.get(User, user_id)

        if user is None:
            return jsonify({'error': 'Not found'}), 400

        new_place = Place(**post_args)
        new_place.city_id = city_id
        storage.new(new_place)
        storage.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """Displays a list of places"""
    if request.method == 'PUT':
        place = storage.get(Place, place_id)

        if place is None:
            return jsonify({'error': 'Not found'}), 404

        if not request.is_json:
            return ("Not a JSON"), 400

        put_args = request.get_json()
        if put_args is None:
            return ("Not a JSON"), 400

        for key, value in put_args.items():
            if not key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200
