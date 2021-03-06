from flask import Flask, jsonify, request
from flask_cors import CORS

from src.rest_api.db.config import DEFAULTS
from src.rest_api.db.data_access import (get_filtered_data, insert_class_of_ips, get_all_classes_of_ips,
                                         get_class_of_ips, delete_class_of_ips, edit_class_of_ips, get_aggregation)
from flasgger import Swagger

from src.rest_api.process.continuous_streams import find_continuous_streams

app = Flask(__name__)

CORS(app)
Swagger(app)


@app.route('/version', methods=['GET'])
def version():
    return "1.0"


@app.route('/classOfIps', methods=['POST'])
def insert_class_of_ips_api():
    """Define class of ips
        ---
        parameters:
          - in: body
            name: body
            schema:
              properties:
                name:
                  type: string
                  description: Name of defined class of ip
                  example: YouTube
                ips:
                  type: array
                  description: List of ips belonging to defined class
                  example: ['151.101.129.69', '111.222.222.111']
        responses:
          200:
            description: Ok code
    """
    posted_json = request.json
    class_of_ips_name = posted_json["name"]
    ips = posted_json["ips"]

    insert_class_of_ips(class_of_ips_name, ips)
    return "OK"


@app.route('/classOfIps', methods=['PUT'])
def edit_class_of_ips_api():
    """Update class of ips
        ---
        parameters:
          - in: body
            name: body
            schema:
              properties:
                name:
                  type: string
                  description: Name of updated class of ip
                  example: YouTube
                ips:
                  type: array
                  description: List of new ips belonging to defined class
                  example: ['111.222.222.111', '111.111.111.111']
        responses:
          200:
            description: Ok code
    """
    posted_json = request.json
    class_of_ips_name = posted_json["name"]
    ips = posted_json["ips"]

    edit_class_of_ips(class_of_ips_name, ips)
    return "OK"


@app.route('/classOfIps', methods=['GET'])
def get_class_of_ips_api():
    """Get class of ips
        ---
        parameters:
          - in: query
            name: name
            schema:
              properties:
                name:
                  type: string
                  description: Optional filter for name of class of ips. If empty then all classes are returned
                  example: test
        responses:
          200:
            description: List of classes of ip
    """
    optional_name = request.args.get('name')

    if optional_name is None:
        return jsonify(get_all_classes_of_ips())
    else:
        return jsonify(get_class_of_ips(optional_name))


@app.route('/classOfIps', methods=['DELETE'])
def remove_class_of_ips():
    """Delete class of ip
        ---
        parameters:
          - in: body
            name: body
            schema:
              properties:
                name:
                  type: string
                  description: Name of ip class to delete
                  example: test
        responses:
          200:
            description: Ok code
    """
    posted_json = request.json
    class_of_ips_name = posted_json["name"]
    delete_class_of_ips(class_of_ips_name)
    return "OK"


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
              description: Optional array for filtering just for specific ips. For example&#58; ['10.0.2.15'] or just a part of ip ['10.']
              example: ['10.0.2.15']
            ip_dst_in:
              type: array
              description: Optional array for filtering just for specific ips. For example&#58; ['151.101.129.69'] or just a part of ip ['151.1']
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
            incoming_outgoing_in:
              type: array
              description: Optional array for filtering just for specific direction (incoming or outgoing)
              example: ['incoming']
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

        "incoming_outgoing_in",
    ]

    kwargs = {arg_name: posted_json.get(arg_name, DEFAULTS[arg_name]) for arg_name in arg_names}

    return jsonify(get_filtered_data(kwargs))


@app.route('/accts_streams', methods=['POST'])
def accts_streams():
    """Returns streams in data filtered by optional parameters
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
            incoming_outgoing_in:
              type: array
              description: Optional array for filtering just for specific direction (incoming or outgoing)
              example: ['incoming']
    responses:
      200:
        description: A list of streams
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

        "incoming_outgoing_in",
    ]

    kwargs = {arg_name: posted_json.get(arg_name, DEFAULTS[arg_name]) for arg_name in arg_names}

    records = get_filtered_data(kwargs)

    streams = find_continuous_streams(records)

    return jsonify(streams)


@app.route('/accts_aggregates', methods=['POST'])
def accts_aggregates():
    """Get aggregated ip traffic data
        ---
        parameters:
          - in: body
            name: body
            schema:
              properties:
                aggregated_column:
                  type: string
                  description: Column which will be aggeregated (sumed, counted etc.)
                  example: bytes
                aggregate_func:
                  type: string
                  description: Name of aggregation function (sum, avg, count etc.)
                  example: sum
                aggregate_part:
                  type: string
                  description: How results should be grouped (defaults to 'day', but should be one of&#58; millennium century decade year quarter month week day hour minute second milliseconds microseconds (see more at&#58; https://www.postgresql.org/docs/9.1/functions-datetime.html)
                  example: day
                stamp_between:
                  type: array
                  description: Optional array for filtering for timestamps being in specific range. For example&#58; ['2020-03-27 21:02:01.000000', '2020-03-27 21:48:02.000000'] or ['2020-03-27 21:02:01.000000', null] (for no upper limit)
                  example: ['2020-03-27 21:02:01.000000', null]
        responses:
          200:
            description: Aggregated results. When using for example week or month in aggregate_part in the response key indicated the start of period (e. g. "Wed, 01 Apr 2020 00&#58;00&#58;00 GMT" means whole April month)
    """
    posted_json = request.json

    arg_names = ["aggregated_column", "aggregate_func", "aggregate_part", "stamp_between"]

    parameter_values = [posted_json.get(arg_name, DEFAULTS[arg_name]) for arg_name in arg_names]

    aggregation_results = get_aggregation(*parameter_values)
    return jsonify(aggregation_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
