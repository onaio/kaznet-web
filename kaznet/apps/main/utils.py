"""
Main app utils module
"""
from django.utils import timezone

from dateutil.rrule import rrulestr
from tasking.utils import (generate_task_occurrences,
                           generate_tasklocation_occurrences, get_rrule_end,
                           get_rrule_start)

from kaznet.apps.main.models import TaskLocation, TaskOccurrence


def get_start_end_from_timing_rules(timing_rules: list):
    """
    Get the start and end times from timing rules

    Will return the very very first start
    and the very very last end from the provided timing_rules
    """
    start, end = None, None
    start_list = []
    end_list = []

    # remove obviously invalid
    timing_rules = [x for x in timing_rules if x]

    for timing_rule in timing_rules:
        try:
            start_list.append(get_rrule_start(rrulestr(timing_rule)))
        except ValueError:
            pass

        try:
            end_list.append(get_rrule_end(rrulestr(timing_rule)))
        except ValueError:
            pass

    if start_list:
        start = min(start_list)

    if end_list:
        end = max(end_list)

    return (start, end)


def create_occurrences(task):
    """
    Updates a task's occurrences
    Deletes a task's future occurrences and recreates them
    This task is meant to be called by a post_save signal on the Task model
    """
    # delete all future occurrences
    future_occurrences = TaskOccurrence.objects.filter(
        date__gt=timezone.now().date())
    future_occurrences.delete()
    # now generate new occurrences if any
    # first, occurrences based on the task timing rule
    if task.timing_rule:
        generate_task_occurrences(
            task=task, timing_rule=task.timing_rule,
            OccurrenceModelClass=TaskOccurrence)
    # next, occurrences based on TaskLocations
    task_locations = TaskLocation.objects.filter(task=task)
    for task_location in task_locations:
        generate_tasklocation_occurrences(
            task_location, OccurrenceModelClass=TaskOccurrence)
