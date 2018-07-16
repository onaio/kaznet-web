# Tasks

This API endpoint follows the [JSON API](http://jsonapi.org/) structure.

Adds ability to create, list, update, delete and retrieve Tasks.

Once a Task is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/tasks/ :: Requires User to be an Admin

Creates a Task, requires a `name`, `timing_rule`, `target_content_type` and `target_id`. It can optionally also create a bounty if an `amount` is passed.

```console
curl -X POST -H "Content-Type:application/vnd.api+json" -d '{"data":{"type":"Task","id":null,"attributes":{"name":"Coconut Quest","estimated_time":"3 2:20:10","description":"This is awesome, as tasks go.","start":"2018-06-12T17:48:34+03:00","end":"2018-12-12T17:48:34+03:00","timing_rule":"RRULE:FREQ=DAILY;INTERVAL=10;COUNT=50","total_submission_target":1000,"user_submission_target":5,"status":"d","target_id":1,"target_content_type":16,"client":{"type":"Client","id":"1"},"locations_input":[{"location":{"type":"Location","id":1},"timing_rule":"RRULE:FREQ=DAILY;INTERVAL=10;COUNT=7","start":"09:00:00","end":"15:00:00"}]}}}' "http://example.com/api/v1/tasks/"
```

`target_content_type`: _integer_, is a unique identifier for any of the allowed content types.

`timing_rule`: _string_, is a [standard rrule](https://tools.ietf.org/html/rfc2445) _string_.

`target_id`: _integer_, is the target identifier.

It can take additional optional inputs in the content such as:

- `status`: _string_, can be either an **a** for ACTIVE, **s** for SCHEDULED, **b** for DEACTIVATED, **c** for EXPIRED or **d** for DRAFT.
- `parent`: _integer_, is the unique identifier for a parent task object.
- `description`: _string_.
- `start`: _Date and Time_.
- `end`: _Date and Time_.
- `total_submission_target`: _integer_.
- `user_submission_target`: _integer_.
- `segment_rules`: _list of integers_, is the unique identifier for a segment rule.
- `estimated_time`: _string_, is a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) _string_.
- `client`: _integer_, is the unique identifier for a client object.
- `amount`: _integer_, is the bounty of the task.
- `required_expertise`: _string_, can be either '1' for BEGINNER, '2' for INTERMEDIATE, '3' for ADVANCED or '4' for EXPERT.
- `locations_input`: _list of dictionaries_, this is the list of locations at which the task can be done. The dictionary has the following fields:
  - location_id: _int_, the id of the location
  - timing_rule: _string_, is a [standard rrule](https://tools.ietf.org/html/rfc2445) _string_.
  - start: _string_, the start time e.g. '09:00:00'
  - end: _string_, the end time e.g. '19:30:00'

### GET /api/v1/tasks/

Returns a list of all tasks.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/"
```

```json
{
  "links": {
    "first": "http://127.0.0.1:8000/api/v1/tasks/?format=vnd.api%2Bjson&page=1",
    "last": "http://127.0.0.1:8000/api/v1/tasks/?format=vnd.api%2Bjson&page=1",
    "next": null,
    "prev": null
  },
  "data": [
    {
      "type": "Task",
      "id": "1",
      "attributes": {
        "created": "2018-07-09T14:54:58.972959+03:00",
        "modified": "2018-07-09T15:08:56.291994+03:00",
        "name": "Awful Task",
        "estimated_time": "3 02:20:10",
        "approved_submissions_count": 0,
        "pending_submissions_count": 0,
        "rejected_submissions_count": 0,
        "total_bounty_payout": "0 KES",
        "current_bounty_amount": null,
        "required_expertise": "1",
        "description": "This is awesome, as tasks go.",
        "xform_title": "Form1",
        "xform_id_string": "form_1",
        "status_display": "Draft",
        "required_expertise_display": "Beginner",
        "start": "2018-06-12T17:48:34+03:00",
        "end": "2018-12-12T17:48:34+03:00",
        "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=50",
        "total_submission_target": 1000,
        "user_submission_target": 5,
        "status": "d",
        "submission_count": 0,
        "target_id": 1,
        "created_by_name": "Ona User",
        "task_locations": []
      },
      "relationships": {
        "created_by": {
          "data": {
            "type": "User",
            "id": "3"
          }
        },
        "parent": {
          "data": null
        },
        "client": {
          "data": {
            "type": "Client",
            "id": "1"
          }
        },
        "bounty": {
          "data": null
        },
        "target_content_type": {
          "data": {
            "type": "ContentType",
            "id": "16"
          }
        },
        "segment_rules": {
          "data": [],
          "meta": {
            "count": 0
          }
        },
        "locations": {
          "data": [],
          "meta": {
            "count": 0
          }
        }
      }
    },
    {
      "type": "Task",
      "id": "2",
      "attributes": {
        "created": "2018-07-09T14:59:22.934380+03:00",
        "modified": "2018-07-09T15:09:03.019849+03:00",
        "name": "Coconut Quest",
        "estimated_time": "3 02:20:10",
        "approved_submissions_count": 0,
        "pending_submissions_count": 0,
        "rejected_submissions_count": 0,
        "total_bounty_payout": "0 KES",
        "current_bounty_amount": null,
        "required_expertise": "1",
        "description": "This is awesome, as tasks go.",
        "xform_title": "Form1",
        "xform_id_string": "form_1",
        "status_display": "Draft",
        "required_expertise_display": "Beginner",
        "start": "2018-06-12T17:48:34+03:00",
        "end": "2018-12-12T17:48:34+03:00",
        "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=50",
        "total_submission_target": 1000,
        "user_submission_target": 5,
        "status": "d",
        "submission_count": 0,
        "target_id": 1,
        "created_by_name": "Davis Raymond",
        "task_locations": [
          {
            "task": {
              "type": "Task",
              "id": "2"
            },
            "created": "2018-07-09T14:59:22.954438+03:00",
            "modified": "2018-07-09T14:59:22.954454+03:00",
            "location": {
              "type": "Location",
              "id": "1"
            },
            "location_name": "Kiambu",
            "location_description": "Some county in Kenya",
            "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=7",
            "start": "09:00:00",
            "end": "15:00:00"
          }
        ]
      },
      "relationships": {
        "created_by": {
          "data": {
            "type": "User",
            "id": "1"
          }
        },
        "parent": {
          "data": null
        },
        "client": {
          "data": {
            "type": "Client",
            "id": "1"
          }
        },
        "bounty": {
          "data": null
        },
        "target_content_type": {
          "data": {
            "type": "ContentType",
            "id": "16"
          }
        },
        "segment_rules": {
          "data": [],
          "meta": {
            "count": 0
          }
        },
        "locations": {
          "data": [
            {
              "type": "Location",
              "id": "1"
            }
          ],
          "meta": {
            "count": 1
          }
        }
      }
    },
    {
      "type": "Task",
      "id": "3",
      "attributes": {
        "created": "2018-07-09T15:08:12.817452+03:00",
        "modified": "2018-07-09T15:09:10.675419+03:00",
        "name": "Livestock Prices",
        "estimated_time": "3 02:20:10",
        "approved_submissions_count": 0,
        "pending_submissions_count": 0,
        "rejected_submissions_count": 0,
        "total_bounty_payout": "0 KES",
        "current_bounty_amount": "15.00 KES",
        "required_expertise": "1",
        "description": "This is awesome, as tasks go.",
        "xform_title": "Form1",
        "xform_id_string": "form_1",
        "status_display": "Draft",
        "required_expertise_display": "Beginner",
        "start": "2018-06-12T17:48:34+03:00",
        "end": "2018-12-12T17:48:34+03:00",
        "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=50",
        "total_submission_target": 5,
        "user_submission_target": 1,
        "status": "d",
        "submission_count": 0,
        "target_id": 1,
        "created_by_name": "Ona User",
        "task_locations": [
          {
            "task": {
              "type": "Task",
              "id": "3"
            },
            "created": "2018-07-09T15:08:12.842855+03:00",
            "modified": "2018-07-09T15:08:12.842871+03:00",
            "location": {
              "type": "Location",
              "id": "1"
            },
            "location_name": "Meru",
            "location_description": "Some county in Kenya",
            "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=7",
            "start": "09:00:00",
            "end": "15:00:00"
          }
        ]
      },
      "relationships": {
        "created_by": {
          "data": {
            "type": "User",
            "id": "3"
          }
        },
        "parent": {
          "data": null
        },
        "client": {
          "data": {
            "type": "Client",
            "id": "1"
          }
        },
        "bounty": {
          "data": {
            "type": "Bounty",
            "id": "1"
          }
        },
        "target_content_type": {
          "data": {
            "type": "ContentType",
            "id": "16"
          }
        },
        "segment_rules": {
          "data": [],
          "meta": {
            "count": 0
          }
        },
        "locations": {
          "data": [
            {
              "type": "Location",
              "id": "1"
            }
          ],
          "meta": {
            "count": 1
          }
        }
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 1,
      "count": 3
    }
  }
}
```

Returns a list of all tasks with specific locations if given `locations` query parameter. The `locations` query parameter takes an _integer_ which is the unique identifier for a location object.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?locations=1"
```

Returns a list of all tasks with specific status if given `status` query parameter. The `status` query parameter takes a _string_ which can be either an **a** for ACTIVE, **b** for DEACTIVATED, **c** for EXPIRED, **d** for DRAFT, **e** for ARCHIVED or **s** for SCHEDULED.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?status=b"
```

Returns a list of all tasks in a specific project if given `project` query parameter. The `project` query parameter takes an _integer_ which is the unique identifier for a project object.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?project=498"
```

Returns a list of all tasks with a specific parent if given `parent` query parameter. The `parent` query parameter takes an _integer_ which is the unique identifier for a parent location object.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?parent=43"
```

Returns a list of all tasks with a specific client if given `client` query parameter. The `client` query parameter takes an _integer_ which is the unique identifier for a client object.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?client=78"
```

Returns a list of all tasks filtered by modified if given `modified` query parameter. The `modified` query parameter takes a _datetime_ formatted as "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][tz]". You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by modified.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?modified__gt=2018-06-15 06:00:00.000000"
```

Returns a list of all tasks filtered by date if given `date` query parameter. The `date` query parameter takes a _date_ formatted like so "yyyy-mm-dd". You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by date.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?date__gt=2018-05-21"
```

Returns a list of all tasks filtered by time if given `start_time` query parameter. The `start_time` query parameter takes a _time_ formatted like so "H:M". You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by time.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?start_time__lte=17:27"
```

Returns a list of all tasks filtered by time if given `end_time` query parameter. The `end_time` query parameter takes a _time_ formatted like so "H:M". You can use [standard Django lookups](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups) when filtering by time.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?end_time=21:00"
```

Returns a list of all tasks ordered by either creation date, task status, number of submissions or name of task if given a `ordering` query parameter. The `ordering` query parameter takes either `created`, `status`, `submission_count`, `estimated_time`, `project__id`, `bounty__amount` or `name` for ascending order and either `-created`, `-status`, `-submission_count`, `-project_id`, `-estimated_time`, `-bounty__amount` or `-name` for descending order.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/?ordering=-created,status,name,submission_count,-project__id,-submission_count,-bounty__amount"
```

### GET /api/v1/tasks/[pk]/

Returns a specific task with matching pk.

```console
curl -X GET -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/81/"
```

This request returns a response containing the specific task.

```json
{
    "type": "Task",
    "id": "3",
    "attributes": {
    "created": "2018-07-09T15:08:12.817452+03:00",
    "modified": "2018-07-09T15:09:10.675419+03:00",
    "name": "Livestock Prices",
    "estimated_time": "3 02:20:10",
    "approved_submissions_count": 0,
    "pending_submissions_count": 0,
    "rejected_submissions_count": 0,
    "total_bounty_payout": "0 KES",
    "current_bounty_amount": "15.00 KES",
    "required_expertise": "1",
    "description": "This is awesome, as tasks go.",
    "xform_title": "Form1",
    "xform_id_string": "form_1",
    "status_display": "Draft",
    "required_expertise_display": "Beginner",
    "start": "2018-06-12T17:48:34+03:00",
    "end": "2018-12-12T17:48:34+03:00",
    "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=50",
    "total_submission_target": 5,
    "user_submission_target": 1,
    "status": "d",
    "submission_count": 0,
    "target_id": 1,
    "created_by_name": "Ona User",
    "task_locations": [
        {
        "task": {
            "type": "Task",
            "id": "3"
        },
        "created": "2018-07-09T15:08:12.842855+03:00",
        "modified": "2018-07-09T15:08:12.842871+03:00",
        "location": {
            "type": "Location",
            "id": "1"
        },
        "location_name": "Taita Taveta",
        "location_description": "Some county in Kenya",
        "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=7",
        "start": "09:00:00",
        "end": "15:00:00"
        }
    ]
    },
    "relationships": {
    "created_by": {
        "data": {
        "type": "User",
        "id": "3"
        }
    },
    "parent": {
        "data": null
    },
    "client": {
        "data": {
        "type": "Client",
        "id": "1"
        }
    },
    "bounty": {
        "data": {
        "type": "Bounty",
        "id": "1"
        }
    },
    "target_content_type": {
        "data": {
        "type": "ContentType",
        "id": "16"
        }
    },
    "segment_rules": {
        "data": [],
        "meta": {
        "count": 0
        }
    },
    "locations": {
        "data": [
        {
            "type": "Location",
            "id": "1"
        }
        ],
        "meta": {
        "count": 1
        }
    }
    }
}
```

### DELETE /api/v1/tasks/[pk]/ :: Requires User to be an Admin

Deletes a specific task with matching pk.

```console
curl -X DELETE -H "Content-type:application/vnd.api+json" "https://example.com/api/v1/tasks/81/"
```

### PATCH /api/v1/tasks/[pk]/ :: Requires User to be an Admin

Partially updates a specific task with matching pk. Takes the same inputs as the POST Create request with an addition of a specific tasks `id` on the url.

```console
curl -X PATCH -H "Content-Type:application/vnd.api+json" -d '{"data":{"type":"Task","id":5,"attributes":{"name":"Awesome Task"}}}' "https://example.com/api/v1/tasks/5/"
```
