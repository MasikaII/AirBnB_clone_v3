#!/usr/bin/python3
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def create_list_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        states = storage.all(State)
        return jsonify([state.to_dict() for state in states.values()])

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get("name") is None:
            abort(400, 'Missing name')
        new_state = state(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def update_delete_states():
    """Updates or Deletes a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, value in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, value)
                state.save()
                return jsonify(state.to_dict()), 200
