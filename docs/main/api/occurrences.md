# Occurrences

Adds ability to List and Retrieve Occurrences. **Requires User to be an Admin to access Endpoint**

## API Endpoints

### GET /api/v1/occurrences/

Returns a list of all occurrences.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurences
```

Returns a list of all occurences for a specific task if given the `task` query parameter.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences?task=24
```

Returns a list of all occurrences for a specific `start_time` if given the `start_time` query parameter. The `start_time` query parameter allows the following time lookups and takes a *String* which is time as an input.

- exact
- gt
- lt
- lte
- gte

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences?start_time__gte=17:00:00
```

Returns a list of all occurrences for a specific `end_time` if given the `end_time` query parameter. The `end_time` query parameter allows the following time lookups and takes a *String* which is time as an input.

- exact
- gt
- lt
- lte
- gte

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences?end_time__exact=17:00:00
```

Returns a list of all occurrences for a specific `date` if given the `date` query parameter. The `date` query parameter allows the following datetime lookups and takes a *String* which is time as an input.

- exact
- gt
- lt
- gte
- lte
- year
- year__gt
- year__lt
- year__gte
- year__lte
- month
- month__gt
- month__lt
- month__gte
- month__lte
- day day__gt
- day__lt
- day__gte
- day__lte

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences?date__year__gte=2017
```

Returns a list of occurences ordered by either `created`, `date`, `start_time` or `end_time` in ascending order or `-created`, `-date`, `-start_time` or `end_time` in descending order if passed into the `ordering` query parameter.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences/?ordering=created,-date,start_time,end_time
```

## GET /api/v1/occurrences/[pk]/

Returns a specific Occurrence.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/occurrences/1/
```

This request returns a response containing the specific Occurrence.

```json
{
    "data": {
        "type": "TaskOccurrence",
        "id": "1",
        "attributes": {
            "created": "2018-06-13T09:05:38.009325+03:00",
            "modified": "2018-06-13T09:05:38.009343+03:00",
            "date": "2018-06-13",
            "start_time": "09:05:38",
            "end_time": "23:59:59.999999",
            "time_string": "13th June 2018, 9:05 a.m. to 11:59 p.m."
        },
        "relationships": {
            "task": {
                "data": {
                    "type": "Task",
                    "id": "1"
                }
            }
        }
    }
}
```
