# Kleros IPFS Proxy

Kleros hosts an IPFS node so that we can pin files that are submitted through our UI's.
Sometimes our UI's need to make api calls to our node. Instead of opening up the entire
IPFS api to the world we run this proxy in front to make the calls for us.

## Quickstart

- (Recommended) Install a `virtualenv` using Python 3.x.
- `pip install -r requirements.txt`
- `python application.py`

## Routes

### `POST /add`

Add files to IPFS. By default it will pin the file and use a directory to preserve filename and extension.

#### Request Body

Expects a JSON body that includes:

```typescript
{
  fileName: string,
  buffer: Buffer
}
```

#### Response Body

```typescript
{
  data: [
    {
      path: string,
      hash: string
    },
    {
      path: "/",
      hash: string
    }
  ]
}
```

### `GET /ipfs/<path>`

Fetch a file from the node.

#### Response Body

The contents of the file.


### `POST /add-zipped-directory` (experimental)

Adds a zipped directory to IPFS. It will extract the zip file into a folder with the same name and upload it.

#### Request Body

Expects a `multipart/form-data` body with a `file` field:

```typescript
----FormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="<filename>.zip"
Content-Type: application/zip

(data)
----FormBoundary7MA4YWxkTrZu0gW
```

#### Response Body

```typescript
{
  data: [
    ...
    {
      path: string,
      hash: string
    },
    {
      path: "/",
      hash: string
    }
  ]
}
```

