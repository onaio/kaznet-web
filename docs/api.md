# Kaznet API #

This documenti describes the Kaznet API.

The Kaznet API is implemented using the [JSON API](http://jsonapi.org/) specification.

## Task Endpoints ##

### /tasks ###

This endpoint allows you to do CRUD operations on Tasks.

You can filter tasks using:

    * parent_id
    * tasklist_id
    * location_id
    * timing_rule
    * status
    * bounty
    * client_id

### /tasklists ###

This endpoint allows you to do CRUD operations on TaskLists.

### /tasksubmissions ###

This endpoint allows you to do CRUD operations on TaskSubmissions.

You can filter task submissions by:

    * task_id
    * user_id
    * location_id
    * data_collection_time
    * submission_time
    * valid
    * approved

### /segmentrules ###

This endpoint allows you to do CRUD operations on SegmentRules.

### /segment ###

This endpoint allows you to segment _something_  i.e. filter using a segment rule.

For example, you can query this endpoint to get a list of tasks that can a user can participate in.

### /locations ###

This endpoint allows you to do CRUD operations on Locations.

### /bounties ###

This endpoint allows you to do CRUD operations on Bounties.

### /clients ###

This endpoint allows you to do CRUD operations on Clients.

## User Endpoints ##

### /users ###

This endpoint allows you to do CRUD operations on Users.

You can filter users by:

    * location_id
    * rating
    * role
    * available
    * group_id
    * expertise_id

### /groups ###

This endpoint allows you to do CRUD operations on Groups.

### /expertise ###

This endpoint allows you to do CRUD operations on Expertise.
