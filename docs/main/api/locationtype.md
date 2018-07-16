# Location Types

This API endpoint follows the [JSON API](http://jsonapi.org/) structure.

Adds ability to create, list, update, delete and retrieve a Location Type.

Once a Location Type is created it's stored in the database and can be retrieved from the API as shown below. **To Use this API Endpoint User must be an Admin**

## API Endpoints

### POST /api/v1/locationtypes/

Creates a new location type, requires `name`

```console
curl -X POST -H "Content-type:application/vnd.api+json" -d '{"data":{"type":"LocationType","id":null,"attributes":{"name":"The Palace"}}}' http://127.0.0.1:8000/api/v1/locationtypes/
```

Returns the location type that was created:

```json
{
    "data": {
        "type": "Location Type",
        "id": "4",
        "attributes": {
            "name": "The Palace"
        }
    }
}
```

### GET /api/v1/locationtypes/

Returns a list of all location types.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" http://127.0.0.1:8000/api/v1/locationtypes/
```

```json
{
    "links": {
        "first": "http://127.0.0.1:8000/api/v1/locationtypes/?page=1",
        "last": "http://127.0.0.1:8000/api/v1/locationtypes/?page=1",
        "next": null,
        "prev": null
    },
    "data": [
        {
            "type": "LocationType",
            "id": "2",
            "attributes": {
                "created": "2018-07-13T17:34:27.023947+03:00",
                "name": "Hospital",
                "modified": "2018-07-13T17:34:27.023970+03:00"
            }
        },
        {
            "type": "LocationType",
            "id": "1",
            "attributes": {
                "created": "2018-07-13T17:34:14.408576+03:00",
                "name": "Market",
                "modified": "2018-07-13T17:34:14.408599+03:00"
            }
        }
    ],
    "meta": {
        "pagination": {
            "page": 1,
            "pages": 1,
            "count": 2
        }
    }
}
```

Returns a list of location types with a specific name if given the `search` query parameter. The `search` query parameter takes a *string* which is the location type name.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "http://127.0.0.1:8000/api/v1/locationtypes/?search=jolt"
```

Returns a list of location types ordered by location type name if given the `ordering` query parameter. The `ordering` query parameter either takes `name` for ascending order or `-name` for descending order.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "http://127.0.0.1:8000/api/v1/locationtypes/?ordering=-name"
```

### GET /api/v1/locationtypes/[pk]/

Returns a specific location type with matching pk.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "http://127.0.0.1:8000/api/v1/locationtypes/2/"
```

This request will return a response containing data on the specific location type.

```json
{
    "data": {
        {
            "type": "LocationType",
            "id": "1",
            "attributes": {
                "created": "2018-07-13T17:34:14.408576+03:00",
                "name": "Market",
                "modified": "2018-07-13T17:34:14.408599+03:00"
            }
        }
    }
}
```

### DELETE /api/v1/locationtypes/[pk]/

Deletes a specific location type with matching pk.

```console
curl -X DELETE -H "Content-Type:application/vnd.api+json" "http://127.0.0.1:8000/api/v1/locationtypes/12/"
```

### PATCH  /api/v1/locationtypes/[pk]/

Partial updates a specific location type with matching pk.

```console
curl -X PATCH -H "Content-Type:application/vnd.api+json" -d '{"data":{"type":"LocationType","id":3,"attributes":{"name":"Sun Order"}}}' "http://127.0.0.1:8000/api/v1/locationtypes/3/"
```
