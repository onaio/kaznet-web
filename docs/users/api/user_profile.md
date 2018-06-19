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

```json
{
    "data": {
        "type": "UserProfile",
        "id": "3",
        "attributes": {
            "created": "2018-06-18T08:37:57.813788+03:00",
            "modified": "2018-06-18T12:07:33.232180+03:00",
            "first_name": "",
            "last_name": "",
            "email": "sol@admin.me",
            "ona_pk": null,
            "ona_username": null,
            "payment_number": "",
            "approved_submissions": 1,
            "rejected_submissions": 0,
            "approval_rate": 1.0,
            "amount_earned": "44545454.00 KES",
            "last_login": "2018-06-18T15:05:01.869279+03:00",
            "avg_submissions": 1.0,
            "avg_approved_submissions": 1.0,
            "avg_rejected_submissions": 0.0,
            "avg_approval_rate": 1.0,
            "avg_amount_earned": 44545454.0,
            "phone_number": "",
            "role": "1",
            "expertise": "1",
            "gender": "0",
            "national_id": null,
            "submission_count": 1
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
