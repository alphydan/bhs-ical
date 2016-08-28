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

from dates_and_breaks import first_day, last_day, current_yr, staff_induction,\
                             staff_prof_development, secondary_meetings, \
                             half_days, sports_day, performing_arts_day, \
                             breaks, public_holidays, no_teaching, steam_week,\
                             unique_special_days

from calendar_statistics import days_of_teaching_sofar

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
            pass  # don't count the day of teaching if it's in the no-teaching-today list
        else:
            d_o_t.append(next_day)  # not a weekend + not a break? add to list
    next_day = next_day + a_day


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


def add_special_days_to_calendar(full_calendar):
    '''
    This adds special days like sports day, arts day
    STEAM day. and modifies the schedule
    '''
    for a_day in full_calendar:

        if a_day[0] in sports_day:
            a_day.append('Sports Day')

        if a_day[0] in steam_week:
            a_day.append('STEAM WEEK')

        if a_day[0] in performing_arts_day:
            a_day.append('Performing Arts Day')

    for a_half_day in half_days:
        full_calendar.append([a_half_day, 0, ['','','','','',''],
                             'Half Day'])

    return full_calendar



full_calendar = create_calendar(d_o_t, timetable_dict, schedule_times)
new_full_calendar = add_special_days_to_calendar(full_calendar)

for x in new_full_calendar:
    print x

# for x in full_calendar:
#     print x



# dates_intervals_to_exclude = [
#     [dt(2015, 2, 15), dt(2015, 2, 26)], # Mock exams
#     [dt(2015, 4, 14), dt(2015, 4, 14)], # Torch
#     [dt(2015, 5, 2), dt(2015, 7, 1)], # exams
# ]


# Define the full list of break days
# all_dates_to_exclude = []
# a_day = td(days=1)  # timedelta of a day

# for br in dates_intervals_to_exclude:
#     if br[0] == br[1]:  # single day break
#         all_dates_to_exclude.append(br[0])
#     else:  # multi-day holiday
#         all_dates_to_exclude.append(br[0])
#         next_day = br[0] + a_day
#         while next_day != (br[1] + a_day):
#             all_dates_to_exclude.append(next_day)
#             next_day = next_day + a_day

# print all_dates_to_exclude





# IB2 = 0

# for x in full_calendar:
#     # print x[0], '---', x[2]
#     project_regex = ur'IB2 D.tech'
#     for lesson in x[2]:
#         found = re.compile(project_regex, re.DOTALL).findall(lesson)
#         if found and x[0] > dt.today():
#             if x[0] in all_dates_to_exclude:
#                 print 'exclude'
#                 pass
#             else:
#                 IB2 +=1
#                 print x[0], '---', x[2]


# print IB2, '\n'

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

# class SchoolDay(object):
#     """Holds the properties of that day of the school calendar:
#     - Is it a teaching day? (if so what is the schedule)
#     - What number day is it?
#     - Is it a special day (Sports day? Arts & Performance?
#     - Is it a holliday? Part of Steam week?"""

#     # def __init__(self, arg):
#     #     super(SchoolDay, self).__init__()
#     #     self.arg = arg

#     # initialize the object with a full_calendar item
#     def __init__(self, a_day):
#         self.a_day = a_day

#     def show_school_day(self):
#         month_string = self.a_day[0].strftime("%B")
#         sentence = self.a_day[0].strftime('Here is what is happening on the %d, %b %Y:')
#         # sentence = "Here is what is happening on the %s of %s:" % (self.a_day[0].day, month_string)
#         print sentence

# print '\n\n', '##################', '\n'
# arandomday = SchoolDay(full_calendar[0])
# print arandomday.a_day
# arandomday.show_school_day()
# print arandomday.a_day
