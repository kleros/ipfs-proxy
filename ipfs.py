import ipfsapi
import requests

# connect to local node
api = ipfsapi.connect('127.0.0.1', 5001)

def add_file(file_path, pin=True, wrap_with_directory=True):
    res = api.add(file_path, wrap_with_directory=wrap_with_directory, pin=pin)
    return res

def cat_file(file_path):
    resp = requests.get('http://localhost:8080/ipfs/%s' % file_path)
    return resp
