## Student Name:
## Student ID:

"""
Task A: Appointment Timeslot Recommender (Stub)

In this lab, you will design and implement an Appointment Slot Recommender using an LLM assistant
as your primary programming collaborator.

You are asked to implement a Python module that recommends available meeting slots within a
defined working window.

The system must:
  • Accept working hours (start and end time).
  • Accept a list of existing busy intervals.
  • Accept a required meeting duration.
  • Accept an optional buffer time between meetings.
  • Optionally restrict suggestions to a candidate time window.
  • Return chronologically ordered appointment slots that satisfy all constraints.

The system must ensure that:
  • Suggested slots fall within working hours.
  • Suggested slots do not overlap busy intervals.
  • Buffer time is respected when evaluating availability.
  • Output ordering is deterministic under identical inputs.

The module must preserve the following invariants:
  • Returned slots must be at least as long as the required duration.
  • No returned slot may violate buffer constraints.
  • The returned list must reflect the current system state.

The system must correctly handle non-trivial scenarios such as:
  • Adjacent busy intervals.
  • Very small gaps between meetings.
  • Buffers eliminating otherwise valid availability.
  • Overlapping or unsorted busy intervals.
  • A meeting duration longer than any available gap.
  • No availability within the working window.

Output:
  The output consists of the next N valid appointment suggestions in chronological order.
  Behavior must be deterministic under ties (if any).

See the lab handout for full requirements.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, time
from typing import List, Optional, Tuple


# ---------------- Data Models ----------------

@dataclass(frozen=True)
class TimeWindow:
    """
    A daily time window.
    Assumption (unless stated otherwise in handout): non-wrapping window where start < end.
    """
    start: time
    end: time


@dataclass(frozen=True)
class BusyInterval:
    """
    A busy interval on the given day.
    Invariant: start < end
    """
    start: time
    end: time


@dataclass(frozen=True)
class Slot:
    """
    A recommended appointment slot.

    start_time is a time-of-day within the working window.
    Deterministic ordering: sort by start_time ascending.
    """
    start_time: time


class InfeasibleSchedule(Exception):
    """Raised when no valid slots can be produced (if required by handout)."""
    pass


# ---------------- Core Function ----------------

def suggest_slots(
    day: date,
    working_hours: TimeWindow,
    busy_intervals: List[BusyInterval],
    duration: timedelta,
    n: int,
    buffer: timedelta = timedelta(0),
    candidate_window: Optional[TimeWindow] = None
) -> List[Slot]:
    """
    Suggest up to the next n valid appointment slots (start times) for the given day.

    Args:
        day: the calendar day for which to suggest slots.
        working_hours: the allowed working window for meetings (start < end).
        busy_intervals: list of busy time intervals (may be overlapping / unsorted).
        duration: required meeting length (must be > 0).
        n: maximum number of slot suggestions to return (n >= 0).
        buffer: optional buffer time required between meetings (buffer >= 0).
        candidate_window: optional extra restriction on suggestions (must lie within this window too).

    Returns:
        A list of Slot objects, sorted by start_time ascending, deterministic under identical inputs.
        If no suitable time slots are available, return an empty list.

    Notes:
        - Suggested slots must fall within working_hours (and candidate_window if provided).
        - Suggested slots must not overlap busy_intervals, considering buffer time.
        - You are free to choose internal representation; inputs use time-of-day.
        - See lab handout for required slot granularity (e.g., 5-min/15-min steps), if any.
    """
     # ---------------- Input Validation ----------------

    if working_hours.start >= working_hours.end:
        raise ValueError("Working hours must satisfy start < end")

    if duration <= timedelta(0):
        raise ValueError("Meeting duration must be >= 1 minute")

    if buffer < timedelta(0):
        raise ValueError("Buffer must be >= 0")

    if n < 0:
        raise ValueError("n must be >= 0")

    if n == 0:
        return []

    if candidate_window is not None:
        if candidate_window.start >= candidate_window.end:
            raise ValueError("Candidate window must satisfy start < end")

        if (candidate_window.start < working_hours.start or
                candidate_window.end > working_hours.end):
            raise ValueError("Candidate window must lie within working hours")

    for interval in busy_intervals:
        if interval.start >= interval.end:
            raise ValueError("Busy interval start must be < end")

        if interval.start < working_hours.start or interval.end > working_hours.end:
            raise ValueError("Busy interval outside working hours")

    # ---------------- Helper Conversions ----------------

    def combine(t: time) -> datetime:
        return datetime.combine(day, t)

    work_start_dt = combine(working_hours.start)
    work_end_dt = combine(working_hours.end)

    if candidate_window:
        search_start = max(work_start_dt, combine(candidate_window.start))
        search_end = min(work_end_dt, combine(candidate_window.end))
    else:
        search_start = work_start_dt
        search_end = work_end_dt

    # ---------------- Normalize Busy Intervals ----------------

    busy_dt = [(combine(b.start), combine(b.end)) for b in busy_intervals]

    busy_dt.sort(key=lambda x: x[0])

    merged_busy = []
    for start, end in busy_dt:
        if not merged_busy:
            merged_busy.append([start, end])
        else:
            last_start, last_end = merged_busy[-1]

            if start <= last_end:  # overlap or adjacency
                merged_busy[-1][1] = max(last_end, end)
            else:
                merged_busy.append([start, end])

    merged_busy = [(s, e) for s, e in merged_busy]

    # ---------------- Slot Search ----------------

    results: List[Slot] = []
    current = search_start

    while current + duration <= search_end:

        meeting_start = current
        meeting_end = meeting_start + duration

        valid = True

        # Check conflicts with busy intervals
        for busy_start, busy_end in merged_busy:

            if (meeting_start < busy_end + buffer and
                    meeting_end > busy_start - buffer):
                valid = False
                break

        # Check buffer relative to previous meeting
        if valid and results:
            prev_start = combine(results[-1].start_time)
            prev_end = prev_start + duration

            if meeting_start < prev_end + buffer:
                valid = False

        if valid:
            results.append(Slot(start_time=meeting_start.time()))

            if len(results) == n:
                break

            current = meeting_end + buffer
        else:
            current += timedelta(minutes=1)

    return results

    ##################################################################
    # TODO: Implement as per lab handout requirements and constraints.
    ##################################################################
    
    ##raise NotImplementedError("suggest_slots has not been implemented yet")
