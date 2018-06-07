# Occurrences

Adds ability to List and Retrieve Occurences. **Requires User to be an Admin to access Endpoint**

## API Endpoints

### GET /api/v1/occurrences

Returns a list of all occurrences.

```console
curl -X GET https://example.com/api/v1/occurences
```

Returns a list of all occurences for a specific task if given the `task` query parameter.

```console
curl -X https://example.com/api/v1/occurrences?task=24
```

Returns a list of all occurrences for a specific `start_time` if given the `start_time` query parameter. The `start_time` query parameter allows the following time lookups and takes a *String* which is time as an input.

- exact
- gt
- lt
- lte
- gte

```console
curl -X https://example.com/api/v1/occurrences?start_time__gte=17:00:00
```

Returns a list of all occurrences for a specific `end_time` if given the `end_time` query parameter. The `end_time` query parameter allows the following time lookups and takes a *String* which is time as an input.

- exact
- gt
- lt
- lte
- gte

```console
curl -X https://example.com/api/v1/occurrences?end_time__exact=17:00:00
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
curl -X https://example.com/api/v1/occurrences?date__year__gte=2017
```
