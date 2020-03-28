from flask import Flask, jsonify, request
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict

from src.rest_api.db.config import default_page, default_limit, DEFAULTS
from src.rest_api.db.data_access import get_all_data
from flasgger import Swagger

app = Flask(__name__)

CORS(app)
Swagger(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/all_accts')
def data():
    """Returns all data
    ---
    responses:
      200:
        description: A list of accrs
    """
    return jsonify(get_all_data())


@app.route('/accts')
def data_paginated():
    """Returns all data
    ---
    parameters:
      - in: query
        name: page
        type: integer
        description: Page number
      - in: query
        name: limit
        type: integer
        description: The numbers of items in page
    responses:
      200:
        description: A list of accrs paginated
    """

    posted_json = request.json

    page = posted_json.get("page", DEFAULTS['page'])
    limit = posted_json.get("limit", DEFAULTS['limit'])
    ip_src_in = posted_json.get("ip_src_in", DEFAULTS['ip_src_in'])
    packets_between = posted_json.get("packets_between", DEFAULTS['packets_between'])
    bytes_between = posted_json.get("bytes_between", DEFAULTS['bytes_between'])
    stamp_between = posted_json.get("stamp_between", DEFAULTS['stamp_between'])


    return jsonify(get_filtered_data(page, limit, ip_src_in, packets_between, bytes_between, stamp_between))


if __name__ == '__main__':
    app.run(debug=True)
