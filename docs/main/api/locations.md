# Locations

This API endpoint follows the [JSON API](http://jsonapi.org/) structure.

Adds ability to create, list, update, delete and retrieve Locations.

Once a Location is created it's stored in the database and can be retrieved from the API as shown below. Only Admins Can interact with this API Endpoint

## API Endpoints

### POST /api/v1/locations/

Creates a new location, requires a `name`.

```console
curl -X POST -H "Content-type:application/vnd.api+json" -d '{"data": {"type": "Location","id": "1","attributes": {"name":"Sol Point","country":"CK","description":"Something"}}}' https://example.com/api/v1/locations/
```

The `name` is a *string*. It can take additional inputs in the content such as:

- `parent`: *integer*, is the unique identifier for a parent location object.
- `country`: *string*, is the country code of a country.
- `geopoint`: *string*, is a comma separated string specifying longtitude and latitude. Longtitude should be written first followed by a comma then the latitude. **If geopoint is specified, radius should be inputed and shapefile shouldn't be uploaded.**
- `radius`: *decimal*. **If radius is specified, geopoint should be inputted and shapefile shouldn't be uploaded.**
- `shapefile`: *shapefile*, is a *.zip* file containing strictly three files, the *.shp*, *.shx* and *.dbf* files. **If shapefile is uploaded, geopoint and radius shouldn't be inputted.**

### GET /api/v1/locations/

Returns a list of all locations

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/
```

Returns a list of all locations with a specific parent location if given a `parent` query parameter. The `parent` query parameter takes an *integer* which is the unique identifier for the parent location.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/?parent=2
```

Returns a list of all locations in a specific country if given a `country` query parameter. The `country` query parameter takes a *string* which is the country code.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/?country=KE
```

Returns a list of all locations with a specific name if given `search` query parameter. The `search` query parameter takes a *string* which is the name of the location.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/?search=eldorado
```

Returns a list of locations ordered by name or creation date if given `ordering` query parameter. The `ordering` can be done in ascending order using either `name` or `created` and can be done in descending order using either `-name` or `-created`.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/?ordering=name,created
```

### GET /api/v1/locations/[pk]/

Returns a specific location with matching pk.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/24/
```

This request will return a response containing the specific location.

```json
{
    "data": {
        "type": "Location",
        "id": "1",
        "attributes": {
            "name": "Here",
            "country": "KE",
            "parent_name": "None",
            "description": "",
            "geopoint": null,
            "radius": null,
            "shapefile": null,
            "created": "2018-06-19T16:03:47.411387+03:00",
            "modified": "2018-06-19T16:03:47.411411+03:00"
        },
        "relationships": {
            "location_type": {
                "data": null
            },
            "parent": {
                "data": null
            }
        }
    }
}
```

### DELETE /api/v1/locations/pk/

Deletes a specific location with matching pk.

```console
curl -X DELETE -H "Content-type:application/vnd.api+json" https://example.com/api/v1/locations/23/
```

### PATCH /api/v1/locations/[pk]/

Partially Updates a specific location with matching pk. Takes the same inputs as the POST create location request but with an additional location `id` in the url.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Hyperion"}' https://example.com/api/v1/locations/24/
```
