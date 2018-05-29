# XForm

Adds ability to list and retrieve XForms.

## API Endpoints

### GET /api/v1/xforms

Returns a list of all XForms.

```console
curl -X GET https://example.com/api/v1/xforms
```

### GET /api/v1/xforms/[pk]

Returns a specific XForm with matching pk.

```console
curl -X GET https://example.com/api/v1/xforms/20
```

This request returns a response containing the specific XForm.

```json
{
    "id": 20,
    "ona_pk": 9324,
    "ona_project_id": 3277,
    "title": "Form A",
    "id_string": "E-iH-p5kK_IdV",
    "created": "2018-05-28T17:55:27.980050+03:00",
    "modified": "2018-05-28T17:55:27.980069+03:00",
    "deleted_at": null
}
```
