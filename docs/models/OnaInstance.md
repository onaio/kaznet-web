# Ona Instances

Model for OnaData Instances. Inherits:

```
TimeStampedModel
```

---

- `ona_pk`: *Postive Integer*, is the OnaData primary key for the XForm Instance.
- `xform`: *Integer*, is a unique identifier for a XForm object.
- `json`: *Json*, contains data of Instance.
- `deleted_at`: *Date & Time*.
- `created`: *Date & Time*, inherited from TimeStampedModel.
- `modified`: *Date & Time*, inherited from TimeStampedModel.
