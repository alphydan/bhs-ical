#!/usr/bin/env python
# Class Based implementation of the BHS calendar
from icalendar import Calendar, Event, vText
from datetime import timedelta as td
from datetime import datetime as dt
import tempfile
import pytz
import csv
import os

from import_fun_and_stats import add_half_a_day, add_special_day, \
                                 add_PD_day, add_teaching_day, \
                                 count_teaching_days, count_lesson_days,\
                                 get_list_of_unique_lessons

######################
#    DEFINITIONS     #
######################


class SchoolDay(object):
    """Holds the properties of that day of the school calendar:
    - Is it a teaching day? (if so what is the schedule)
    - What number-day is it?
    - Is it a special day (Sports day? Arts & Performance?
    - Is it a holliday? Part of Steam week?"""

    # def __init__(self, arg):
    #     super(SchoolDay, self).__init__()
    #     self.arg = arg

    # initialize the object with a full_calendar item
    def __init__(self, a_day):
        self.date = a_day
        self.teaching_day = False
        self.half_day = False
        # special_day can be 'sports', 'arts', 'steam', 'RoundSquare' or None
        self.special_day = None  # or string
        # day number can be 1,2,3,4,5,6
        self.day_number = None  # or int
        # meeting can be 'secondary', 'all', 'ib', 'hod_hoy', 'dept' or None
        self.meeting = None  # or string
        self.staff_prof_dev = None  # or PD_day
        self._789_leave = False
        self.y10_leave = False
        self.y11_leave = False
        self.ib1_leave = False
        self.ib2_leave = False
        self.reg = ""
        self.L1 = ""
        self.L2 = ""
        self.L3 = ""
        self.L4 = ""
        self.L5 = ""
        self.all_lessons = []
        self.lunch = ""  # 6th item on the "schedule_times"
        self.stats = {}




    def show_school_day(self):
        month_string = self.a_day[0].strftime("%B")
        sentence = self.a_day[0].strftime('Here is what is happening on the %d, %b %Y:')
        # sentence = "Here is what is happening on the %s of %s:" % (self.a_day[0].day, month_string)
        print sentence


random_day = SchoolDay(dt.today())
print random_day


##################
#    IMPORTS     #
##################


###########################
# Read Timetable CSV file #

timetable = open('../timetable_files/timetable.csv', 'r',)
tt_reader = csv.reader(timetable)
tt_headers = tt_reader.next()
timetable_dict = {}
for row in tt_reader:
    timetable_dict[int(row[0])] = row[1:]
timetable.close()


###########################
# Read Dates n Breaks CSV file #

all_dates = open('dates_n_breaks.csv', 'r',)
current_yr = 2017
tt_reader = csv.reader(all_dates) # time table headers
tt_headers = tt_reader.next()

# I'm creating a list for now, but can skip it (refactor)
# when I have figured out the structure of the program
# call by header instead of index (maybe with pandas?)
all_dates_list = [tt_headers]


for row in tt_reader:
    month=int(row[0].split('-')[1])
    day = int(row[0].split('-')[2])
    year = current_yr if month >= 8 else current_yr+1

    # Convert date string to a proper datetime object
    all_dates_list.append([dt(year, month, day)] + row[1:])

all_dates.close()


# Fill up Calendar (instantiate objects)
bhs_calendar = {}  # Dictionary

for i, x in enumerate(all_dates_list):
    if i > 0:
        this_day = SchoolDay(x[0])
        if x[3]:  # has a day number
            this_day.day_number = int(x[3])
            this_day.teaching_day = True
        if x[1]:  # it's a half day
            this_day.teaching_day = False
            this_day.half_day = True
        elif x[2]:  # it's a special day
            this_day.teaching_day = False
            this_day.special_day = x[2]
        elif (x[4] or x[7] or x[8]):  # induction day, break or holiday
            this_day.teaching_day = False
        elif x[5]:  # PD day
            this_day.teaching_day = False
            this_day.staff_prof_dev = 'PD_day'
        elif x[6]:
            this_day.meeting = x[6]
        elif x[7]:
            this_day.teaching_day = False

        # write study leave data
        if x[9]:
            this_day._789_leave = True
        if x[10]:
            this_day.y10_leave = True
        if x[11]:
            this_day.y11_leave = True
        if x[12]:
            this_day.ib1_leave = True
        if x[13]:
            this_day.ib2_leave = True

        # write schedule
        if x[3]:  # has a day number
            # get time table for that day (a list)
            ttable = timetable_dict[int(x[3])]
            this_day.L1 = ttable[1]
            this_day.L2 = ttable[2]
            this_day.L3 = ttable[3]
            this_day.L4 = ttable[4]
            this_day.L5 = ttable[5]
            this_day.all_lessons = [ttable[1], ttable[2],
                                    ttable[3], ttable[4],
                                    ttable[5]]

        bhs_calendar[i] = this_day



###############################
#      Compile Statistics     #
#                             #
###############################


nr_teaching_days = count_teaching_days(bhs_calendar)
all_classes = get_list_of_unique_lessons(timetable)

cal_list = sorted(bhs_calendar.iteritems())
teaching_days_gone = 0

for a_day in cal_list:
    stat_dict = {}
    day_data = a_day[1]
    stat_dict['days_to_summer'] = (len(cal_list)-a_day[0])

    if day_data.teaching_day:
        stat_dict['days_left_teaching'] = (nr_teaching_days - teaching_days_gone)
        stat_dict['days_taught'] = teaching_days_gone
        teaching_days_gone += 1

        for lesson_string in all_classes:
            stat_dict[lesson_string+'-left'] = count_lesson_days(bhs_calendar,
                                            lesson_string, day_data.date, 'left')
            stat_dict[lesson_string+'-done'] = count_lesson_days(bhs_calendar,
                                            lesson_string, day_data.date, 'done')
        day_data.stats = stat_dict




###############################
# Create the iCalendar Object
#      And Populate it.
###############################


ical = Calendar()

# for compliance with ical format:
ical.add('prodid', '-//My BHS Calendar/afeito//')
ical.add('version', '2.0')

def add_day(ical, bhs_calendar):
    cal_list = sorted(bhs_calendar.iteritems())
    for a_day in cal_list:
        if a_day[1].half_day:
            add_half_a_day(ical, a_day)
        elif a_day[1].special_day:
            add_special_day(ical, a_day)
        elif a_day[1].staff_prof_dev:
            add_PD_day(ical, a_day)
        elif a_day[1].teaching_day:
            add_teaching_day(ical, a_day)

add_day(ical, bhs_calendar)



# Write to file
f = open('BHS_Calendar_2018_afeito.ics', 'wb')
f.write(ical.to_ical())
f.close()



