import os
from flask import Flask, jsonify, request
from tempfile import TemporaryDirectory
from ipfs import add_file, cat_file

application = Flask(__name__)

@application.route('/health-check', methods=['GET'])
@application.route('/', methods=['GET'])
def health_check():
    return jsonify({ 'status': 'OK' }), 200

@application.route('/add', methods=['POST'])
def add():
    # check if the post request has the file part
    requestJSON = request.json
    if not requestJSON.get("buffer") or not requestJSON.get("fileName"):
        return jsonify(error="Missing buffer and/or fileName in JSON body")

    tmp_dir = TemporaryDirectory()
    tmp_file_path = os.path.join(tmp_dir.name, requestJSON["fileName"])

    # temporarily write to disk. Slow, get a workaround in ipfs api to pass straight bytes. FIXME
    newFile = open(tmp_file_path, "wb+")
    newFile.write(bytes(requestJSON["buffer"]["data"]))
    newFile.close() # close to write all in memory data to disk

    # add to ipfs
    hash = add_file(tmp_file_path)

    # remove tmp file
    tmp_dir.cleanup()

    return jsonify(data=list(map(lambda x: {"path": ("/%s" % x["Name"]), "hash": x["Hash"]}, hash))), 201

@application.route('/ipfs/<path:path>', methods=['GET'])
def get(path):
    res = cat_file(path)
    return (res.content, res.status_code, res.headers.items())

# CORS headers
@application.after_request
def after_request(response):
    if response.headers.get('Access-Control-Allow-Origin') is None:
        response.headers.add('Access-Control-Allow-Origin', "*")
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

if __name__ == "__main__":
    port = os.getenv('PORT', 8000)
    application.run(debug=True, threaded=True, port=port, host="0.0.0.0")
