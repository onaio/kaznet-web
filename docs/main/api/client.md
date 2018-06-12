# Clients

This API endpoint follows the [JSON API](http://jsonapi.org/) structure.

Adds ability to create, list, update, delete and retrieve a Client.

Once a Client is created it's stored in the database and can be retrieved from the API as shown below. **To Use this API Endpoint User must be an Admin**

## API Endpoints

### POST /api/v1/clients/

Creates a new client, requires `name`

```console
curl -X POST -H "Content-type:application/vnd.api+json" -d '{"data":{"type":"Client","id":null,"attributes":{"name":"Knights Order"}}}' https://example.com/api/v1/clients/
```

Returns the client that was created:

```json
{
    "data": {
        "type": "Client",
        "id": "4",
        "attributes": {
            "name": "Knights Order"
        }
    }
}
```

### GET /api/v1/clients/

Returns a list of all clients.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" https://example.com/api/v1/clients/
```

```json
{
    "links": {
        "first": "https://example.com/api/v1/clients/?page=1",
        "last": "https://example.com/api/v1/clients/?page=1",
        "next": null,
        "prev": null
    },
    "data": [{
        "type": "Client",
        "id": "1",
        "attributes": {
            "name": "Knights Order"
        }
    }, {
        "type": "Client",
        "id": "2",
        "attributes": {
            "name": "Awesome Client"
        }
    }],
    "meta": {
        "pagination": {
            "page": 1,
            "pages": 1,
            "count": 2
        }
    }
}
```

Returns a list of clients with a specific name if given the `search` query parameter. The `search` query parameter takes a *string* which is the clients name.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/clients/?search=jolt"
```

Returns a list of clients ordered by client name if given the `ordering` query parameter. The `ordering` query parameter either takes `name` for ascending order or `-name` for descending order.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/clients/?ordering=-name"
```

### GET /api/v1/clients/[pk]/

Returns a specific client with matching pk.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/clients/2/"
```

This request will return a response containing data on the specific client.

```json
{
    "data": {
        "type": "Client",
        "id": "2",
        "attributes": {
            "name": "Knights Order"
        }
    }
}
```

### DELETE /api/v1/clients/[pk]/

Deletes a specific client with matching pk.

```console
curl -X DELETE -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/clients/12/"
```

### PATCH  /api/v1/clients/[pk]/

Partial updates a specific client with matching pk.

```console
curl -X PATCH -H "Content-Type:application/vnd.api+json" -d '{"data":{"type":"Client","id":3,"attributes":{"name":"Sun Order"}}}' "https://example.com/api/v1/clients/3/"
```
