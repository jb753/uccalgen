import uccalgen

def test_parse_week_numbers():
    strings = ['1', '1,3,5', '4-6', '-1', '-1,3,6-8', 'odd', 'EVEN']
    values = [(1,), (1,3,5), (4,5,6), (-1,), (-1,3,6,7,8), (1,3,5,7), (2,4,6,8)]
    for s,v in zip(strings, values):
        assert uccalgen.parse_week_numbers(s) == v

def test_4yp_2021():
    """Compare my dates to fourth-year project list from teaching office."""

    current_year = 2021
    events = uccalgen.load_file('4yp.dat')
    dates = [uccalgen.get_dates(current_year, *d)[0] for _,d in events]

    truth = [
        '2021-10-13',
        '2021-11-05',
        '2021-11-18',
        '2021-12-01',
        '2021-12-03',
        '2022-01-20',
        '2022-02-17',
        '2022-02-18',
        '2022-03-18',
        '2022-04-18',
        '2022-05-13',
        '2022-06-01',
        '2022-06-02',
        '2022-06-10'
    ]

    for date, val in zip(dates, truth):
        assert str(date) == val

def test_consecutive_days():
    """Check that weekwise dates are consecutive."""

    day_names = ['Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed']
    days_ordered = [uccalgen.Weekdays[k].value for k in day_names]

    current_year = 2022
    for term in range(3):
        dates = []
        for week in range(-1,9):
            for day in days_ordered:
                dates.append(uccalgen.get_date(current_year, term, week, day))

        for i in range(len(dates)-1):
            assert dates[i+1]-dates[i] == uccalgen.DAY_DURATION

def test_term_ends():
    """Check that end of Full Term is when we expect."""

    full_term_ends = {
        2017: [1, 16, 15],
        2018: [30, 15, 14],
        2019: [6, 13, 12],
        2020: [4, 19, 18],
        2021: [3, 18, 17],
        2022: [2, 17, 16],
        2023: [1, 15, 14],
        2024: [6, 21, 20],
        2025: [5, 20, 19],
        2026: [4, 19, 18],
        2027: [3, 17, 16],
        2028: [1, 16, 15],
        2029: [30, 15, 14],
    }

    for year, end_days in full_term_ends.items():
        for term in range(3):
            week_num = 9 if term<2 else 8
            date_now = uccalgen.get_date(year, term, week_num, uccalgen.Weekdays.Fri.value)
            assert date_now.day == end_days[term]
