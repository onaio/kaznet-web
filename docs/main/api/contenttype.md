# Content Type

Adds ability to list supported content types and their primary keys.

## API Endpoints

### GET /api/v1/contenttypes/

Returns a list of all allowed content types and their identifiers.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/contenttypes/
```

This request will return a response containing the list of allowed content types.

```json
{
    "links": {
        "first": "http://localhost:8000/api/v1/contenttypes/?page=1",
        "last": "http://localhost:8000/api/v1/contenttypes/?page=1",
        "next": null,
        "prev": null
    },
    "data": [
        {
            "type": "ContentType",
            "id": "13",
            "attributes": {
                "app_label": "ona",
                "model": "instance"
            }
        },
        {
            "type": "ContentType",
            "id": "15",
            "attributes": {
                "app_label": "ona",
                "model": "xform"
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
