from flask import Flask, request, jsonify, make_response
import time

app = Flask(__name__)

protocols = []


@app.errorhandler(404)
def handle_404_path_not_savedd():
    response = jsonify({'error': 'Path not found'})
    response.status_code = 404
    return response


@app.errorhandler(400)
def abort_if_path_is_none():
    response = jsonify({'error': 'path is required'})
    response.status_code = 400
    return response


@app.errorhandler(400)
def abort_if_path_already_exists():
    response = jsonify({'error': 'path already saved'})
    response.status_code = 400
    return response


@app.route("/set_response", methods=["GET"])
def set_response():
    path = request.args.get("path", default=None, type=str)
    state = request.args.get("state", default=200, type=int)
    content = request.args.get("content", default="", type=str)
    if path is None:

        return abort_if_path_is_none()
    else:
        for p in protocols:
            if p['path'] == path:
                return abort_if_path_already_exists()
    timestamp = int(time.time())
    protocols.append({'path': path, 'content': content, 'state': state, 'timestamp': timestamp, 'parameters': ""})
    response = make_response('')
    return response


@app.route("/<path:urlpath>", methods=["GET", "POST"])
def get_paths(urlpath='/'):
    urlpath = '/' + urlpath
    protocol = {}

    for p in protocols:
        if p['path'] == urlpath:
            protocol = p

    if protocol:

        if protocol['content'] != "":
            response = make_response(protocol['content'])

        else:
            response = make_response('')
        response.status_code = protocol['state']

        parameters = request.args.items()
        if parameters:
            protocol['parameters'] = [{item[0]: item[1]} for item in parameters]
        return response

    else:
        return handle_404_path_not_savedd()


@app.route("/protocol", methods=["GET"])
def get_protocol():
    list_paths = []
    response_json = {}
    for p in protocols:
        response_json['request'] = {'path': p['path'], 'timestamp': p['timestamp'], 'parameters': p['parameters']}
        response_json['response'] = {'state': p['state'], 'content': p['content']}
        list_paths.append(response_json)
    response = make_response(list_paths)
    return response
