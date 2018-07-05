"""
Main app utils module
"""
from dateutil.rrule import rrulestr
from tasking.utils import get_rrule_end, get_rrule_start


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
