# User Profile

Adds ability to Create, Update, Delete, Retrieve and List User Profiles.

## API Endpoints

### POST /api/v1/userprofiles :: **User must be Admin to perform this request**

Creates a User Profile, requires `user`.

- `user`: *string*, is the unique identifier for a User Object.

Optionally it can also take:

- `ona_pk`: *Positive Integer*, is the uniqure identifier for an Ona User.
- `ona_username`: *Text*, is the username of User in Ona.
- `national_id`: *String*.
- `payment_number`: *Phone Number*
- `phone_number`: *Phone Number*
- `role`: *Integer*, can either be 1 for ADMIN or 2 for CONTRIBUTOR
- `expertise`: *Integer*, can either be 1 for BEGINNER, 2 for INTERMEDIATE, 3 for ADVANCED or 4 for EXPERT.
- `gender`: *Integer*, can either be 0 for OTHER, 1 for MALE or 2 for FEMALE

### GET /api/v1/userprofiles/ :: **User must be Admin to perform this request**

Returns a list of all user profiles.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/
```

Returns a list of User Profiles with a specific First Name, Last Name, Ona Username, Email or National Id if given a `search` query parameter.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/?search=David
```

Returns a list of User Profiles with specific role if given a `role` query parameter. The `role` takes an *Integer* which has to be either 1 for ADMIN or 2 for CONTRIBUTOR.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/?role=1
```

Returns a profile tied to a specific Ona user if given `ona_username` query parameter. The `user` query parameter takes a *String*.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/?ona_username=lee
```

Returns a list of User Profiles with specific expertise if given a `expertise` query parameter. The `expertise` takes an *Integer* which has to be either  1 for BEGINNER, 2 for INTERMEDIATE, 3 for ADVANCED or 4 for EXPERT.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/?expertise=1
```

Returns a list of User Profiles either ordered by `user__first_name`, `user__last_name`, `created`, `submission_count` or `national_id` if given a `ordering` query parameter. The `ordering` can be done in ascending order using either `user__first_name`, `user__last_name`, `created`, `submission_count` or `national_id`. It can also be done in descending order using `-user__first_name`, `-user__last_name`, `-created`, `-submission_count` or `-national_id`.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/?ordering=user__first_name,-national_id
```

### GET /api/v1/userprofiles/[pk]/

Returns a specific user profile with matching pk. **Requires User to either be linked to the UserProfile or be an Admin to request**.

```console
curl -X GET -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/12/
```

This request will return a response containing the specific User Profile.

```py
{
    "data": {
        "type": "UserProfile",
        "id": "1",
        "attributes": {
            "created": "2018-06-27T15:08:09.531149+03:00",
            "modified": "2018-06-28T11:50:11.727434+03:00",
            "role_display": "Admin",
            "gender_display": "Other",
            "expertise_display": "Expert",
            "first_name": "Sample",
            "last_name": "User",
            "email": "sample@admin.me",
            "ona_pk": 1,
            "ona_username": "onauser",
            "payment_number": "+254709439032",
            "approved_submissions": 0,
            "rejected_submissions": 0,
            "approval_rate": 0.0,
            "amount_earned": "0 KES",
            "last_login": "2018-06-28T11:49:51+03:00",
            "avg_submissions": 0.0,
            "avg_approved_submissions": 0.0,
            "avg_rejected_submissions": 0.0,
            "avg_approval_rate": 0.0,
            "avg_amount_earned": "0.0 KES",
            "phone_number": "+254709439032",
            "role": "1",
            "expertise": "4",
            "gender": "0",
            "national_id": "2342343",
            "submission_count": 0,
            "metadata": {}  # The user profile owner only gets to view this
        }
    }
}
```
### DELETE /api/v1/userprofiles/[pk]/ : **User must be Admin to perform this request**

Deletes a specific User Profile with matching pk.

```console
curl -X DELETE -H "Content-type:application/vnd.api+json" https://example.com/api/v1/userprofiles/54/
```

### PATCH /api/v1/userprofiles/[pk]/

Updates a specific user profile with matching pk. **Requires User to either be linked to the UserProfile or be an Admin to request**.

```console
curl -X PATCH -H "Content-Type:application/vnd.api+json" -d '{"data": {"type": "UserProfile","id": "1","attributes": {"first_name": "Leo","last_name": "Sol","role": "1","expertise": "3","gender": "1"}}}' "https://example.com/api/v1/userprofiles/1/"
```
