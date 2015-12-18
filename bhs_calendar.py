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
###########


# import this year's schedule (lists of datetime and tuples of datetimes)
from dates_and_breaks import staff_induction, staff_prof_development, \
                             breaks, first_day, last_day, current_yr, \
                             half_days, public_holidays, secondary

# What period is at what time? eg. period 1 from 8:40 - 9:45
# (import dictionary with the info)
from schedule_times import schedule_times


###########################
# Read Timetable CSV file #
###########################

timetable = open('timetable_files/timetable.csv', 'r',)
tt_reader = csv.reader(timetable)
tt_headers = tt_reader.next()
timetable_dict = {}
for row in tt_reader:
    timetable_dict[int(row[0])] = row[1:]
timetable.close()



############################
#  Define Days of Teaching #
############################

# Let's make a list with the days which are not teaching days (no lessons)
# we can combine the lists of induction, prof. dev., breaks and last day
no_school = breaks + public_holidays + staff_induction + \
            staff_prof_development + last_day

d_o_t = [first_day[0]]  # days of teaching
a_day = td(days=1)  # timedelta of a day

next_day = first_day[0] + a_day
while next_day != last_day[0]:
    if (next_day.weekday() != 5) and (next_day.weekday() != 6):
        # .weekday -> {0 : "Monday", 1 : "Tuesday", etc ..}
        # only add if it's not Saturday (5) and not Sunday (6)
        if next_day in no_school:
            pass  # don't count the day of teaching if it's in the breaks list
        else:
            d_o_t.append(next_day)  # not a weekend + not a break? add to list
    next_day = next_day + a_day


def days_of_teaching_sofar(days_of_teaching, adate = None):
    '''Returns the total days of teaching left
       once we remove holidays, half-days, and vacations
       input: a list with the days of teaching
    '''
    if adate == None:
        d_o_t_sofar = [x for x in days_of_teaching if x <= dt.now()]
        d_o_t_left = [x for x in days_of_teaching if x > dt.now()]
        return len(d_o_t_sofar), len(d_o_t_left)
    else:
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

    return td(hours = hor, minutes = minu) # time delta


def calendar_day_2timetable(full_calendar_day, schedule_times):
    '''
        ```Input:
        full_calendar_day:
        [datetime.datetime(2016, 6, 1, 0, 0),
        4,
        ['IB2 Reg. @7', '','Y11 Science @PL', '', 'Y11 Phys 1 @PR', '9A Sc @PL']
        ]

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
                            timetable_dict[day[1]]]
                            )

    return full_calendar


# for x in append_day_number(d_o_t):
#     print x

print len(append_day_number(d_o_t))
print len(d_o_t) # make a histogram of which number days appear more/less?

full_calendar = create_calendar(d_o_t, timetable_dict, schedule_times)

print schedule_times
print timetable_dict

# for x in full_calendar:
#     print calendar_day_2timetable(x, schedule_times), '\n'


print 'this year you have taught %s days already' \
        % days_of_teaching_sofar(d_o_t)[0]

print 'you have %s days left to teach' \
        % days_of_teaching_sofar(d_o_t)[1], '\n'



print 'this year you have taught %s days already' \
        % days_of_teaching_sofar(d_o_t, dt(2015,12,8))[0]

print 'you have %s days left to teach' \
        % days_of_teaching_sofar(d_o_t, dt(2015, 12, 8))[1], '\n'

print 'total days', len(d_o_t)

print public_holidays
