"""Stuff"""

from datetime import date, datetime, timedelta, time
from enum import Enum


class Terms(Enum):
    M = 0
    L = 1
    E = 2

class Weekdays(Enum):
    """Index days of the week from Monday"""
    Mon = 0
    Tue = 1
    Wed = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6

WEEK_DURATION = timedelta(weeks=1)
DAY_DURATION = timedelta(days=1)

# DEFINE FULL TERM DATES
# From University of Cambridge Statutes and Ordinances 2018 edition
# Chapter II Section 10 "Dates of Term and Full Term"
# Full Michaelmas starts on Tues Jan, ends Fri early Dec or late Nov
# Full Lent starts Tues Jan, ends Fri Mar
# Full Easter starts Tues Apr, ends Fri Jun
# Myear Mst Men Lst Len Est Een
FULL_TERM_DATES = {
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


def full_term_start(year, term):
    """The ."""
    year_adjusted = year-1 if term else year  # Michaelmas == 0 is Falsey
    return date(year, TERM_MONTHS[term], FULL_TERM_DATES[year_adjusted][term])

def get_date(year, term, week, day, hour=None, minute=None):
    # If days are indexed so that Mon=0, reindex so that week starts on Thu
    day_adjusted = day+4 % 7
    # Lectures begin two days after Full term start
    lectures_start = full_term_start(year, term) + 2*DAY_DURATION
    # Add on a number of weeks
    week_start = lectures_start + (week-1)*WEEK_DURATION
    # Finally add on the day within the week
    day = week_start + day_adjusted*DAY_DURATION
    # Update the time if needed
    if hour is None:
        return day
    elif minute is None:
        return datetime.combine(day, time(hour))
    else:
        return datetime.combine(day, time(hour,minute))

def get_dates(year, term, weeks, day, hour=None, minute=None):
    return [get_date(year, term, wi, day, hour, minute) for wi in weeks]

def parse_line(l):
    datetime_raw, description_raw = l.split(';')
    date_spec = parse_datetime(datetime_raw)
    description = description_raw.strip()
    return description, date_spec

def parse_datetime(d):
    ds = d.split()
    if len(ds) == 3:
        term_raw, day_raw, week_raw = ds
        return (
            Terms[term_raw].value,
            parse_week_numbers(week_raw),
            Weekdays[day_raw].value,
        )
    else:
        term_raw, day_raw, week_raw, time_raw = ds
        hour, minute = [int(si) for si in time_raw.split(':')]
        return (
            Terms[term_raw].value,
            parse_week_numbers(week_raw),
            Weekdays[day_raw].value,
            hour,
            minute
        )

def parse_week_numbers(s):
    week_numbers = []
    for si in s.split(','):
        if '-' in si[1:]:
            lims = [int(sij) for sij in si.split('-')]
            week_numbers += [i for i in range(lims[0],lims[1]+1)]
        else:
            week_numbers.append(int(si))
    return week_numbers

def parse_string(s):
    sl = s.splitlines()
    return [parse_line(l) for l in sl if l.strip()]

with open('events.txt','r') as f:
    s = f.read()

pp = parse_string(s)

for pi in pp:
    print(pi)

# print(get_dates(2022,*parse_line(s[3])[1]))
# print(get_dates(2022,*parse_line(s[1])[1]))

quit()



# print(full_term_start(2022, 2))
print(get_date(2022, 2, 6, Weekdays.Mon.value, 15, 32))
print(get_date(2022, 2, 6, Weekdays.Mon.value, 16))
print(get_date(2022, 2, 5, 2))
