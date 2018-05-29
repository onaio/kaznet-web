# XForms

Model that links XForms between Onadata and Kaznet. Inherits:

```
TimeStampedModel
```

---

- `ona_pk`: *Postive Integer*, is the OnaData primary key for the XForm Instance.
- `ona_project_id`: *Positive Integer*, is the OnaData primary key for the XForms' Project.
- `title`: *String*, is the title for the XForm.
- `id_string`: *Slug Field*.
- `deleted_at`: *Date & Time*.
- `created`: *Date & Time*, inherited from TimeStampedModel.
- `modified`: *Date & Time*, inherited from TimeStampedModel.
