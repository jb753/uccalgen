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

