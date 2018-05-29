# Client

A client is whoever contracts whoever is running kaznet to collect market data on their behalf. We need a model to hold this information.

```
TimeStampedModel
```

---
- `id`: *Postive Integer* primary key
- `name`: *String* name of the client
