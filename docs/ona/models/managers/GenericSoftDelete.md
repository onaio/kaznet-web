# Generic Soft Delete Manager

Custom Manager that adds a `alive_only` method.

- `alive_only` - Returns a queryset of object which have *deleted_at* as **None**.
