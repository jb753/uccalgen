#!/usr/bin/env python3
"""Generate ics files for events by University of Cambridge term weeks.

James Brind, June 2022"""

import sys, icalendar
from datetime import date, datetime, timedelta, time
from hashlib import sha256

# Mappings from strings to indexes for term, day of week
TERMS = {"m": 0, "l": 1, "e": 2}
WEEKDAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}

# FULL TERM DATES
# From University of Cambridge Statutes and Ordinances 2018 edition
# Chapter II Section 10 "Dates of Term and Full Term"
# Full Michaelmas starts on Tues Oct
# Full Lent starts Tues Jan
# Full Easter starts Tues Apr
# Keyed with the Michaelmas year
FULL_TERM_DATES = {
    2017: [3, 16, 24],
    2018: [2, 15, 23],
    2019: [8, 14, 21],
    2020: [6, 19, 27],
    2021: [5, 18, 26],
    2022: [4, 17, 25],
    2023: [3, 16, 23],
    2024: [8, 21, 29],
    2025: [7, 20, 28],
    2026: [6, 19, 27],
    2027: [5, 18, 25],
    2028: [3, 16, 24],
    2029: [2, 15, 23],
}

# Michaelmas Term starts in October
# Lent Term starts in January
# Easter Term starts in Apr
TERM_MONTHS = [10, 1, 4]

# Time intervals
WEEK_DURATION = timedelta(weeks=1)
DAY_DURATION = timedelta(days=1)
HOUR_DURATION = timedelta(hours=1)


def full_term_start(year, term):
    """The start date of `term` in academic year beginning `year`."""
    # Adjust the year forward if Lent or Easter (Michaelmas == 0 is Falsey)
    year_adjusted = year + 1 if term else year
    return date(year_adjusted, TERM_MONTHS[term], FULL_TERM_DATES[year][term])


def get_date(year, term, week, day, hour=None, minute=None):
    """Given all indexes for a Cambridge term date, return datetime."""
    # If days are indexed so that Mon=0, reindex so that week starts on Thu
    day_adjusted = (day + 4) % 7
    # Lectures begin two days after Full term start
    lectures_start = full_term_start(year, term) + 2 * DAY_DURATION
    # Add on a number of weeks
    week_start = lectures_start + (week - 1) * WEEK_DURATION
    # Finally add on the day within the week
    day = week_start + day_adjusted * DAY_DURATION
    # Update the time if needed
    if hour is None:
        return day
    elif minute is None:
        return datetime.combine(day, time(hour))
    else:
        return datetime.combine(day, time(hour, minute))


def get_dates(year, term, weeks, day, hour=None, minute=None):
    """For recurring events on multiple weeks, get a list of datetimes."""
    return [get_date(year, term, wi, day, hour, minute) for wi in weeks]


def parse_line(l):
    """Given a complete input line, split description and date spec, parse."""
    datetime_raw, description_raw = l.split(";")
    date_spec = parse_datetime(datetime_raw)
    description = description_raw.strip()
    return description, date_spec


def parse_datetime(d):
    """Given a datetime string in my format, extract numbers.

    'TERM_LETTER DAY_OF_WEEK WEEK_NUMS [HH:MM]' ->
        (term_index, week_index, day_index, [hours, minutes])

    Examples
    --------

    'E Tue 2,5 15:00' -> (2, (2,5), 1, 15, 0)
    'M Wed 1' -> (0, (1,), 1)

    """

    ds = d.split()
    if len(ds) == 3:
        term_raw, day_raw, week_raw = ds
        return (
            TERMS[term_raw.lower()],
            parse_week_numbers(week_raw),
            WEEKDAYS[day_raw.lower()],
        )
    else:
        term_raw, day_raw, week_raw, time_raw = ds
        hour, minute = [int(si) for si in time_raw.split(":")]
        return (
            TERMS[term_raw.lower()],
            parse_week_numbers(week_raw),
            WEEKDAYS[day_raw.lower()],
            hour,
            minute,
        )


def parse_week_numbers(s):
    """Given a string, return tuple of week numbers.

    Examples
    --------

    '1' -> 1
    '1,3,5' -> [1,3,5]
    '4-6' -> [4,5,6]
    '-1' -> -1
    '-1,3,6-8' -> [-1,3,6,7,8]

    """

    if s.strip().lower() == "odd":
        week_numbers = [i for i in range(1, 9, 2)]
    elif s.strip().lower() == "even":
        week_numbers = [i for i in range(2, 10, 2)]
    else:
        week_numbers = []
        for si in s.split(","):
            if "-" in si[1:]:
                lims = [int(sij) for sij in si.split("-")]
                week_numbers += [i for i in range(lims[0], lims[1] + 1)]
            else:
                week_numbers.append(int(si))

    return tuple(week_numbers)


def load_file(filename):
    """Open file by name, parse contents into descriptions and date specs."""
    with open(filename, "r") as f:
        return [
            parse_line(l)
            for l in f.read().splitlines()
            if l.strip() and not l.startswith("#")
        ]


def default_year():
    """Choose a year based on current date.

    From the end of the Long Vac to Christmas Vac, the most relavent Michaelmas
    term starts in the current year.

    From Lent to end of Easter, the relavent Michaelmas started last year.

    """
    now = datetime.now()
    if now.month < 7:
        return now.year - 1
    else:
        return now.year


def save_ical(events, current_year, filename):
    """Write a list of tuples of Cambridge term indexes to an ics."""

    cal = icalendar.Calendar()
    cal.add("prodid", "-//James Brind//uccalgen.py//EN")
    cal.add("version", "2.0")
    now = datetime.now()

    for description, date_specs in events:

        dates = get_dates(current_year, *date_specs)

        for d in dates:

            e = icalendar.Event()
            e.add("summary", description)
            e.add("dtstamp", now)

            if type(d) == date:
                e.add("dtstart", d)
            else:
                e.add("dtstart", d)
                e.add("dtend", d + HOUR_DURATION)

            # Make an event UID by hashing the description and date together
            # This ensures that events are not duplicated if we import twice
            hashstr = bytes(description + d.isoformat(), 'utf-8')
            e.add("uid",sha256(hashstr).hexdigest())

            cal.add_component(e)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())


if __name__ == "__main__":

    # Parse input arguments
    if len(sys.argv) == 3:
        infile, outfile = sys.argv[1:]
        current_year = default_year()
    elif len(sys.argv) == 4:
        infile, outfile, current_year_raw = sys.argv[1:]
        current_year = int(current_year_raw)
    else:
        print("Usage: uccalgen.py IN_DAT OUT_ICS [MICH_YEAR]")
        quit()

    # Read events from the input file, process, write output file
    events = load_file(infile)
    save_ical(events, current_year, outfile)
