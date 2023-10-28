#!/usr/bin/python3
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        states = storage.all(State).values()
        list_states = [state.to_dict() for state in states]
        return jsonify(list_states)


s_route = '/states/<state_id>'


@app_views.route(s_route, methods=['GET'], strict_slashes=False)
def state(state_id):
    """Retrieves a State object """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        state_json = state.to_dict()
        return jsonify(state_json)


@app_views.route(s_route, methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object """
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ Post a State object """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()

        if data is None:
            return ("Not a JSON"), 400
        if 'name' not in data:
            return ("Missing name"), 400
        # unpack the dictionary data
        new_state = State(**data)
        # add new object to the database
        storage.new(new_state)
        # save new_object
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        return "Not a JSON", 400


@app_views.route(s_route, methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object """
    state = storage.get(State, state_id)
    data = request.get_json()

    if state is None:
        abort(404)
    if data is None:
        return ("Not a JSON"), 400
    # Update the state object with the data
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
