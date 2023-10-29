#!/usr/bin/python3
"""A script that display city objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state_id(state_id):
    """Retrieves the cities of that state_id"""
    if request.method == 'GET':
        state = storage.get(State, state_id)

        if state is None:
            abort(404)

        city_dict = [city.to_dict() for city in state.cities]
        return jsonify(city_dict)

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities_by_city_id(city_id):
    """Retrieves a city object by its city_id"""
    if request.method == 'GET':
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities_by_id(city_id):
    """Retrieves the cities of that state_id"""
    if request.method == 'DELETE':
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        storage.delete(city)
        storage.save()
    
        return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_cities_by_id(state_id):
    """Creates a cities for a state"""
    if request.method == 'POST':
        state = storage.get(State, state_id)

        if state is None:
            abort(404)

        post_data = request.get_json()
        if 'name' not in post_data:
            return ("Missing name"), 400

        if post_data is None:
            return ("Not a JSON"), 400

        post_data['state_id'] = state_id

        new_city = City(**post_data)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_cities_by_id(city_id):
    """Updates a city with a city_id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    put_data = request.get_json()
    if put_data is None:
        return ("Not a JSON"), 400

    if put_data:
        for key, value in put_data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                storage.save()
        return jsonify(city.to_dict()), 200
    else:
        return jsonify(city.to_dict()), 200
