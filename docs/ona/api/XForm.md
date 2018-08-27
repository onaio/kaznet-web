# XForm

Adds ability to list and retrieve XForms.

## API Endpoints

### GET /api/v1/forms/

Returns a list of all XForms.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/forms/"
```

```json
{
    "links": {
        "first": "https://example.com/api/v1/forms/?page=1",
        "last": "https://example.com/api/v1/forms/?page=1",
        "next": null,
        "prev": null
    },
    "data": [{
        "type": "XForm",
        "id": "98",
        "attributes": {
            "ona_pk": 202979,
            "ona_project_id": 21,
            "last_updated": null,
            "title": "XLSX_String_Name_Export1",
            "id_string": "XLSX_String_Name_Export1",
            "created": "2018-07-10T16:41:01.948801+03:00",
            "modified": "2018-07-10T16:55:07.339018+03:00",
            "deleted_at": null,
            "has_task": false
        },
        "relationships": {
            "project": {
                "data": null
            }
        }
    }, {
        "type": "XForm",
        "id": "160",
        "attributes": {
            "ona_pk": 214440,
            "ona_project_id": 21,
            "last_updated": null,
            "title": "XLS_Report_Form",
            "id_string": "XLS_Report_Form",
            "created": "2018-07-10T16:41:02.054439+03:00",
            "modified": "2018-07-10T16:55:07.420101+03:00",
            "deleted_at": null,
            "has_task": false
        },
        "relationships": {
            "project": {
                "data": null
            }
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

Returns a list of all XForms filtered by `has_task` if given `has_task` query parameter. The `has_task` query parameter takes either *true* or *false*.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/forms/?has_task=false"
```

Returns a list of XForms with a specific title if given the `search` query parameter. The `search` query parameter takes a *string* which is the forms title.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/forms/?search=mosquito"
```

Returns a list of forms ordered by XForm title if given the `ordering` query parameter. The `ordering` query parameter either takes `title` for ascending order or `-title` for descending order.

```console
curl -X GET -H "Content-Type:application/vnd.api+json" "https://example.com/api/v1/forms/?ordering=-title"
```

### GET /api/v1/forms/[pk]/

Returns a specific XForm with matching pk.

```console
curl -X GET https://example.com/api/v1/forms/20/
```

This request returns a response containing the specific XForm.

```json
{
    "data": {
        "type": "XForm",
        "id": "1",
        "attributes": {
            "ona_pk": 122938,
            "ona_project_id": 17,
            "last_updated": null,
            "title": "Baseline_Questionnaire",
            "id_string": "Baseline_Questionnaire",
            "created": "2018-07-10T16:41:01.828550+03:00",
            "modified": "2018-07-10T16:55:07.140987+03:00",
            "deleted_at": null,
            "has_task": true
        },
        "relationships": {
            "project": {
                "data": null
            }
        }
    }
}
```
