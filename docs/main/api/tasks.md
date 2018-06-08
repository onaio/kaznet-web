# Tasks

Adds ability to create, list, update, delete and retrieve Tasks.

Once a Task is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/tasks :: Requires User to be an Admin

Creates a Task, requires a `name`, `timing_rule`, `target_content_type` and `target_id`. It can optionally also create a bounty if an `amount` is passed.

```console
curl -X POST -H "Content-Type:application/json" '{"name": "Cow price", "description": "Some description", "total_submission_target": 10, "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", "target_content_type": 9, "target_id": 234, "amount": 5400}' https://example.com/api/v1/tasks
```

`target_content_type`: *integer*, is a unique identifier for any of the allowed content types.

`timing_rule`: *string*, is a [standard rrule](https://tools.ietf.org/html/rfc2445) *string*.

`target_id`: *integer*, is the target identifier.

It can take additional optional inputs in the content such as:

- `status`: *string*, can be either an **a** for ACTIVE, **s** for SCHEDULED, **b** for DEACTIVATED, **c** for EXPIRED or **d** for DRAFT.
- `parent`: *integer*, is the unique identifier for a parent task object.
- `description`: *string*.
- `start`: *Date and Time*.
- `end`: *Date and Time*.
- `total_submission_target`: *integer*.
- `user_submission_target`: *integer*.
- `segment_rules`: *list of integers*, is the unique identifier for a segment rule.
- `locations`: *list of integers*, is the unique identifier for a location.
- `estimated_time`: *string*, is a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) *string*.
- `client`: *integer*, is the unique identifier for a client object.
- `amount`: *integer*, is the bounty of the task.

### GET /api/v1/tasks

Returns a list of all tasks.

```console
curl -X GET https://example.com/api/v1/tasks
```

Returns a list of all tasks with specific locations if given `locations` query parameter. The `locations` query parameter takes an *integer* which is the unique identifier for a location object.

```console
curl -X GET https://example.com/api/v1/tasks?locations=1
```

Returns a list of all tasks with specific status if given `status` query parameter. The `status` query parameter takes a *string* which can be either an **a** for ACTIVE, **b** for DEACTIVATED, **c** for EXPIRED, **d** for DRAFT, **e** for ARCHIVED or **s** for SCHEDULED.

```console
curl -X GET https://example.com/api/v1/tasks?status=b
```

Returns a list of all tasks in a specific project if given `project` query parameter. The `project` query parameter takes an *integer* which is the unique identifier for a project object.

```console
curl -X GET https://example.com/api/v1/tasks?project=498
```

Returns a list of all tasks with a specific parent if given `parent` query parameter. The `parent` query parameter takes an *integer* which is the unique identifier for a parent location object.

```console
curl -X GET https://example.com/api/v1/tasks?parent=43
```

Returns a list of all tasks with a specific client if given `clinet` query parameter. The `client` query parameter takes an *integer* which is the unique identifier for a client object.

```console
curl -X GET https://example.com/api/v1/tasks?client=78
```

Returns a list of all tasks filtered by date if given `date` query parameter. The `date` query parameter takes a *date* formatted like so "yyyy-mm-dd".  You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by date.

```console
curl -X GET https://example.com/api/v1/tasks?date__gt=2018-05-21

```

Returns a list of all tasks filtered by time if given `start_time` query parameter. The `start_time` query parameter takes a *time* formatted like so "H:M".  You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by time.

```console
curl -X GET https://example.com/api/v1/tasks?start_time__lte=17:27

```

Returns a list of all tasks filtered by time if given `end_time` query parameter. The `end_time` query parameter takes a *time* formatted like so "H:M".  You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by time.

```console
curl -X GET https://example.com/api/v1/tasks?end_time=21:00
```

Returns a list of all tasks ordered by either creation date, task status, number of submissions or name of task if given a `ordering` query parameter. The `ordering` query parameter takes either `created`, `status`, `submission_count`, `estimated_time`, `project__id`, `bounty__amount` or `name` for ascending order and either `-created`, `-status`, `-submission_count`, `-project_id`, `-estimated_time`, `-bounty__amount` or `-name` for descending order.

```console
curl -X GET https://example.com/api/v1/tasks?ordering=-created,status,name,submission_count,-project__id,-submission_count,-bounty__amount
```

### GET /api/v1/tasks/[pk]

Returns a specific task with matching pk.

```console
curl -X GET https://example.com/api/v1/tasks/81
```

This request returns a response containing the specific task.

```json
{
    "id": 81,
    "created": "2018-05-24T09:00:06.750893+03:00",
    "modified": "2018-05-24T09:00:06.750912+03:00",
    "name": "Cow price",
    "parent": null,
    "client": null,
    "description": "Some description",
    "start": "2018-05-24T09:00:06+03:00",
    "end": "2018-07-03T09:00:06+03:00",
    "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", "total_submission_target": 10,
    "user_submission_target": null,
    "status": "d",
    "target_content_type": 9,
    "target_id": 45,
    "segment_rules": [8, 7],
    "locations": []
}
```

### DELETE /api/v1/tasks/[pk] :: Requires User to be an Admin

Deletes a specific task with matching pk.

```console
curl -X DELETE https://example.com/api/v1/tasks/81
```

### PATCH /api/v1/tasks/[pk] :: Requires User to be an Admin

Partially updates a specific task with matching pk. Takes the same inputs as the POST Create request with an addition of a specific tasks `id` on the url.

```console
curl -X PATCH "Content-Type:application/json" -d '{"name": "Cheese Shop Locations"}' https://example.com/api/v1/tasks/18
```
