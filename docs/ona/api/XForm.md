# XForm

Adds ability to list and retrieve XForms.

## API Endpoints

### GET /api/v1/xforms/

Returns a list of all XForms.

```console
curl -X GET https://example.com/api/v1/xforms/
```

Returns a list of all XForms filtered by `has_task` if given `has_task` query parameter. The `has_task` query parameter takes either *1* for *True* or *0* for *False*.

```console
curl -X GET https://example.com/api/v1/xforms/?has_task=0
```

### GET /api/v1/xforms/[pk]/

Returns a specific XForm with matching pk.

```console
curl -X GET https://example.com/api/v1/xforms/20/
```

This request returns a response containing the specific XForm.

```json
{
    "data": {
        "type": "XForm",
        "id": "1",
        "attributes": {
            "ona_pk": 53,
            "project_id": 1,
            "last_updated": "2018-05-30T09:47:23.196149+03:00",
            "title": "Form",
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "created": "2018-06-13T09:48:20.976288+03:00",
            "modified": "2018-06-13T09:48:20.976307+03:00",
            "deleted_at": null
        }
    }
}
```
