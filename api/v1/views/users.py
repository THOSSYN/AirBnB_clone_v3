#!/usr/bin/python3
"""A script that creates view for amenity object"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Renders all users page"""
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Displays an endpoint for one user by id"""
    if request.method == 'GET':
        per_user = storage.get(User, user_id)

        if per_user is None:
            abort(404)

        #if per_user.id == user_id:
        return jsonify(per_user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a user by its id"""
    if request.method == 'DELETE':
        per_user = storage.get(User, user_id)
    
        if per_user is None:
            abort(404)
    
        storage.delete(per_user)
        storage.save()

        return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an additional user"""
    if request.method == 'POST':
        data = request.get_json()

        if 'email' not in data:
            return ("Missing email"), 400

        if 'password' not in data:
            return ("Missing password"), 400

        if data is None:
            return ("Not a JSON"), 400

        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a user instance"""
    per_user = storage.get(User, user_id)

    if per_user is None:
        return jsonify({'eeror': 'Not found'}), 404

    put_args = request.get_json()

    if put_args is None:
        return ("Not a JSON"), 400

    for key, value in put_args.items():
        if not key in ['id', 'email', 'created_at', 'updated_at']:
            setattr(per_user, key, value)
    storage.save()
    return jsonify(per_user.to_dict())
