import os

from flask import Flask, jsonify, request

from ipfs import add_file, cat_file

app = Flask(__name__)
TMP_FOLDER = './tmp'

@app.route('/add', methods=['POST'])
def add():
    # check if the post request has the file part
    requestJSON = request.json
    if not requestJSON.get("buffer") or not requestJSON.get("fileName"):
        return jsonify(error="Missing buffer and/or fileName in JSON body")

    tmp_file_path = os.path.join(TMP_FOLDER, requestJSON["fileName"])

    # temporarily write to disk. Slow, get a workaround in ipfs api to pass straight bytes. FIXME
    newFile = open(tmp_file_path, "wb")
    newFile.write(bytes(requestJSON["buffer"]["data"]))
    newFile.close() # close to write all in memory data to disk

    # add to ipfs
    hash = add_file(tmp_file_path)

    try:
        request.post('http://127.0.0.1:9094' + '/pins/' + hash["Hash"])
    except:
        pass

    # remove tmp file
    os.remove(tmp_file_path)

    return jsonify(data=list(map(lambda x: {"path": ("/%s" % x["Name"]), "hash": x["Hash"]}, hash))), 201

@app.route('/ipfs/<path:path>', methods=['GET'])
def get(path):
    resp = cat_file(path)
    return (resp.content, resp.status_code, resp.headers.items())


# CORS headers
@app.after_request
def after_request(response):
    if response.headers.get('Access-Control-Allow-Origin') is None:
        response.headers.add('Access-Control-Allow-Origin', "*")
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
