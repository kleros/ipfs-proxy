import ipfshttpclient
import requests
import os

# connect to local node
api = ipfshttpclient.connect(os.environ['IPFS_API_ENDPOINT'])


def add_file(file_path, pin=True, wrap_with_directory=True):
    res = api.add(file_path, wrap_with_directory=wrap_with_directory, pin=pin)
    return res

gateway_endpoint = os.environ['IPFS_GATEWAY_ENDPOINT'];
gateway_timeout = os.getenv('IPFS_GATEWAY_TIMEOUT', 30);

def cat_file(file_path):
    res = requests.get('%s/ipfs/%s' % (gateway_endpoint, file_path), timeout=gateway_timeout)
    return res
