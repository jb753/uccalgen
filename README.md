# uccalgen

`uccalgen` is a Python script that automates generating an ics file for a set
of events specified in the University of Cambridge week notation.

# Quickstart

List events one per line using the format,
```
$TERM $DAY_OF_WEEK $WEEK_NO [$HOURS:$MINUTES] ; $DESCRIPTION
```
For example, if `calendar.dat` contains,
```
M Thu 1 ; Lectures start
L Mon odd 15:00 ; Supervisions
E Fri 4-8 15:00 ; More supervisions
```
then to generate an ics file for the academic year 2022/23,
```
$ python uccalgen.py calendar.dat output.ics 2022
```

## The problem

The University of Cambridge has a slightly obscure convention for scheduling
lectures and other events: term is divided into eight weeks starting on a
Thursday. (Supposedly, this was so that students could attend Sunday church
services at home before making the slow journey to Cambridge and arriving in
time to start studying.) Your introductory lecture might be on "Thursday, week
1", supervisions might take place "Mondays, odd weeks", your stress levels peak
during the "week 5 blues",  lectures finish "Wednesday, week 8", and so on. The
date of any event is quoted relative to the start of term.

Before a new term begins, I receive my schedule written down in terms of
Cambridge weeks on some kind of pdf timetable. I then have to look up when
exactly term starts, offset to the relevant week and weekday, and enter the
events into my calendar on the correct dates. Tedious and ripe for automation.

## Input file format

We need to know three pieces of information to uniquely specify a day in the
Cambridge calendaring system: which term (Michaelmas, Lent, or Easter), a week
number, and a day of the week. Optionally, we can add a time of day. We also
need a description for what is happening on that date.

Each event is listed on a separate line, with the format:
```
$TERM $DAY_OF_WEEK $WEEK_NO [$HOURS:$MINUTES] ; $DESCRIPTION
```
where a semicolon separates date/time specification from the description, and
the other fields are space-separated (but consecutive spaces are ignored).

Any human-readable file should allow for comments and white space. Blank lines
and lines starting with `#` are ignored.

A date specification looks something like, 
```
M Thu 1 ; Start of Michaelmas term
```
or if a time is required as well,
```
M Thu 1 09:00 ; First lecture
```

It is also useful to support recurring events on multiple weeks, or negative
weeks for before term. These examples are all valid events:
```
M Wed -1 ; Day before lectures start
L Wed odd 15:00 ; Lent term supervisions
L Tue even 15:00 ; Other supervisions
L Fri 4-8 15:00 ; More supervisions
L Mon 1,3,6-9 15:00 ; Even more supervisions
E Thu 2,3 15:00 ; Easter term revision supervisions
```

As a complete example, here is a yearly calendar `yearly.dat` with dates for
admissions interviews and MEng fourth-year project administration:
```
# Admissions

M Mon 9 ; Interviews start
M Fri 11 ; Interview end

# Fourth-year projects

M Wed 1 ; 4YP hazard form
M Fri 5 ; 4YP progress form
M Thu 7 ; 4YP presentations
M Wed 8 ; 4YP presentation feedback
M Fri 9 ; 4YP progress form

L Thu 1 ; 4YP TMR hand in
L Thu 5 ; 4YP TMR mark form
L Fri 5 ; 4YP progress form
L Fri 9 ; 4YP progress form

E Mon -1; 4YP proposals
E Fri 3 ; 4YP preallocation
E Wed 5 ; 4YP report hand in
E Thu 6 ; 4YP presentations start
E Fri 7 ; 4YP planning form
```

## Algorithm

* Input the academic year of interest as a command-line option;
* Parse an event file line-by-line, converting the formatted data into a tuple of indices for `(term, week_no, day_of_week)` and an optional time; 
* The University [Statutes and
Ordinances](https://www.admin.cam.ac.uk/univ/so/2018/chapter02-section10.html#heading1-10)
do not specify a general rule for determining when term starts, instead giving a table
up to 2030. So I thought the best I could do was hard-code the start dates of every term and
update in eight years time;
* Offset from the term start date by the required number of weeks and days
  to give a `datetime` object for each event;
* Use the [icalendar](https://icalendar.readthedocs.io/en/latest/)
library to generate an ics file with our events in it.

## Usage

To generate an ics from the yearly calendar input data given above, for the
next academic year 2022/23,
```
$ python uccalgen.py yearly.dat yearly.ics 2022
```
The resulting `yearly.ics` can be imported into any standards-compliant
calendar application.
