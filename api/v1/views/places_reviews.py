#!/usr/bin/python3
"""A script that creates a place view"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from models.user import User
from models.review import Review


p = '/places/<place_id>'


@app_views.route(p + '/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Displays a list of reviews"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)

        if place is None:
            return jsonify({'error': 'Not found'}), 404

        return jsonify([item.to_dict() for item in place.reviews])


r = '/reviews/<review_id>'


@app_views.route(r, methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """Displays a review by id"""
    if request.method == 'GET':
        review = storage.get(Review, review_id)

        if review is None:
            return jsonify({'error': 'Not found'}), 404

        return jsonify(review.to_dict())


@app_views.route(r, methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a review by id"""
    if request.method == 'DELETE':
        review = storage.get(Review, review_id)

        if review is None:
            return jsonify({'error': 'Not found'}), 404

        storage.delete(review)
        storage.save()

        return jsonify({}), 200


@app_views.route(r + '/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review instance"""
    if request.method == 'POST':
        place_for_review = storage.get(Place, place_id)
        post_args = request.get_json()

        if place_for_review is None:
            return jsonify({'error': 'Not found'}), 404

        if post_args is None:
            return ("Not a JSON"), 400

        if 'user_id' not in post_args:
            return ("Missing user_id"), 400

        if 'text' not in post_args:
            return ("Missing text"), 400

        user_id = post_args['user_id']
        user = storage.get(User, user_id)

        if user is None:
            return jsonify({'error': 'Not found'}), 404

        new_review = Review(**post_args)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()

        return jsonify(new_review.to_dict()), 201


@app_views.route(r, methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    if request.method == 'PUT':
        review = storage.get(Review, review_id)

        if review is None:
            return jsonify({'error': 'Not found'}), 404

        put_args = request.get_json()
        # if not request.is_json:
        # return ("Not a JSON"), 400

        if put_args is None:
            return("Not a JSON"), 400

        all_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in put_args.items():
            if key not in all_keys:
                setattr(review, key, value)

        storage.save()
        return jsonify(review.to_dict()), 200
