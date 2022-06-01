"""Stuff"""

from datetime import date, datetime
from enum import Enum


class Terms(Enum):
    M = 0
    L = 1
    E = 2


# DEFINE FULL TERM DATES
# From University of Cambridge Statutes and Ordinances 2018 edition
# Chapter II Section 10 "Dates of Term and Full Term"
# Full Michaelmas starts on Tues Jan, ends Fri early Dec or late Nov
# Full Lent starts Tues Jan, ends Fri Mar
# Full Easter starts Tues Apr, ends Fri Jun
# Myear Mst Men Lst Len Est Een
FULL_TERM_DATES = {
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
    return datetime(year, TERM_MONTHS[term], FULL_TERM_DATES[year][term])


print(full_term_start(2022, 0))
print(full_term_start(2023, 1))
print(full_term_start(2023, 2))
