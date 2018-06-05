# User Profiles

Model for User Profiles, extends the auth.User.

Inherits:

```
TimeStamped Model
```

---

- `user`: *Foreign Key*, is the foreign key for a auth.User entity.
- `ona_pk`: *Postive Integer*, is the OnaData primary key for the Users Instance.
- `ona_username`: *Text*.
- `national_id`: *Text*
- `payment_number`: *Phone Number*, is a mobile number that has mobile money enabled.
- `phone_number`: *Phone Number*
- `role`: *Integer*, can either be 1 for ADMIN or 2 for CONTRIBUTOR
- `expertise`: *Integer*, can either be 1 for BEGINNER, 2 for INTERMEDIATE, 3 for ADVANCED or 4 for EXPERT.
- `gender`: *Integer*, can either be 0 for OTHER, 1 for MALE or 2 for FEMALE
