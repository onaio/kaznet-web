# Backend API Architecture #

![kaznet backend](https://user-images.githubusercontent.com/372073/39635248-9946d06e-4fc5-11e8-8228-49833495cc4b.png)

We have a situation where we need to implement tasking for the ILRI Kaznet project, but we need to implement it in a way that:

    * is not very tightly coupled with onadata - so that including tasking in onadta is optional
    * allows us to have tasking in onadata without needing anything from the Kaznet system
    * ensures that all the necessary Kaznet tasking features will work as epxected

To achieve this goal, I propose that the implementation be as follows:

## 1. Tasking Library ##

We will build a Django  that will implement the core tasking features.  The general idea is that this tasking library provides a base that is easily extensible to add `tasking` to any Django project.

Specifically, in our case, it will be used to add tasking to both Kaznet and Onadata.  Why is this necessary?  Well, as we will see below, Onadata and Kaznet may have to implement tasking in slightly different ways and having a common library that they can both extend is, in my view, the best way to  solve this problem.

The various data models that the tasking library will provide are defined below:

### i. Task ###

A discrete data collection activity to be completed by a number of persons at specific locations and time.

* **id** (int) *required*
* **parent_id** (int) *optional* - the id of the parent task
* **name** (str) *required*
* **description** (str) *optional*
* **tasklist_id** (int) *optional*
* **location_id** (int) *optional*
* **timing_rule** (str) *required* - stores an `rrule` (as defined in the [iCalendar RFC](https://tools.ietf.org/html/rfc5545)) that defines when the task starts, ends and any recurrence
* **total_submissions_target** (int) *optional* - total submissions for the task
* **user_submissions_target** (int) *optional* - per user submissions for the task
* **status** (int) *required* - one of active, closed, or draft

### ii. TaskSubmission ###

Represents the task submission.  It is essentially an Ona submission with extra metadata

* **id** (int) *required*
* **task_id** (int) *required*
* **user_id** (int) *required*
* **location_id** (id) *required*
* **submission_time** (datetime) *required*
* **valid** (bool) *required* - based on initial automated checks
* **approved** (bool) *required* - based on a manual user review
* **comments** (str) *required*

### iii. TaskList ###

A way to group tasks.  This represents a many-to-one relationship between a TaskList and Tasks.

* **id** (int) *required*
* **name** (str) *required*

### iv. SegmentRule ###

A rule that is used to segment _things_.

* **id** (int) *required*
* **target** (str) *required* - the model that the rule runs against
* **target_field** (str) *required* - the field on the target model that this rule applies to
* **target_field_value** (int) *required* - the value of the target_field that is expected
* **description** (str) *optional*

### v. SegmentRuleTask ###

A way to relate Tasks and Segment Rules.  This represents a many-to-many relationship between SegmentRules and Tasks

* **task_id** (int) *required*
* **segment_rule_id** (int) *required*

### vi. Location ###

* **id** (int) *required*
* **name** (str) *required*
* **country** (str) *required*
* **geopoint** (str)  *optional
* **radius** (decimal) *optional*
* **geom** (str)- *optional* the shapefile that represents the location

## 2. Kaznet Application ##

We will build a Django application that will extend the tasking library to add unique Kaznet features.

### i. KaznetTask ###

This model extends the `Task` model from the tasking application and adds the following fields:

* **xform_id** (int) *required*
* **client_id** (int) *optional*
* **bounty_id** (int) *required*

### ii. KaznetTaskSubmission ###

This model extends the `TaskSubmission` model from the tasking application and adds the following fields:

* **submission_id** (int) *required*
* **data_collection_time** (datetime) *required*
* **data** (json) *required* - the JSON data of the linked Onadata Submission
* **bounty_id** (int) *required*
* **rating** (int) *required* - the rating of the user for this submission

### iii. Bounty ###

Represents the amount (reward) paid for a valid task submission.

* **id** (int) *required*
* **task id** (id) *required*
* **date** (datetime) *required*
* **amount** (decimal) *required*
* **currency** (str) *required* - standard representation of currency e.g. USD, KES, EUR, etc

### iv. Client ###

The entity who commissions a task.  This is a client from ILRI's perspective i.e. someone who hires ILRI to collect certain data

* **id** (int) *required*
* **name** (str) *required*

### v. User ###

* **id** (int) *required*
* **first_name** (str) *required*
* **last_name** (str) *required*
* **email** (str) *required*
* **phone** (str) *required*
* **location_id** (int) *required*
* **gender** (int) *required* - one of Male, Female, Other
* **available** (bool) *required*
* **rating** (int) *required*
* **role** (int) *required* - one of Admin, Editor, Contributor

### vi. Group ###

A way to group users.

* **id** (int) *required*
* **name** (str) *required*
* **description** (str) *required*

### vii. UserGroup ###

A way to relate users and groups.  This represents a many-to-many relationship between Users and Groups.

* **user_id** (int) *required*
* **group_id** (int) *required*

### viii. Expertise ###

* **id** (int) *required*
* **name** (str) *required*
* **description** (str) *optional*

### ix. UserExpertise ###

A way to relate users and expertise.  This represents a many-to-many relationship between Users and Expertise.

* **user_id** (int) *required*
* **expertise_id** (int) *required*
