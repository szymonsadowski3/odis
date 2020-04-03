from flask import Flask, jsonify, request
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict

from src.rest_api.db.config import DEFAULTS
from src.rest_api.db.data_access import get_all_data, get_filtered_data
from flasgger import Swagger

app = Flask(__name__)

CORS(app)
Swagger(app)


@app.route('/version', methods=['GET'])
def version():
    return "1.0"


@app.route('/accts', methods=['POST'])
def accts():
    """Returns all data
    ---
    parameters:
      - in: body
        name: body
        schema:
          properties:
            page:
              type: integer
              description: Page number
              example: 0
            limit:
              type: integer
              description: The numbers of items in page. If not provided then there is no limit at all
              example: 10
            ip_src_in:
              type: array
              description: Optional array for filtering just for specific ips. For example&#58; ['10.0.2.15']
              example: ['10.0.2.15']
            ip_dst_in:
              type: array
              description: Optional array for filtering just for specific ips. For example&#58; ['151.101.129.69']
              example: ['151.101.129.69']
            port_src_in:
              type: array
              description: Optional array for filtering just for specific ports. For example&#58; ['47718']
              example: ['47718']
            port_dst_in:
              type: array
              description: Optional array for filtering just for specific ports. For example&#58; ['443']
              example: ['443']
            ip_proto_in:
              type: array
              description: Optional array for filtering just for specific ip protocols (tcp or udp). For example&#58; ['tcp']
              example: ['tcp']
            mac_src_in:
              type: array
              description: Optional array for filtering just for specific mac addresses. For example&#58; ['52:54:00:12:35:02']
              example: ['52:54:00:12:35:02']
            mac_dst_in:
              type: array
              description: Optional array for filtering just for specific mac addresses. For example&#58; ['08:00:27:51:b8:cb']
              example: ['08:00:27:51:b8:cb']
            packets_between:
              type: array
              description: Optional array for filtering for packets being in specific range. For example&#58; [10, 200] or [200, null] (for no upper limit)
              example: [10, null]
            bytes_between:
              type: array
              description: Optional array for filtering for bytes being in specific range. For example&#58; [100, 2000] or [2000, null] (for no upper limit)
              example: [2000, null]
            stamp_between:
              type: array
              description: Optional array for filtering for timestamps being in specific range. For example&#58; ['2020-03-27 21:02:01.000000', '2020-03-27 21:48:02.000000'] or ['2020-03-27 21:02:01.000000', null] (for no upper limit)
              example: ['2020-03-27 21:02:01.000000', null]
    responses:
      200:
        description: A list of accts
    """

    posted_json = request.json

    arg_names = [
        "page",
        "limit",
        "ip_src_in",
        "ip_dst_in",
        "packets_between",
        "bytes_between",
        "stamp_between",

        "port_src_in",
        "port_dst_in",

        "ip_proto_in",
    ]

    kwargs = {arg_name: posted_json.get(arg_name, DEFAULTS[arg_name]) for arg_name in arg_names}


    return jsonify(get_filtered_data(kwargs))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
