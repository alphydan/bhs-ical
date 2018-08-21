from datetime import datetime as dt
from datetime import timedelta as td

from newcal import all_dates_list, bhs_calendar, current_yr
from import_fun_and_stats import get_list_of_unique_lessons # , timetable_path_n_file




def add_lesson_to_wld(lesson_attribute, weekly_lesson_dictionary):
    '''
    add lesson to weekly lesson dictionary
    increments counter of lessons if the lesson is in the dictionary
    or creates a new entry to count this lesson
    '''
    lesson = lesson_attribute.split('@')[0].rstrip()
    # removes the location: 'Y11 Phys @PL' --> 'Y11 Phys'

    if (lesson in weekly_lesson_dictionary) and (len(lesson) > 1):
        weekly_lesson_dictionary[lesson] += 1
    elif len(lesson) > 1:  # don't count empy lesson
        weekly_lesson_dictionary[lesson] = 1

    return None

def total_weekly_lessons(weekly_lesson_dictionary):
    ''' returns an integer
        which is the total number of lessons that week.
        typically 15 - 20
    '''
    return sum(weekly_lesson_dictionary.values())

def when_is_this_lesson(year_lesson_substring, day_data):
    '''
    input: string like 'Y8' or 'Y10'
    outpt: Lesson number when it's taught or False
    '''

    is_lesson_taught = [L for L in day_data.all_lessons
                        if year_lesson_substring in L]
    if len(is_lesson_taught) == 0:
        return False
    else:
        indx = [i+1 for i, L in enumerate(day_data.all_lessons)
                if year_lesson_substring in L][0]
        lesson = is_lesson_taught[0]
        return indx, lesson


def generate_weekly_calendar(full_calendar, monday, friday):
    this_week = []
    for x in full_calendar:
        if (x[0] >= monday) and (x[0] <= friday):
            this_week.append(x)
    return this_week

def what_week_are_we(someday=None):
  '''
  When today() is called, it returns the date of Monday
  this week and the day of Friday this week.
  Output: datetime of Monday, datetime of Friday
  '''
  if someday:
    weekday_today = someday.weekday()
    monday = someday - td((weekday_today), 0, 0)
    friday = monday+  td(4,0,0)
    return monday, friday
  else:
    weekday_today = dt.today().weekday()
    monday = dt.today() - td((weekday_today), 0, 0)
    friday = monday + td(4,0,0)
    return monday, friday



cal_list = sorted(bhs_calendar.iteritems()) # calendar list


##########################################
#  Make dict with the weeks of the year  #
##########################################

weeks_dict = {0: (dt(2018, 8, 27), dt(2018, 8, 31))}
week_counter = 1
for i in cal_list:
    if i[0] > 6:
        # skip the first week (as it's already item zero above)
        if i[1].date.weekday() == 0:
            monday = i[1].date
        elif i[1].date.weekday() == 4:
            friday = i[1].date
            weeks_dict[week_counter] = (monday, friday)
            week_counter += 1

print "There are %s weeks in the %s-%s year" % \
      (len(weeks_dict), current_yr, current_yr+1)



#############################################################
# Make list with a dict of how many lessons of each class   #
#                     are given each week                   #
#############################################################
# Example, weekly_lesson_dictionary[1] =
# [datetime.datetime(2018, 9, 3, 0, 0),
# {'Y10BC Phy 2': 2, 'Y8B Sc': 2,
#  'Y11 Phy': 2, 'Y10A Phy 1': 1,
# 'IB1': 2, 'IB2': 2}
# ]

weekly_lesson_configurations = []
for i in range(len(weeks_dict)):  # loop over all weeks
    monday = weeks_dict[i][0]
    friday = weeks_dict[i][1]

    wld = {}  # weekly lesson dictionary
    for x in cal_list:

        if (x[1].date >= monday) and (x[1].date <= friday) \
            and (not x[1].half_day) and (not x[1].special_day):
            add_lesson_to_wld(x[1].L1, wld)
            add_lesson_to_wld(x[1].L2, wld)
            add_lesson_to_wld(x[1].L3, wld)
            add_lesson_to_wld(x[1].L4, wld)
            add_lesson_to_wld(x[1].L5, wld)
    weekly_lesson_configurations.append([monday, wld])




all_weeks = sorted(weeks_dict.iteritems())
cal_list = sorted(bhs_calendar.iteritems()) # calendar list
# the unwieldy animal of dict of dicts with lists of lists:
full_schedule_by_year = {}

for aweek in all_weeks:
  # Not sure why this is here!!???
  full_schedule_by_year[aweek[1][0]] = \
  {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}



for aweek in sorted(full_schedule_by_year):
    for adate in cal_list:
    # for aweek in sorted(weeks_dict.iteritems()):  # weeks list
        monday = aweek
        friday = aweek + td(days=4)
        aday = adate[1]
        if (aday.date >= monday) and (aday.date <= friday):

            whe = when_is_this_lesson('Y8', aday)
            # assumption: a given lesson only happens once a day
            if whe:
                full_schedule_by_year[monday][0].append( \
                              [aday.date, whe[0], whe[1]])

            whe = when_is_this_lesson('Y10', aday)
            if whe:
                full_schedule_by_year[monday][1].append( \
                              [aday.date, whe[0], whe[1]])

            whe = when_is_this_lesson('Y11 Phy 1', aday)
            if whe:
                full_schedule_by_year[monday][2].append( \
                              [aday.date, whe[0], whe[1]])

            whe = when_is_this_lesson('Y11 Phy 6', aday)
            if whe:
                full_schedule_by_year[monday][3].append( \
                              [aday.date, whe[0], whe[1]])

            whe = when_is_this_lesson('IB1', aday)
            if whe:
                full_schedule_by_year[monday][4].append( \
                              [aday.date, whe[0], whe[1]])

            whe = when_is_this_lesson('IB2', aday)
            if whe:
                full_schedule_by_year[monday][5].append( \
                              [aday.date, whe[0], whe[1]])
            # if aday.date == friday:
                # print full_schedule_by_year[monday], '\n', '-----------------------', '\n'


# --> Now use this full_schedule_by_year object to make the layout
# and use the usual cal_list to make the calendar on the right page
