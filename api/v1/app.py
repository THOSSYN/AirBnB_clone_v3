#!/usr/bin/python3
"""A script that starts a flask application"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(Exception):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """handling error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'), threaded=True)
