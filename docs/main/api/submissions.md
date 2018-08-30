# Submissions

Adds ability to list and retrieve Submissions.

## API Endpoint

### GET /api/v1/submissions/ :: **Can only list own Submissions unless Admin**

Returns a list of all submissions.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/
```

Returns a list of submissions for a specific task if given `task` query parameter. The `task` query parameter takes a *integer* which is a unique identifier for a task.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?task=4
```

Returns a list of submissions for a specific location if given `location` query parameter. The `location` query parameter takes a *integer* which is a unique identifier for a location.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?location=46
```

Returns a list of submissions from a specific user if given `user` query parameter. The `user` query parameter takes a *integer* which is a unique identifier for a user.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?user=17
```

Returns a list of submissions with a specific status if given `status` query parameter. The `status` query parameter takes a *string* which can be either **a** for Approved, **b** for Rejected Status, **c** for Under Review, **d** for Pending Review.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?status=b
```

Returns a list of all valid or invalid submissions if given `valid` query parameter. The `valid` query parameter takes a *boolean*.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?valid=0
```

Returns a list of all submissions filtered by modified if given `modified` query parameter. The `modified` query parameter takes a _datetime_ formatted as "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][tz]". You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by modified.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/submissions/?modified__gt=2018-06-15 06:00:00.000000"
```

Returns a list of all submissions ordered by either creation date, valid status, submission status, time of submission or task if given `ordering` query parameter. The `ordering` can be done in ascending order using either `bounty__amount`, `submission_time` or `task__id` and in descending order using either `-bounty__amount`, `-submission_time` or `-task__id`

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/?ordering=-created,valid,submission_time,task__id,status
```

### GET /api/v1/submissions/[pk]/

Return a specific submission with matching pk.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/submissions/20/
```

This request will return a response containing the specific submission.

```json
{
    "data": {
        "type": "Submission",
        "id": "1",
        "attributes": {
            "modified": "2018-06-13T09:06:04.007967+03:00",
            "created": "2018-06-13T09:05:49.896293+03:00",
            "submission_time": "2018-06-13T09:05:00+03:00",
            "valid": true,
            "approved": true,
            "status": "a",
            "comments": "",
            "target_id": 1,
            "amount": "5000.00 KES"
        },
        "relationships": {
            "task": {
                "data": {
                    "type": "Task",
                    "id": "1"
                }
            },
            "bounty": {
                "data": {
                    "type": "Bounty",
                    "id": "1"
                }
            },
            "location": {
                "data": null
            },
            "user": {
                "data": {
                    "type": "User",
                    "id": "1"
                }
            },
            "target_content_type": {
                "data": {
                    "type": "ContentType",
                    "id": "15"
                }
            }
        }
    }
}
```
