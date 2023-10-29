#!/usr/bin/python3
"""A script that creates a place view"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from models.user import User
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Displays a list of reviews"""
    place = storage.get(Place, place_id)

    if place is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify([item.to_dict() for item in place.reviews])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """Displays a review by id"""
    review = storage.get(Review, review_id)

    if review is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a review by id"""
    review = storage.get(Review, review_id)

    if review is None:
        return jsonify({'error': 'Not found'}), 404

    storage.delete(review)
    storage.save()

    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review instance"""
    place_for_review = storage.get(Place, place_id)
    post_args = request.get_json()

    if place_for_review is None:
        return jsonify({'error': 'Not found'}), 404

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in post_args:
        return jsonify({'error': 'Missing user_id'}), 400

    if 'text' not in post_args:
        return jsonify({'error': 'Missing text'}), 400

    user_id = post_args['user_id']
    user = storage.get(User, user_id)

    if user is None:
        return jsonify({'error': 'Not found'}), 400

    new_review = Review(**post_args)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)

    if review is None:
        return jsonify({'error': 'Not found'}), 404

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    put_args = request.get_json()
    if not put_args:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in put_args.items():
        if not key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
