from flask import Flask, jsonify
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict

from src.rest_api.db.data_access import get_all_data

app = Flask(__name__)

CORS(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/data')
def data():
    return jsonify(get_all_data())


if __name__ == '__main__':
    app.run(debug=True)
