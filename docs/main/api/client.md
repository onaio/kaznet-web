# Clients

Adds ability to create, list, update, delete and retrieve a Client.

Once a Client is created it's stored in the database and can be retrieved from the API as shown below. **To Use this API Endpoint User must be an Admin**

## API Endpoints

### POST /api/v1/client

Creates a new client, requires `name`

```console
curl -X POST -H "Content-type:application/json" -d '{"name": "Knight Order"}' https://example.com/api/v1/client
```

### GET /api/v1/client

Returns a list of all clients.

```console
curl -X GET https://example.com/api/v1/client
```

Returns a list of clients with a specific name if given the `search` query parameter. The `search` query parameter takes a *string* which is the clients name.

```console
curl -X GET https://example.com/api/v1/client?search=jolt
```

Returns a list of clients ordered by client name if given the `ordering` query parameter. The `ordering` query parameter either takes `name` for ascending order or `-name` for descending order.

```console
curl -X GET https://example.com/api/v1/client?ordering=-name
```

### GET /api/v1/client/[pk]

Returns a specific client with matching pk.

```console
curl -X GET https://example.com/api/v1/client/14
```

This request will return a response containing data on the specific client.

```json
{
    "id": 14,
    "name": "Knight Order"
}
```

### DELETE /api/v1/client/[pk]

Deletes a specific client with matching pk.

```console
curl -X DELETE https://example.com/api/v1/client/12
```

### PATCH  /api/v1/client/[pk]

Partial updates a specific client with matching pk.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Sun Order"}' https://example.com/api/v1/client/14
```
