#!/usr/bin/python3
"""A script that display an index page with status"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'],  strict_slashes=False)
def status():
    """ return the status of your API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by typ"""
    new_dict = {}
    for cls, value in classes.items():
        new_dict[cls] = storage.count(value)
    return jsonify(new_dict)
