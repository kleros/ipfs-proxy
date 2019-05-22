# Kleros IPFS Proxy

Kleros hosts an IPFS node so that we can pin files that are submitted through our UI's.
Sometimes our UI's need to make api calls to our node. Instead of opening up the entire
IPFS api to the world we run this proxy in front to make the calls for us.

## Quickstart

- (Recommended) Install a `virtualenv` using Python 3.x.

- `pip install -r requirements.txt`

- python server.py

## Routes

- Add files to IPFS. By default it will pin the file and use a directory to preserve filename and extension.

`POST /add`

Expects a JSON body that includes:
```
{
  fileName: <string>,
  buffer: <[]int>
}
```

Returns:
```
[{
  path: string,
  hash: string
}]
```

- Fetch a file from the node.

`GET /ipfs/<path>`
