#!/usr/bin/env python
from datetime import datetime as dt
from datetime import timedelta as td
import re
import csv

'''
Functions to build a School calendar. Used to:

- export our daily schedule to Google Calendar (or iCalendar)
- find out how many days are left of each class / year / etc
- find out how many hours are left of each lesson
'''

###########
# Imports #

from dates_and_breaks import staff_induction, staff_prof_development, \
                             breaks, first_day, last_day, current_yr, \
                             half_days, no_teaching, secondary_meetings, \
                             public_holidays

# What period is at what time? eg. period 1 from 8:40 - 9:45
# (import dictionary with the info)
from schedule_times import schedule_times

###########################
# Read Timetable CSV file #

timetable = open('timetable_files/timetable.csv', 'r',)
tt_reader = csv.reader(timetable)
tt_headers = tt_reader.next()
timetable_dict = {}
for row in tt_reader:
    timetable_dict[int(row[0])] = row[1:]
timetable.close()

############################
#  Define Days of Teaching #

d_o_t = [first_day[0]]  # days of teaching
a_day = td(days=1)  # timedelta of a day
next_day = first_day[0] + a_day # advance a day

while next_day != last_day[0]:
    if (next_day.weekday() != 5) and (next_day.weekday() != 6):
        # .weekday -> {0 : "Monday", 1 : "Tuesday", etc ..}
        # only add if it's not Saturday (5) and not Sunday (6)
        if next_day in no_teaching:
            pass  # don't count the day of teaching if it's in the breaks list
        else:
            d_o_t.append(next_day)  # not a weekend + not a break? add to list
    next_day = next_day + a_day


def days_of_teaching_sofar(days_of_teaching, adate=None):
    '''Returns the total days of teaching left
       once we remove holidays, half-days, and vacations
       input: a list with the days of teaching
    '''
    if adate is None: # not for a specific date (takes today)
        d_o_t_sofar = [x for x in days_of_teaching if x <= dt.now()]
        d_o_t_left = [x for x in days_of_teaching if x > dt.now()]
        return len(d_o_t_sofar), len(d_o_t_left)
    else: # a specific date has been given to calculate days left
        d_o_t_sofar = [x for x in days_of_teaching if x <= adate]
        d_o_t_left = [x for x in days_of_teaching if x > adate]
        return len(d_o_t_sofar), len(d_o_t_left)


def append_day_number(days_of_teaching):
    '''
    The weeks are 6-day weeks. So if Monday is day "1"
    , Tuesday is "2", etc ... and the next Monday will be day 6
    and the following Tuesday will be day "1".
    This function takes the list with the days of teaching, and
    returns them with their corresponding number in a lits of lists:
    [[2015-09-08, 1], [2015-09-09, 2], ... ,etc]

    '''
    d_o_t_and_number = []
    for day_nr, date in enumerate(d_o_t):
        d_o_t_and_number.append([date, (day_nr % 6)+1])
        # Strategy:
        # Half days don't add a number (as they are not used for teaching)
        # since we've removed the half days from our list,
        # we'll just run the counter
        # and return the counter modulo 6 (the 'enumerate' counter starts at 0,
        # so we need to add 1)
    return d_o_t_and_number


def time_string_to_deltatime(time_string):
    '''
    in: time string of the form "14:29"
    out: timedelta(hours=14, minutes=29)
    '''
    hor = int(time_string.split(":")[0])
    minu = int(time_string.split(":")[1])

    return td(hours=hor, minutes=minu) # time delta


def calendar_day_2timetable(full_calendar_day, schedule_times):
    '''
        ```Input:

        full_calendar_day:
        [datetime.datetime(2016, 6, 1, 0, 0),
        4, ['IB2 Reg. @7', '','Y11 Science @PL', '',
        'Y11 Phys 1 @PR', '9A Sc @PL'],]

        the schedule_times:
        {0: ("8:20", "8:40"), ...}  time of each period

        and converts it to a list of events.
        Each event is a tuple with the location, description and
        start and end of events each day:
    '''
    events_of_the_day = []

    for lesson_nr, lesson in enumerate(full_calendar_day[2]):
        if lesson: # is that time period empty? or is there a lesson?
            # Does it have a location? @followed by characters [a-zA-Z,_,-] no space
            location = re.compile(ur'\@[\w\-]', re.DOTALL).findall(lesson)
            if location:
                lesson_location = location[0][1:]
            else:
                lesson_location = 'unspecified location'
            if lesson_nr == 0: # if it's the registration, write the day number
                lesson_description = "[day %01d] " % full_calendar_day[1] + lesson
            elif lesson_nr == 1: # write the day number for the first lesson too
                lesson_description = "[day %01d] " % full_calendar_day[1] + lesson
            else:
                lesson_description = lesson
            start_of_lesson = full_calendar_day[0] + time_string_to_deltatime(schedule_times[lesson_nr][0])
            end_of_lesson = full_calendar_day[0] + time_string_to_deltatime(schedule_times[lesson_nr][1])
            events_of_the_day.append((lesson_description, lesson_location, start_of_lesson, end_of_lesson))

    return events_of_the_day


def create_calendar(days_of_teaching, timetable_dict, schedule_times):
    '''
    Takes as input the days of teaching [datetime, datetime, etc]
    uses the function append_day_number to append the day numbers
    use the timetable to know what times correspond to what day-number
    The output is a list with all 3 attributes:
    [datetime1, day-number, (n-th-period-start, nth-period-end), ... ],
     datetime, day-number+1, (n-th-period-start, nth-period-end), ... ],
    ]
    '''
    simple_cal = append_day_number(days_of_teaching)
    full_calendar = []
    for day in simple_cal:
        full_calendar.append([day[0], day[1],
                             timetable_dict[day[1]]])
    return full_calendar


def get_list_of_unique_lessons(timetable_dict):
    '''
    `input`: timetable_dict
    `output`: unique lessons, for ex:
    ['IB1 Phys', 'IB2 D.tech', 'Y10 Phys 1', 'Lunch Duties',
    'Y11 Phys 2', 'Y11 Phys 1', '9A Sc', 'IB2 Reg.']
    '''
    all_lessons = []

    for i in timetable_dict:
        all_lessons += timetable_dict[i]

    regex = re.compile(ur'\@[\w\-]*', re.DOTALL)
    lessons_without_location = [regex.sub('', lesson).strip() for lesson in all_lessons]
    unique_lessons = list(set(lessons_without_location))
    # remove empty lessons:
    unique_lessons = [x for x in unique_lessons if x]
    return unique_lessons


full_calendar = create_calendar(d_o_t, timetable_dict, schedule_times)

print '#######################################################################################'
print get_list_of_unique_lessons(timetable_dict)





def count_lesson_occurrences(full_calendar, lesson_string, adate=None):
    '''
    Count all the lessons of a particular lesson string in the full_calendar
    for example, how many times does "IB1 Phys" appear throughout the year.
    if adate is given, then count the lessond in the year starting from that
    date
    '''




dates_intervals_to_exclude = [
    [dt(2015, 2, 15), dt(2015, 2, 26)], # Mock exams
    [dt(2015, 4, 14), dt(2015, 4, 14)], # Torch
    [dt(2015, 5, 2), dt(2015, 7, 1)], # exams
]


# Define the full list of break days
all_dates_to_exclude = []
a_day = td(days=1)  # timedelta of a day

for br in dates_intervals_to_exclude:
    if br[0] == br[1]:  # single day break
        all_dates_to_exclude.append(br[0])
    else:  # multi-day holiday
        all_dates_to_exclude.append(br[0])
        next_day = br[0] + a_day
        while next_day != (br[1] + a_day):
            all_dates_to_exclude.append(next_day)
            next_day = next_day + a_day

print all_dates_to_exclude





IB2 = 0

for x in full_calendar:
    # print x[0], '---', x[2]
    project_regex = ur'IB2 D.tech'
    for lesson in x[2]:
        found = re.compile(project_regex, re.DOTALL).findall(lesson)
        if found and x[0] > dt.today():
            if x[0] in all_dates_to_exclude:
                print 'exclude'
                pass
            else:
                IB2 +=1
                print x[0], '---', x[2]


print IB2, '\n'

# def hours_left_of_class()

# print 'this year you have taught %s days already' \
#         % days_of_teaching_sofar(d_o_t)[0]

# print 'you have %s days left to teach' \
#         % days_of_teaching_sofar(d_o_t)[1], '\n'

# print 'this year you have taught %s days already' \
#         % days_of_teaching_sofar(d_o_t, dt(2015,12,18))[0]

# print 'you have %s days left to teach' \
#         % days_of_teaching_sofar(d_o_t, dt(2015, 12, 18))[1], '\n'

# print 'total days', len(d_o_t)
