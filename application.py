import os
from flask import Flask, jsonify, request
from tempfile import TemporaryDirectory
from ipfs import add_file, add_directory, cat_file
from requests.exceptions import ReadTimeout
from zipfile import ZipFile, BadZipFile

application = Flask(__name__)

def fetch_file(path):
    try:
        res = cat_file(path)
        if (res.status_code in [400, 404]):
            return jsonify({ 'error': res.content.decode('utf-8') }), res.status_code
        else:
            return res.content, res.status_code, res.headers.items()
    except ReadTimeout:
            return jsonify(error="Gateway timeout"), 504
    except:
            return jsonify(error="Unknown error"), 500

IPFS_HEALTH_CHECK_PATH = os.getenv('IPFS_HEALTH_CHECK_PATH')

@application.route('/health-check', methods=['GET'])
@application.route('/', methods=['GET'])
def health_check():
    return fetch_file(IPFS_HEALTH_CHECK_PATH)

@application.route('/add', methods=['POST'])
def add():
    # check if the post request has the file part
    requestJSON = request.json
    if not requestJSON.get("buffer") or not requestJSON.get("fileName"):
        return jsonify(error="Missing buffer and/or fileName in JSON body"), 400

    tmp_dir = TemporaryDirectory()
    tmp_file_path = os.path.join(tmp_dir.name, requestJSON["fileName"])

    # temporarily write to disk. Slow, get a workaround in ipfs api to pass straight bytes. FIXME
    new_file = open(tmp_file_path, "wb+")
    new_file.write(bytes(requestJSON["buffer"]["data"]))
    new_file.close() # close to write all in memory data to disk

    # add to ipfs
    hash = add_file(tmp_file_path)

    # remove tmp file
    tmp_dir.cleanup()

    return jsonify(data=list(map(lambda x: {"path": ("/%s" % x["Name"]), "hash": x["Hash"]}, hash))), 201

@application.route('/add-zipped-directory', methods=['POST'])
def add_zipped_directory():
    file = request.files['file']
    zipfile_obj = None

    try:
        zipfile_obj = ZipFile(file.stream._file)
    except BadZipFile:
        return jsonify(error="Invalid zip file"), 400
    except:
        return jsonify(error="Unknown error"), 500

    tmp_dir = TemporaryDirectory()
    dst_dir = os.path.join(tmp_dir.name, os.path.splitext(file.filename)[0])
    os.makedirs(dst_dir)

    zipfile_obj.extractall(dst_dir)

    # add to ipfs
    hash = add_file(dst_dir)

    # remove tmp file
    tmp_dir.cleanup()

    return jsonify(data=list(map(lambda x: {"path": ("/%s" % x["Name"]), "hash": x["Hash"]}, hash))), 201

@application.route('/ipfs/<path:path>', methods=['GET'])
def get(path):
    return fetch_file(path)

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
