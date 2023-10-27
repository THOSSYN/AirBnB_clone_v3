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

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Retrieves a State object """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        state_json = state.to_dict()
        return jsonify(state_json)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object """
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({})
